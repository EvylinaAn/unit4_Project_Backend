from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils import timezone
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
      

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})
    
    class Meta:
        ordering = ['-created_at']
    

class Photo(models.Model):
    url = models.ImageField( max_length=254)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo url: {self.url}"
    
    class Meta:
        verbose_name_plural = 'photos'

class FeaturedPhoto(models.Model):
    url = models.ImageField( max_length=254)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo url: {self.url}"
    
    class Meta:
        verbose_name_plural = 'photos'



class Comment(models.Model):
    created_at  = models.DateTimeField('comment added', default=timezone.now)
    updated_at = models.DateTimeField('last modified', auto_now=True)
    comment = models.TextField(max_length=300)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-id']

