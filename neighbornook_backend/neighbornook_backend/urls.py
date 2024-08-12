from django.contrib import admin
from django.urls import path, include
from user.views import (CustomPasswordResetView, CustomPasswordResetDoneView,
                    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('communication/', include('communication.urls')),
    path('event/', include('event.urls')),
    path('user/', include('user.urls')),
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='user/password_reset.html'
        ), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'
        ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'
        ),name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'
        ), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)