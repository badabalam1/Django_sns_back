from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from . import serializers
from .models import *
from post import models as Post
import jwt

# JWT settings파일에서 필요한 부분 가져오기
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_payload(request):
    token = request.META['HTTP_AUTHORIZATION']
    payload = jwt.decode(token, settings.SECRET_KEY)
    return payload


class UserPage(APIView):

    def get(self, request, user_id, format=None):

        payload = jwt_payload(request)

        user = get_object_or_404(UserModel, id=user_id)

        serializer = serializers.UserLoginSerializer(user)

        userJson = {}
        userJson = serializer.data
        userJson['postCount'] = Post.PostModel.objects.filter(
            user_id=user_id).count()
        follow = []
        s = ''
        a = user.get_followers()

        ad = user.follows.filter(username=payload['username'])

        result = user.followed_to.filter(username=payload['username'])

        if(result):
            userJson['result'] = True
        else:
            userJson['result'] = False

        userJson['followers'] = user.get_followers().count()
        userJson['following'] = user.get_followings().count()

        return Response(data=userJson, status=status.HTTP_200_OK)


# 로그인
class UserLogin(APIView):
    def get(self, request, fromat=None):
        payload = jwt_payload(request)

        user = UserModel.objects.get(username=payload['username'])

        serializer = serializers.UserLoginSerializer(user)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        print(request.data)

        try:
            username = request.data['username']
            password = request.data['password']

            user = UserModel.objects.get(
                username=username, password=password)
            if user:
                try:
                    serializer = serializers.UserLoginSerializer(user)
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['token'] = token

                    return Response(data={'user': serializer.data, 'token': user_details}, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
            else:
                res = {
                    'message': '아이디 혹은 비밀번호가 잘못되었습니다.'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        except UserModel.DoesNotExist:
            res = {'error': '아이디 혹은 비밀번호가 잘못되었습니다.'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)


# 회원가입
class UserRegister(APIView):
    def get(self, request, format=None):
        user = UserModel.objects.all()

        serializer = serializers.UserGetSerializer(
            user, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = serializers.UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'restul': '이미 가입된 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class PasswordChange(APIView):
    def put(self, request, format=None):
        # 토큰 decode을 통해 유저 확인
        payload = jwt_payload(request)
        user = UserModel.objects.get(
            username=payload['username'], password=request.data['password'])
        serializer = serializers.PasswordChangeSerializer(
            user)

        # 기존 비밀번호와 변경할 비밀번호를 비교해 지금 비밀번호와 같은 지 확인
        if serializer.data['password'] == request.data['newPassword']:
            return Response(data={'message': '기존 비밀번호와 동일합니다.'})
        else:
            user.password = request.data['newPassword']
            user.save()
            return Response(data={'message': '비밀번호가 변경되었습니다.'})


# 팔로우
class Follow(APIView):

    # permission_classes = (IsAuthenticated,)
    def get_object(self, id):
        return get_object_or_404(UserModel, id=id)

    def post(self, request, user_id, format=None):
        payload = jwt_payload(request)
        print(self.get_object(user_id))
        if UserModel.follow_to(self.get_object(payload['user_id']), self.get_object(user_id)):
            return Response(data={'result': True}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': '에러가 발생했습니다.'}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, user_id, format=None):
        payload = jwt_payload(request)

        if UserModel.unfollow_to(self.get_object(payload['user_id']), self.get_object(user_id)):
            return Response(data={'result': False}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': '에러가 발생했습니다.'}, status=status.HTTP_409_CONFLICT)


class Following(APIView):

    def get(self, request, user_id, format=None):

        account = get_object_or_404(UserModel, id=user_id)
        followers = account.get_followings()

        serializer = serializers.FollowSerializer(
            followers, many=True, context={'request': request})
        return Response(data=serializer.data)


class Followers(APIView):

    def get(self, request, user_id, format=None):

        account = get_object_or_404(UserModel, id=user_id)
        followers = account.get_followers()

        serializer = serializers.FollowSerializer(
            followers, many=True, context={'request': request})
        return Response(data=serializer.data)
