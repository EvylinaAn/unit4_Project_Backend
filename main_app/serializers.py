from django.contrib.auth.models import Group, User
from rest_framework import serializers
from blog_app.models import Post, Category, Comment
from looks_app.models import Look, LooksCategory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url' ,'title', 'content', 'categories']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['url', 'id', 'category', 'posts']

    def get_posts(self, obj):
        request = self.context.get('request')
        posts = Post.objects.filter(categories=obj)
        return PostSerializer(posts, many=True, context={'request': request}).data


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Look
        fields = '__all__'


class LooksCategorySerializer(serializers.HyperlinkedModelSerializer):
    looks = serializers.SerializerMethodField()

    class Meta:
        model = LooksCategory
        fields = ['url', 'id', 'category', 'looks']

    def get_looks(self, obj):
        request = self.context.get('request')
        looks = Look.objects.filter(categories=obj)
        return LookSerializer(looks, many=True, context={'request': request}).data

