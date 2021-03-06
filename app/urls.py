from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('users/<uuid:chef_uuid>/confirm/<token>', views.confirmAccount, name='confirm-account'),
    path('users/<uuid:chef_uuid>/password-reset/<token>', views.passwordReset, name='password-reset'),
]
