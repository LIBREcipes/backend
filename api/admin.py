from django.contrib import admin
from .models import Ingredient, Recipe, Brand, RecipeIngredient
from .forms import RecipeForm


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    inlines = [
        RecipeIngredientInline,
    ]



admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Brand)