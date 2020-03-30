from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from api.models import Recipe

# Create your views here.
def index(request):
    recipes = get_list_or_404(Recipe)
    return render(
        request,
        'app/index.html',
        {
            'recipes': recipes,
        }
    )

def recipeDetail(request, recipe_uuid):
    recipe = get_object_or_404(Recipe, uuid=recipe_uuid)
    return render(
        request,
        'app/recipe_detail.html',
        {
            'recipe': recipe,
        }
    )