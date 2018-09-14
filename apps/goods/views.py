from django.shortcuts import render
from .models import Goods
from rest_framework.views import APIView
from .serializers import GoodsSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

# Create your views here.
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
#     商品列表
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

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表 ViewSet
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination