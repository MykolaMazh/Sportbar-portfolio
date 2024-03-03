from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def duration_filter(date_time):
    _from = (date_time - timedelta(hours=1)).strftime("%Y %B %d %H:%M")
    to = (date_time + timedelta(hours=2)).strftime("%Y %B %d %H:%M")
    return f"{_from} - {to}"