from django.urls import path
from .views import index, CategoryDetailView, ClientCreateView

app_name = "sportbar"

urlpatterns = [
    path('', index, name="home"),
    path("category_detail/<str:slug>", CategoryDetailView.as_view(), name="category_detail"),
    path("register/", ClientCreateView.as_view(), name="register"),

]