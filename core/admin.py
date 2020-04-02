from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ingredient, Recipe, Brand, RecipeIngredient, MyUser, RecipeStep
from .forms import RecipeForm


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep

class RecipeAdmin(admin.ModelAdmin):
    # form = RecipeForm
    inlines = [
        RecipeStepInline,
        RecipeIngredientInline,
    ]



admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Brand)
admin.site.register(MyUser, UserAdmin)