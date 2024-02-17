from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category, Match, Championship


def index(request):
    return render(
        request,
        "base.html",
        {
            "championships": Championship.objects.all(),
            "categories": Category.objects.all(),
            "matches": Match.objects.select_related("championship")
        }
    )

class CategoryDetailView(DetailView):
    model = Category