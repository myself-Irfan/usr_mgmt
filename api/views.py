import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import authenticate
from .models import Post
from .serializers import *
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# Create your views here.


class ObtainAuthTokenV(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            logger.info(f'User {username} successfully authenticated and obtained access token')
            return Response({'Access_Token': access_token}, status=status.HTTP_200_OK)
        else:
            logger.warning(f'Failed authentication attempt for user {username}. Invalid credentials provided')
            return Response({'Error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpV(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'User {request.data.get("username")} registered successfully')
        return Response({'Message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class HomeV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        if posts:
            logger.info(f'User {request.user.username} retrieved posts successfully')
            return Response({'Posts': serializer.data}, status=status.HTTP_200_OK)
        else:
            logger.info(f'User {request.user.username} attempted to retrieve posts but none available')
            return Response({'Message': 'No posts available'}, status=status.HTTP_204_NO_CONTENT)


class CreatePostV(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['author'] = request.user.id
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'User {request.user.username} created a new post')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeletePostV(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user or request.user.has_perm("main.delete_post"):
            post.delete()
            logger.info(f'User {request.user.username} deleted a post with ID {post_id}')
            return Response({'Message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        logger.warning(f'User {request.user.username} failed to delete a post with ID {post_id} but permission denied')
        return Response({'Message': 'Post not found or permission denied'}, status=status.HTTP_404_NOT_FOUND)
