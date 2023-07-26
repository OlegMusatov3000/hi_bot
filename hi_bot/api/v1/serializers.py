from rest_framework import serializers

from message.models import User


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "User".'''

    class Meta:
        fields = ('username', 'role',)
        model = User
