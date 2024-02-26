from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils import timezone

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
    

class Photo(models.Model):
    url = models.ImageField(upload_to="add_photo/", max_length=254)
    # url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.post_id


class Comment(models.Model):
    comment = models.TextField(max_length=300)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-comment']

