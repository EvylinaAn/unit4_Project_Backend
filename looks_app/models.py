from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class LooksCategory(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
    

class Look(models.Model):
    url = models.ImageField( max_length=254)
    description = models.CharField(max_length=100)
    categories = models.ManyToManyField(LooksCategory)

    def __str__(self):
        return self.description
    
    class Meta:
        ordering = ['-id']


