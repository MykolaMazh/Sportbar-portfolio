from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category, Match


def index(request):
    return render(
        request,
        "base.html",
        {
            "categories": Category.objects.all(),
            "matches": Match.objects.all()
        }
    )

class CategoryDetailView(DetailView):
    model = Category