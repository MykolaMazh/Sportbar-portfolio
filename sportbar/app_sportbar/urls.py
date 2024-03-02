from django.urls import path
from .views import index, CategoryDetailView, ClientCreateView, BookedTableCreateView

app_name = "sportbar"

urlpatterns = [
    path('', index, name="home"),
    path("category_detail/<str:slug>", CategoryDetailView.as_view(), name="category_detail"),
    path("register/", ClientCreateView.as_view(), name="register"),
    path("booked_table/<int:match_id>", BookedTableCreateView.as_view(), name=" booked-table"),
    # path("booked_table/<int:match_id>", d, name=" booked-table"),

]
