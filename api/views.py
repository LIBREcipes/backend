from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer, RecipeIngredientSerializer
from core.models import Recipe, Ingredient, RecipeIngredient, MyUser


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'uuid'
    # permission_classes = (IsAuthenticated,)

    


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'uuid'
    # permission_classes = (IsAuthenticated,)


class UserViewset(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    # permission_classes = (IsAuthenticated,)

class RecipeIngredientViewset(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    # permission_classes = (IsAuthenticated,)