from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName', 'password', 'userNameDisplay']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
