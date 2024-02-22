from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
    
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
    

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