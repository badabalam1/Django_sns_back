from rest_framework import serializers
from .models import *
from api2 import models as UserModel


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('id', 'user_id', 'author', 'content')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('post', 'author_id', 'author_name', 'content')


class PostGet(serializers.ModelSerializer):
    # like_count = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        fields = ('id', 'user_id', 'author', 'content')

    # def get_like_count(self, obj):
    #     return PostModel.get_like()
    #     return obj.like.count()


class CommentGet(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = ('post', 'author_id', 'author_name', 'content')
