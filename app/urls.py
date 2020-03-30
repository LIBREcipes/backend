from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<uuid:recipe_uuid>/', views.recipeDetail, name='recipe-detail'),
]
