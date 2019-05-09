import datetime
from typing import List, Dict, Union

from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from app.models import DailyRecipe, Recipe


def is_daily_recipe_defined_for_user(user: User) -> bool:
    """
    Checks if a DailyRecipe instance is defined today for a user
    """
    return DailyRecipe.objects.filter(user=user, day=datetime.date.today()).exists()


def get_todays_recipe_for_user(user: User) -> Recipe:
    """
    Returns today's recipe for a user
    """
    daily_recipe = DailyRecipe.objects.get(user=user, day=datetime.date.today())
    return daily_recipe.recipe


def get_specific_day_recipe_for_user(user: User, day: datetime.date) -> Union[Recipe, None]:
    recipe = DailyRecipe.objects.filter(user=user, day=day)
    if recipe.exists():
        return recipe.get().recipe
    else:
        return None


def format_recipe_steps(recipe: Recipe) -> str:
    return recipe.steps.replace(';', '\n\n')


def get_this_week_menu(user: User) -> Dict[str, Dict[str, Union[str, Recipe, datetime.date, None]]]:
    today = datetime.date.today()
    # Here is the date from monday of this week
    day = today - datetime.timedelta(days=today.weekday())
    week_menu = {
        _("Lundi"): {
            "date": None,
            "recipe": None
        },
        _("Mardi"): {
            "date": None,
            "recipe": None
        },
        _("Mercredi"): {
            "date": None,
            "recipe": None
        },
        _("Jeudi"): {
            "date": None,
            "recipe": None
        },
        _("Vendredi"): {
            "date": None,
            "recipe": None
        },
        _("Samedi"): {
            "date": None,
            "recipe": None
        },
        _("Dimanche"): {
            "date": None,
            "recipe": None
        }
    }
    for week_day, value in week_menu.items():
        week_menu[week_day]["recipe"] = get_specific_day_recipe_for_user(user, day)
        week_menu[week_day]["date"] = day
        day += datetime.timedelta(days=1)
    return week_menu
