# coding: utf-8
__author__ = 'Evan'

from django_filters import rest_framework as filters
from goods.models import Goods
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gt')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lt')
    top_category = filters.NumberFilter(method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = [ 'pricemin', 'pricemax', 'top_category']