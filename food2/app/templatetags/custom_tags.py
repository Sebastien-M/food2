from django import template
import datetime

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def recipe_date_str_to_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
