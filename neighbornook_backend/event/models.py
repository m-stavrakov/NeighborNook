from django.db import models
from django.contrib.auth.models import User 
from PIL import Image

AGE_LIMIT_CHOICES = [
    (0, 'All Ages'),
    (13, '13+'),
    (18, '18+'),
    (21, '21+'),
    (50, '50+'),
]

WEATHER_CHOICES = [
    ('sunny', 'Sunny'),
    ('rainy', 'Rainy'),
    ('cloudy', 'Cloudy'),
    ('snowy', 'Snowy'),
    ('any', 'Any'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    age_limit = models.PositiveSmallIntegerField(choices=AGE_LIMIT_CHOICES, default=0)
    weather = models.CharField(max_length=100, choices=WEATHER_CHOICES, default='any')
    category = models.ForeignKey(Category, related_name='events' ,on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    what_to_bring = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_pics')

    def __str__(self):
        return f"{self.event.name} Image"