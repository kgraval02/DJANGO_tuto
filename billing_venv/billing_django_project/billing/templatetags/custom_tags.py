from django.templatetags.l10n import register
from product_grocery.models import Product


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
