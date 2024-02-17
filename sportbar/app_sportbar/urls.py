from django.urls import path
from .views import index, CategoryDetailView

app_name = "app_sportbar"

urlpatterns = [
    path('', index, name="home"),
    path("category_detail/<str:slug>", CategoryDetailView.as_view(), name="category_detail"),
]