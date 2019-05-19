import datetime
import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings

from app.models import DailyRecipe, Recipe
from app.utils import is_daily_recipe_defined_for_user, get_todays_recipe_for_user, get_specific_day_recipe_for_user


class UtilsTestCase(TestCase):
    fixtures = [os.path.join(settings.BASE_DIR, 'app/tests/app_fixtures.json')]

    def setUp(self):
        User.objects.create(username='test',
                            password='test',
                            email='test@test.com')
        User.objects.create(username='test2',
                            password='test2',
                            email='test2@test.com')

    def test_is_daily_recipe_defined_for_user_true(self):
        recipe = Recipe.objects.order_by("?").first()
        user = User.objects.get(username='test')
        DailyRecipe.objects.create(user=user, recipe=recipe, day=datetime.date.today())
        self.assertTrue(is_daily_recipe_defined_for_user(user))

    def test_is_daily_recipe_defined_for_user_false(self):
        recipe = Recipe.objects.order_by("?").first()
        user_one = User.objects.get(username='test')
        user_two = User.objects.get(username='test2')
        DailyRecipe.objects.create(user=user_one, recipe=recipe, day=datetime.date.today())
        self.assertFalse(is_daily_recipe_defined_for_user(user_two))

    def test_get_todays_recipe_for_user(self):
        recipe = Recipe.objects.order_by("?").first()
        user = User.objects.get(username='test')
        DailyRecipe.objects.create(user=user, recipe=recipe, day=datetime.date.today())
        self.assertEqual(get_todays_recipe_for_user(user), recipe)

    def test_get_todays_recipe_for_user_no_recipe_defined(self):
        user = User.objects.get(username='test')
        self.assertIsNone(get_todays_recipe_for_user(user))

    def test_get_specific_day_recipe_for_user(self):
        recipe = Recipe.objects.order_by("?").first()
        user = User.objects.get(username='test')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        DailyRecipe.objects.create(user=user, recipe=recipe, day=tomorrow)
        self.assertEqual(get_specific_day_recipe_for_user(user, tomorrow), recipe)

    def test_get_specific_day_recipe_for_user_wrong_day(self):
        recipe = Recipe.objects.order_by("?").first()
        user = User.objects.get(username='test')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        DailyRecipe.objects.create(user=user, recipe=recipe, day=tomorrow)
        self.assertIsNone(get_specific_day_recipe_for_user(user, datetime.date.today()))
