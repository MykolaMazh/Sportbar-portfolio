from django.urls import path


from app_cart.views import cart_add, cart, cart_remove

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path("add/<int:id>/", cart_add, name="add-to-cart"),
    path("delete/<int:product_id>/", cart_remove, name="move-off-cart"),

]