from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from core.models import Recipe, MyUser, Ingredient
from .forms import LoginForm

def index(request):
    return recipeIndex(request)

def recipeIndex(request):
    recipes = Recipe.objects.filter(Q(is_public=True) | Q(chef__username=request.user.username))
    return render(
        request,
        'app/recipes/index.html',
        {
            'recipes': recipes,
        }
    )

def recipeDetail(request, recipe_uuid):
    recipe = get_object_or_404(Recipe, uuid=recipe_uuid)

    if not recipe.is_public and recipe.chef.uuid != request.user.uuid:
        raise PermissionDenied
        
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

def logout(request):
    return auth_views.logout_then_login(request, login_url='/')