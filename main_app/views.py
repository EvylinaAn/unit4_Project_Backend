from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from blog_app.models import Post, Category, Comment, Photo
from looks_app.models import Look, LooksCategory
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view
import uuid
import os
import boto3

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)


@api_view(['POST'])
def add_photo(request, post_id):
    if request.method == 'POST':
        photo_file = request.FILES.get('photo-file', None)
        print(photo_file)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"/{os.environ['S3_BASE_URL']}{bucket}/{key}"
                photo_data = {'url': url, 'post': post_id}
                serializer = PhotoSerializer(data=photo_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
                return Response({'error': 'An error occurred uploading file to S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LookViewSet(viewsets.ModelViewSet):
    queryset = Look.objects.all()
    serializer_class = LookSerializer
    permission_classes = [permissions.IsAuthenticated]


class LooksCategoryViewSet(viewsets.ModelViewSet):
    queryset = LooksCategory.objects.all()
    serializer_class = LooksCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# class HomeView(APIView):
#    permission_classes = (IsAuthenticated, )
#    def get(self, request):
#        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
#        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.body["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    