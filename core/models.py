import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

from django.db import models


def uuid_upload_to(instance, filename):
    _, extension = os.path.splitext(filename)
    return '{0}.{1}'.format(uuid4(), extension)

class MyUser(AbstractUser):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

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
    default_unit = models.CharField(max_length=8, null=True, blank=True)

    calories = models.IntegerField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    fat_saturated = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    carbs_sugar = models.FloatField(null=True, blank=True)
    proteine = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    name = models.CharField(max_length=256)
    chef = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    language = models.CharField(max_length=3, default='en')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=uuid_upload_to, null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=8)

    class Meta:
        unique_together = (("recipe", "ingredient",),)


class RecipeStep(models.Model):
    description = models.CharField(max_length=1024)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.SmallIntegerField()
    image = models.ImageField(upload_to=uuid_upload_to, null=True, blank=True)

    class Meta:
        unique_together = (("recipe", "step",),)
