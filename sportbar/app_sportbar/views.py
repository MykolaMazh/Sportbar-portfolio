from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from app_cart.forms import CartAddProductForm
from .forms import ClientCreationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_add_form"] = CartAddProductForm()
        return context

class ClientCreateView(CreateView):
    model = get_user_model()
    form_class = ClientCreationForm
    success_url = reverse_lazy("login")
