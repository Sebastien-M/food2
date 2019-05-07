from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    steps = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    recipe = models.ManyToManyField(Recipe, related_name='ingredients', through='IngredientRecipe')

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    class Meta:
        db_table = 'app_ingredient_recipe'

    def __str__(self):
        return '{} - {}'.format(self.recipe.name, self.ingredient.name)

    ingredient = models.ForeignKey(Ingredient, on_delete='cascade')
    recipe = models.ForeignKey(Recipe, on_delete='cascade', related_name='ingredient_quantity')
    quantity = models.FloatField(blank=True, null=True)


class DailyRecipe(models.Model):
    class Meta:
        unique_together = (('user', 'day'),)
    user = models.ForeignKey(User, related_name='daily_recipe', on_delete='cascade')
    day = models.DateField(default=timezone.now, db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete='cascade', related_name='daily_recipe', unique=False, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, str(self.day))


class ShoppingListItem(models.Model):
    user = models.ForeignKey(User, related_name='shopping_list', on_delete='cascade')
    ingredient = models.CharField(max_length=255)
    quantity = models.CharField(max_length=10, null=True, blank=True)
    bought = models.BooleanField(default=False, blank=True, null=True)
