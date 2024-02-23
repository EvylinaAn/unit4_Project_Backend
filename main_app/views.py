from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from blog_app.models import Post, Category, Comment
from looks_app.models import Look, LooksCategory
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LookViewSet(viewsets.ModelViewSet):
    queryset = Look.objects.all()
    serializer_class = LookSerializer
    permission_classes = [permissions.IsAuthenticated]


class LooksCategoryViewSet(viewsets.ModelViewSet):
    queryset = LooksCategory.objects.all()
    serializer_class = LooksCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)


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