from django.templatetags.l10n import register
from product_grocery.models import Product
from django import template


@register.filter()
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url


@register.filter()
def productname(pid):
    data = Product.objects.get(id=pid)
    return data.name


@register.filter()
def productprice(pid):
    data = Product.objects.get(id=pid)
    return data.price


@register.simple_tag()
def producttotalprice(pid, qty):
    data = Product.objects.get(id=pid)
    return int(qty) * int(data.price)


register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def sum_total(queryset):
    return sum(item.total for item in queryset)
