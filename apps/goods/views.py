from django.shortcuts import render
from goods.models import Goods
from rest_framework.views import APIView
from goods.serializers import GoodsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from goods.filters import GoodsFilter

"""
# django rest framework called by `DRF` later
Web browsable API
Serialization
CVA

pip install coreapi
pip install django-guardian
"""

# class GoodsListView(APIView):
#     """
#     商品列表页
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)

    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data) # drf封装get/post/body的请求的数据
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoodsPagination(PageNumberPagination):
    """
    商品列表分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListView(generics.ListAPIView):
    """
    商品列表页 ListAPIView  -->  test
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


from rest_framework import mixins, viewsets
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表 ViewSet
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter

    # filter_backends = (DjangoFilterBackend,)
    #filter_fields = ('name', 'shop_price')

    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset