from rest_framework import permissions
from django.contrib.auth.models import Group
from products.models import Product


def check_permission_product_group(user):
    array = []
    group_all = user.request.user.groups.all()
    for group in group_all:
        for product in Product.objects.all():
            for product_group in product.product_group.all():
                if product_group == group:
                    array.append(product.id)
    queryset = Product.objects.filter(id__in=array)
    return queryset


