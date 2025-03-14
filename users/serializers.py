from rest_framework import serializers
from .models import User
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'name', 'email', 'last_login']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = f'{settings.CURRENT_URL}{instance.avatar}'

        return data