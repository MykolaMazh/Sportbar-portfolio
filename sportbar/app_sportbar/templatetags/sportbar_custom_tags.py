from datetime import timedelta

from django import template

from app_sportbar.models import BookedTable

register = template.Library()


@register.filter
def duration_filter(date_time):
    _from = (date_time - timedelta(hours=1)).strftime("%Y %B %d %H:%M")
    to = (date_time + timedelta(hours=2)).strftime("%Y %B %d %H:%M")
    return f"{_from} - {to}"


@register.simple_tag(takes_context=True)
def booked_tables_quantity(context):
    request = context["request"]
    if request.user.is_authenticated:
        return BookedTable.objects.filter(client=request.user).count()
