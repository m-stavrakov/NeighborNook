from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    path('category/<int:category_id>/', views.events_categories, name='events_categories'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('new_event/', views.new_event, name='new_event'),
    path('<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('search/', views.event_search, name='event_search'),
]