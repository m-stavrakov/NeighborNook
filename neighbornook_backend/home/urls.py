from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home_loggedin, name='home_loggedin'),
]