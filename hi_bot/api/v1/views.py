from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from message.models import User
from .serializers import UserSerializer
from .filters import UserFilter


class UserViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Получить набор пользователей удовлетворяющий фильтру.'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
