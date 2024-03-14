from django.urls import path
from .views import (
    index,
    CategoryDetailView,
    ClientCreateView,
    BookedTableCreateView,
    BookedTableListView,
    BookedTableUpdateView,
    BookedTableDeleteView,
)

app_name = "sportbar"

urlpatterns = [
    path("", index, name="home"),
    path(
        "categories/<str:slug>",
        CategoryDetailView.as_view(),
        name="category"
    ),
    path("register/", ClientCreateView.as_view(), name="register"),
    path(
        "booked_table/<int:match_id>",
        BookedTableCreateView.as_view(),
        name=" booked-table",
    ),
    path(
        "booked_table_list/",
        BookedTableListView.as_view(),
        name="booked-table-list"
    ),
    path(
        "booked_table_update/<int:pk>/",
        BookedTableUpdateView.as_view(),
        name="booked-table-update",
    ),
    path(
        "booked_table_delete/<int:pk>/",
        BookedTableDeleteView.as_view(),
        name="booked-table-delete",
    ),
]
