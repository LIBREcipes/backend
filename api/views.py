from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer, RecipeIngredientSerializer
from .models import Recipe, Ingredient, RecipeIngredient


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecipeIngredientViewset(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer