from django.shortcuts import render

from datetime import datetime
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from MyShop.settings import private_key_path, ali_pub_key_path
from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from trade.serializers import ShoppingCartSerializer
from trade.serializers import ShopCartDetailSerializer
from trade.serializers import OrderSerializer, OrderDetailSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods

# Create your views here.

class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list:       获取购物车详情
    create:     加入购物车
    delete:     删除购物车
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        """商品加入购物车，库存相应减少"""
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        """商品移除购物车，库存增加"""
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        """修改购物车商品数量，影响相应的商品库存量"""
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:       列出个人订单
    create:     添加个人订单
    delete:     删除个人订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取用户购物车的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()

        return order


class AliPayView(APIView):
    """
    支付宝接口
    """
    # notify_url 异步请求, POST方式返回
    # return_url 同步请求, GET 方式返回

    def get(self, request):
        """
        支付宝GET接口, 处理return_url
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("self", None)

        alipay = AliPay(
            appid="201608060018695",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,

            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=ali_pub_key_path,
            debug=True,     # 默认False
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")

    def post(self, request):
        """
        支付宝POST接口, 处理notify_url
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("self", None)

        alipay = AliPay(
            appid="201608060018695",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,

            # 支付宝的公钥，验证支付宝回传消息使用
            alipay_public_key_path=ali_pub_key_path,
            debug=True,     # 默认False
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)

            for existed_order in existed_orders:

                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods

                    # 销售量的统计
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")