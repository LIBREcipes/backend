from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'recipes', views.RecipeViewset)
router.register(r'ingredients', views.IngredientViewset)
router.register(r'user', views.UserViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

