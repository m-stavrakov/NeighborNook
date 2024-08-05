from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserProfileView, CustomLoginView, custom_logout_view

app_name = "user"

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('signup/', views.signup, name='signup'),
]