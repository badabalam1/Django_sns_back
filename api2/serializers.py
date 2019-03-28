from rest_framework import serializers
from .models import *


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'id', 'name', 'phone', 'gender')


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'phone', 'gender')


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password',
                  'name', 'phone', 'gender')


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password', 'profile_image',
                  'name', 'phone', 'gender', 'follows')


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username')
