from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def cart_length(context):
    request = context["request"]
    cart = request.session.get("cart")
    if cart:
        return sum(item["quantity"] for item in cart.values())
