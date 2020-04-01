from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from api.models import Recipe, MyUser

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