from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ingredient, Recipe, Brand, RecipeIngredient, MyUser, RecipeStep, File
from .forms import RecipeForm


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    inlines = [
        RecipeStepInline,
        RecipeIngredientInline,
    ]

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('language',)}),
    )
    



admin.site.register(Ingredient)
admin.site.register(RecipeStep)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Brand)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(File)