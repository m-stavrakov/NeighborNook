from django.db import models
from django.contrib.auth.models import User 
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    category = models.ForeignKey(Category, related_name='events' ,on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name