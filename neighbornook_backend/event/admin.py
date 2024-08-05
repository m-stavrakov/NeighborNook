from django.contrib import admin
from . models import Event, EventImage, Category

admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(Category)