from django.urls import path


from app_cart.views import cart_add

app_name = 'cart'

urlpatterns = [
    path("add/<str:slug>/", cart_add, name="add-to-cart"),

]