from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from app_cart.forms import CartAddProductForm
from .forms import ClientCreationForm, BookedTableForm
from .models import Category, Match, Championship, BookedTable


def index(request):
    return render(
        request,
        "base.html",
        {
            "championships": Championship.objects.all(),
            "categories": Category.objects.all(),
            "matches": Match.objects.select_related("championship"),
        },
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


class BookedTableCreateView(LoginRequiredMixin, CreateView):
    form_class = BookedTableForm
    template_name = "app_sportbar/booked_table_form.html"
    success_url = reverse_lazy("sportbar:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if BookedTable.objects.filter(
                match_id=self.kwargs["match_id"]
        ).count() < settings.MAX_BAR_CAPACITY:
            initial_data = {"match": self.kwargs["match_id"],
                            "client": self.request.user}
            context["form"] = BookedTableForm(initial_data)
        else:
            del context["form"]
            context["excess_error"] = "Everything is booked for this match."
        return context

    def post(self, request, *args, **kwargs):
        form = BookedTableForm(self.request.POST)
        if form.is_valid():
            booked_table = form.save()
            match = booked_table.match.title
            booked_time = booked_table.match.event_date
            before = timedelta(hours=1)
            after = timedelta(hours=2.5)
            return JsonResponse(
                {
                    "message": "success",
                    "match": match,
                    "from": (booked_time - before).strftime("%Y %B %d %H:%M"),
                    "to": (booked_time + after).strftime("%Y %B %d %H:%M"),
                },
                status=200,
            )
        else:
            return JsonResponse({"message": "error"}, status=400)


class BookedTableListView(LoginRequiredMixin, ListView):
    model = BookedTable
    template_name = "app_sportbar/booked_table_list.html"

    def get_queryset(self):
        return self.model.objects.filter(client=self.request.user)


class BookedTableUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedTable
    fields = ("match", "phone")
    template_name = "app_sportbar/booked_table_update.html"
    success_url = reverse_lazy("sportbar:home")

    def post(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.phone = self.request.POST.get("phone")
            self.object.match_id = self.request.POST.get("match")
            self.object.save()
        except IntegrityError:
            pass
        return redirect(reverse("sportbar:booked-table-list"))


class BookedTableDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedTable
    template_name = "app_sportbar/booked_table_delete.html"
    success_url = reverse_lazy("sportbar:booked-table-list")
