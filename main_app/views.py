from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, parsers
from rest_framework.views import APIView
from blog_app.models import Post, Category, Comment, Photo, FeaturedPhoto
from looks_app.models import Look, LooksCategory
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view
import uuid
import os
# import boto3

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({
      'username' : user.username,
      'email' : user.email,
      'id': user.id
    })


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
    

class PhotoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


class FeaturedPhotoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FeaturedPhoto.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def create_comment(request, *args, **kwargs):
        print(request)
        post_id = kwargs.get('pk')
        user_id = request.user.id
        user = User.objects.get(id=user_id)  
        post = Post.objects.get(pk=post_id)
        comment_text = request.data.get('comment_text')
        comment = Comment.objects.create(post=post, comment_text=comment_text, user=user)
        return Response({'message': 'Comment created successfully'})
    

class LookViewSet(viewsets.ModelViewSet):
    queryset = Look.objects.all()
    serializer_class = LookSerializer


class LooksCategoryViewSet(viewsets.ModelViewSet):
    queryset = LooksCategory.objects.all()
    serializer_class = LooksCategorySerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
