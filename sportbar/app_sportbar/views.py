from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from app_cart.forms import CartAddProductForm
from .forms import ClientCreationForm, BookedTableForm
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



class BookedTableCreateView(CreateView):
    form_class = BookedTableForm
    template_name = "app_sportbar/booked_table_form.html"
    success_url = reverse_lazy("sportbar:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            initial_data = {"match":self.kwargs["match_id"]}
            if self.request.user.is_authenticated:
                initial_data["client"] = self.request.user
            context["form"] = BookedTableForm(initial_data)
        return context

