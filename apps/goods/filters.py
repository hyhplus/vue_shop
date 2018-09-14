# coding: utf-8
__author__ = 'Evan'

import django_filters
from goods.models import Goods


class GoodsFilter(django_filters.FilterSet):
    """
    商品的过滤类
    """
    price_min = django_filters.NumberFilter(lookup_expr='shop_price__gt')
    price_max = django_filters.NumberFilter(lookup_expr='shop_price__lt')

    class Meta:
        model = Goods
        fields = ['name','shop_price','price_min', 'price_max']