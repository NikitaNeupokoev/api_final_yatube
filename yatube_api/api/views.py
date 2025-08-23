from django.shortcuts import get_object_or_404

from rest_framework import (
    filters,
    mixins,
    permissions,
    viewsets
)
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post.

    Предоставляет CRUD-операции для постов.
    Автоматически устанавливает автора поста при создании.

    Notes:
        1)  Автор поста устанавливается автоматически как текущий пользователь.
        2)  Используется `LimitOffsetPagination` для постраничного вывода.
        3)  Если в запросе указана группа, она связывается с постом.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Автоматически устанавливает
        автора поста при создании.
        """
        serializer.save(
            author=self.request.user,
            group=serializer.validated_data.get('group')
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Comment.

    Предоставляет CRUD-операции для комментариев к посту.
    Автоматически устанавливает автора
    и пост при создании комментария.

    Notes:
        1)  ID поста передается в URL как `post_id`.
        2)  Автор комментария устанавливается автоматически как.
    текущий пользователь.
        3)  Пост, к которому относится комментарий, находится по.
    `post_id` в URL.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def _get_post(self):
        """Возвращает пост по ID из URL параметров."""
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )

    def get_queryset(self):
        """Возвращает все комментарии для текущего поста."""
        return self._get_post().comments.all()

    def perform_create(self, serializer):
        """
        Создает комментарий с автоматическим определением
        автора и поста.
        """
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(
                Post, pk=self.kwargs.get('post_id')
            )
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Group.

    Предоставляет доступ только для чтения к группам.

    Notes:
        1)  Используется `ReadOnlyModelViewSet`, так как группы не должны
    создаваться/редактироваться через API.
        2)  Доступ к группам разрешен всем.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для модели Follow (подписки).

    Предоставляет операции для подписки на пользователей.

    Notes:
        1)  Поддерживаются только операции получения списка подписок (GET) и
        создания подписки (POST).
        2)  Доступна фильтрация по username пользователя, на которого
        подписываются.
        3)  Поле 'user' (кто подписывается) устанавливается автоматически как
        текущий пользователь при создании.
        4)  Для получения списка подписок используется обратная связь
        `follower` от модели `User`.
    """

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=following__username',)

    def get_queryset(self):
        """Возвращает все подписки текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Создает подписку с автоматическим
        определением пользователя.
        """
        serializer.save(user=self.request.user)
