import django_filters

from message.models import User


class UserFilter(django_filters.FilterSet):
    '''Кастомный фильтр.'''

    name = django_filters.CharFilter(
        field_name='username',
    )
    role = django_filters.CharFilter(
        field_name='role'
    )

    class Meta:
        model = User
        fields = ('username', 'role',)
