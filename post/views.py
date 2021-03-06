from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.conf import settings
from . import serializers
from .models import *
from api2 import models as usermodel
import jwt

# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_payload(request):
    token = request.META['HTTP_AUTHORIZATION']
    payload = jwt.decode(token, settings.SECRET_KEY)
    return payload


class MyPost(APIView):
    def get(self, request, limit_id, user_id, format=None):
        payload = jwt_payload(request)

        user = usermodel.UserModel.objects.get(id=user_id)
        posts = PostModel.objects.filter(
            user_id=user).order_by('-created_at')[:limit_id]
        serializer = serializers.PostGet(posts, many=True)
        return Response(data=serializer.data)


class Post_List(APIView):

    def get(self, request, limit_id, format=None):
        payload = jwt_payload(request)
        data = {}

        user = usermodel.UserModel.objects.get(
            username=payload['username'])

        followings = list(user.get_followings()) + [user]
        posts = PostModel.objects.filter(
            user_id__in=followings).order_by('-created_at')[:limit_id]

        serializer = serializers.PostGet(posts,  many=True)

        return Response(data=serializer.data)


class Post(APIView):

    # 글 작성
    def post(self, request, format=None):
        payload = jwt_payload(request)

        user = usermodel.UserModel.objects.get(username=payload['username'])

        data = {}
        data['author'] = user.name
        data['content'] = request.data['content']

        serializer = serializers.PostCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'result': '에러가 발생했습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 글 수정
    def put(self, request, post_id, format=None):
        payload = jwt_payload(request)

        try:
            print(payload['user_id'])
            print(post_id)
            post = PostModel.objects.get(
                id=post_id, user_id=payload['user_id'])
            post.content = request.data['content']
            post.save()
            return Response(data={'comment': request.data['content'], 'post_id': post_id})
        except PostModel.DoesNotExist:
            return Response(data={'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 글 삭제
    def delete(self, request, post_id, format=None):
        payload = jwt_payload(request)

        try:
            post = PostModel.objects.get(
                id=post_id, user_id=payload['user_id'])
            post = post.delete()
            print(post)
            return Response(data={'message': '삭제했습니다.', 'post_id': post_id}, status=status.HTTP_200_OK)
        except PostModel.DoesNotExist:
            return Response(data={'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
    # 댓글 리스트
    def get(self, request, post_id, format=None):
        try:
            post = get_object_or_404(PostModel, id=post_id)
            comment = CommentModel.objects.filter(post=post)
            print(comment)

            serializer = serializers.CommentGet(comment, many=True)
            return Response(data=serializer.data)
        except PostModel.DoesNotExist:
            return Response(data={'message': '글이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 작성
    def post(self, request, post_id, format=None):
        payload = jwt_payload(request)

        data = {}

        try:
            post = get_object_or_404(PostModel, id=post_id)
            user = usermodel.UserModel.objects.get(
                username=payload['username'])

            data['author_id'] = user.id
            data['author_name'] = user.name
            data['content'] = request.data['content']
            serializer = serializers.CommentCreateSerializer(
                data=data)
        except PostModel.DoesNotExist:
            return Response(data={'message': '글이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'result': '에러가 발생했습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정
class Comment_REST(APIView):
    def put(self, request, post_id, comment_id, format=None):
        payload = jwt_payload(request)

        data = {}
        post = PostModel.objects.get(id=post_id)
        comment = CommentModel.objects.get(post=post, id=comment_id)

        if comment.author == payload['username']:
            comment.content = request.data['content']
            comment.save()
            return Response(data={'message': '수정이 되었습니다.'}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(data={'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id, format=None):
        payload = jwt_payload(request)

        data = {}
        post = PostModel.objects.get(id=post_id)
        comment = CommentModel.objects.get(post=post, id=comment_id)

        if comment.author == payload['username']:
            comment.delete()
            return Response(data={'message': '삭제가 되었습니다.'}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(data={'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class Search_REST(APIView):
    def get(self, request, format=None):
        print(12)

        data = {}
        post = PostModel.objects.all()
        print(123)
        user = usermodel.UserModel.objects.all()
        sear = request.GET.get('sear', '')

        PostSearch = post.filter(content__icontains=sear)

        UserSearch = user.filter(name__icontains=sear)

        serializer1 = serializers.SearchUser(UserSearch, many=True)
        serializer2 = serializers.SearchPost(PostSearch, many=True)

        print(serializer1.data)
        print(serializer2.data)

        return Response(data={'user': serializer1.data, 'post': serializer2.data})
