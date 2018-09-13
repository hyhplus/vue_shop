from django.shortcuts import render
from .models import Goods
from rest_framework.views import APIView
from .serializers import GoodsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
# django rest framework:  DRF

"""
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
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination










