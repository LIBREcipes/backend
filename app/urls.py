from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.index, name='recipes'),
    path('recipes/<uuid:recipe_uuid>/', views.recipeDetail, name='recipe-detail'),

    path('chefs/<uuid:chef_uuid>/', views.chefDetail, name='chef-detail'),

    path('ingredients/<uuid:ingredient_uuid>/', views.ingredientDetail, name='ingredient-detail'),

    path('login/', auth_views.LoginView.as_view(template_name='app/auth/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
]
