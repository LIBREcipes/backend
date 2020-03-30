from uuid import uuid4
from django.contrib.auth.models import User

from django.db import models


class Brand(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    name = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, default='en')
    barcode = models.IntegerField(null=True, blank=True)

    calories = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    carbs = models.IntegerField(null=True, blank=True)
    proteine = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    name = models.CharField(max_length=256)
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    language = models.CharField(max_length=3, default='en')
    steps = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=8)

    class Meta:
        unique_together = (("recipe", "ingredient",),)