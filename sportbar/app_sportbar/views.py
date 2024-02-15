from django.shortcuts import render

from .models import Category


def index(request):
    print(Category.objects.all())
    return render(request, "app_sportbar/index.html", {"categories": Category.objects.all()})
