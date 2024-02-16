from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category


def index(request):
    return render(
        request,
        "base.html",
        {
            "categories": Category.objects.all()
        }
    )

class CategoryDetailView(DetailView):
    model = Category