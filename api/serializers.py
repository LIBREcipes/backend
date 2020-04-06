from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Ingredient, Recipe, RecipeIngredient, MyUser, RecipeStep



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('uuid', 'username', 'first_name', 'last_name', 'email')

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    class Meta:
        model = RecipeIngredient
        fields = ('__all__')

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ('__all__')

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source="recipeingredient_set", many=True)
    chef = UserSerializer(many=False)
    steps = StepSerializer(many=True, source='recipestep_set')
    class Meta:
        model = Recipe
        fields = ('__all__')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # del token['user_id']
        # token['uuid'] = str(user.uuid)

        return token