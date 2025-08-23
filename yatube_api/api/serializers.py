from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post.

    Предоставляет информацию о:
    - ID поста;
    - Тексте поста;
    - Авторе (только для чтения);
    - Изображении (опционально);
    - Группе (опционально);
    - Дате публикации.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author',
            'image',
            'group',
            'pub_date'
        )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group.

    Предоставляет информацию о:
    - ID группы;
    - Названии группы;
    - Slug группы;
    - Описании группы.
    """

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment.

    Предоставляет информацию о комментарии, включая:
    - ID;
    - Автора (только для чтения);
    - Post (ID поста, только для чтения);
    - Текст комментария;
    - Дату создания.

    Примечания:
    1) Поле `post` доступно только для чтения.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created'
        )
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow
    (подписки пользователей).

    Notes:
        1) 'user' заполняется автоматически
    текущим пользователем при создании.
        2) Используется `SlugRelatedField`
    для отображения username вместо ID.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        ]

    def validate_following(self, data):
        """
        Проверяет, что пользователь
        не пытается подписаться на себя.
        """
        if data == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data
