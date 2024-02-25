from django.urls import path


from app_cart.views import cart_add, cart

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path("add/<int:id>/", cart_add, name="add-to-cart"),

]