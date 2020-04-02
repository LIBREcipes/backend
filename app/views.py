from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from core.models import Recipe, MyUser, Ingredient

def index(request):
    recipes = Recipe.objects.all()
    return render(
        request,
        'app/recipes/index.html',
        {
            'recipes': recipes,
        }
    )

def recipeDetail(request, recipe_uuid):
    recipe = get_object_or_404(Recipe, uuid=recipe_uuid)
    return render(
        request,
        'app/recipes/detail.html',
        {
            'recipe': recipe,
        }
    )


def chefDetail(request, chef_uuid):
    chef = get_object_or_404(MyUser, uuid=chef_uuid)
    return render(
        request,
        'app/chefs/detail.html',
        {
            'chef': chef,
        }
    )

def ingredientDetail(request, ingredient_uuid):
    ingredient = get_object_or_404(Ingredient, uuid=ingredient_uuid)
    return render(
        request,
        'app/ingredients/detail.html',
        {
            'ingredient': ingredient,
        },
    )