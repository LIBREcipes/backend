from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient



class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email',)

class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('__all__')

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientSerializer(many=True)
    chef = UserSerializer(many=False)
    class Meta:
        model = Recipe
        fields = ('__all__')