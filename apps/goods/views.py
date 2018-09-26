from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication

from goods.filters import GoodsFilter
from goods.serializers import GoodsSerializer, CategorySerializer
from goods.serializers import BannerSerializer, IndexCategorySerializer
from goods.models import Goods, Banner
from goods.models import GoodsCategory


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

    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListView(generics.ListAPIView):
    """
    商品列表页 ListAPIView  -->  test
    """

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


from rest_framework import mixins, viewsets
class GoodsAllViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    商品列表 ViewSet
    包括了分页，搜索，过滤，排序
    """

    '''
    # queryset = Goods.objects.all() 不设置排序会报下面的错误:
    UnorderedObjectListWarning: Pagination may yield inconsistent results 
    with an unordered object_list: <class 'goods.models.Goods'> QuerySet.
    '''
    # queryset = Goods.objects.get_queryset().order_by('id')
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # drf的token认证机制
    # authentication_classes = (TokenAuthentication,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('name', 'shop_price')

    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        """
        重写mixins.RetrieveModelMixin下retrieve()方法, 添加商品点击数
        """
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    list:   商品分类列表数据
    """

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:   获取轮播图列表
    """

    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:   首页商品系列数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品","酒水饮料","牛奶制品","海鲜水产"])
    serializer_class = IndexCategorySerializer