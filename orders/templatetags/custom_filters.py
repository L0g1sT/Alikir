import json

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    multiply_val = float(value) * float(arg)
    return "{:.2f}".format(multiply_val).replace('.', ',')


@register.filter
def to_float_td(value):
    try:
        float_value = float(value)
        return "{:.2f}".format(float_value).replace('.', ',')
    except ValueError:
        return ""


@register.filter
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return ""


@register.filter
def get_total_sum(basket_history):
    return sum(float(item['fields']['quantity']) * float(item['fields']['price']) for item in basket_history)


@register.filter
def jsonify_baskets(baskets):
    baskets_list = []
    for basket in baskets:
        product = basket.product
        basket_dict = {
            "model": "products.product",
            "pk": product.pk,
            "fields": {
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "quantity": basket.quantity,
                "image": product.image.url,
                "category": product.category.pk
            }
        }
        baskets_list.append(basket_dict)
    return json.dumps(baskets_list)


