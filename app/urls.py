from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.index, name='recipes'),
    path('recipes/<uuid:recipe_uuid>/', views.recipeDetail, name='recipe-detail'),

    path('chefs/<uuid:chef_uuid>/', views.chefDetail, name='chef-detail')
]
