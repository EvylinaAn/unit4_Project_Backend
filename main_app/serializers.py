from django.contrib.auth.models import Group, User
from rest_framework import serializers
from blog_app.models import Post, Category, Comment, Photo, FeaturedPhoto
from looks_app.models import Look, LooksCategory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PhotoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Photo
        fields = ('id', 'url', 'post')
        

class FeaturedPhotoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = FeaturedPhoto
        fields = ('id', 'url', 'post')
        

class PostSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'content', 'categories', 'photos', 'created_at', 'comments']

    def get_categories(self, obj):
        return [category.category for category in obj.categories.all()]
    
    def get_photos(self, obj):
        photos_queryset = obj.photo_set.all() 
        photos_data = PhotoSerializer(photos_queryset, many=True).data
        return photos_data

    def get_comments(self, obj):
        request = self.context.get('request')
        comments_queryset = obj.comment_set.all() 
        comments_data = CommentSerializer(comments_queryset, many=True, context={'request': request}).data 
        return comments_data


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['url', 'id', 'category', 'posts']

    def get_posts(self, obj):
        request = self.context.get('request')
        posts = Post.objects.filter(categories=obj)
        return PostSerializer(posts, many=True, context={'request': request}).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['url', 'id', 'comment', 'post', 'owner', 'created_at' ]



class LooksCategorySerializer(serializers.HyperlinkedModelSerializer):
    looks = serializers.SerializerMethodField()

    class Meta:
        model = LooksCategory
        fields = ['url', 'id', 'category', 'looks']

    def get_looks(self, obj):
        request = self.context.get('request')
        looks = Look.objects.filter(categories=obj)
        return LookSerializer(looks, many=True, context={'request': request}).data


class LookSerializer(serializers.ModelSerializer):
    # categories = LooksCategorySerializer()
    
    class Meta:
        model = Look
        fields = ['url', 'id', 'description', 'categories']
