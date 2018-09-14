# coding: utf-8
__author__ = 'Evan'

from django_filters import rest_framework as filters
from goods.models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    price_min = filters.NumberFilter(field_name='shop_price', lookup_expr='gt')
    price_max = filters.NumberFilter(field_name='shop_price', lookup_expr='lt')

    class Meta:
        model = Goods
        fields = [ 'price_min', 'price_max']