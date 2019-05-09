import datetime
from typing import List, Dict, Union

from django.contrib.auth.models import User

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
        "Lundi": {
            "date": None,
            "recipe": None
        },
        "Mardi": {
            "date": None,
            "recipe": None
        },
        "Mercredi": {
            "date": None,
            "recipe": None
        },
        "Jeudi": {
            "date": None,
            "recipe": None
        },
        "Vendredi": {
            "date": None,
            "recipe": None
        },
        "Samedi": {
            "date": None,
            "recipe": None
        },
        "Dimanche": {
            "date": None,
            "recipe": None
        }
    }
    for week_day, value in week_menu.items():
        week_menu[week_day]["recipe"] = get_specific_day_recipe_for_user(user, day)
        week_menu[week_day]["date"] = day
        day += datetime.timedelta(days=1)
    return week_menu


# def get_week_dates(week_menu: Dict[str, Union[Recipe, None]]) -> Dict[str, Union[str, datetime.date]]:
#     """
#     Returns a dict containing day names as key and their date correspondence as value
#     :param week_menu: dict return by get_this_week_menu function
#     """
#     week_days = {}
#     today = datetime.date.today()
#     day = today - datetime.timedelta(days=today.weekday())
#     for day_name, value in week_menu.items():
#         week_days[day_name] = day
#         day += datetime.timedelta(days=1)
#     return week_days
