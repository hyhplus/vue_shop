"""MyShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import xadmin
from django.urls import path
from django.conf.urls import include, url
from django.views.static import serve
from MyShop.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsAllViewSet
from goods.views import CategoryViewSet
from goods.views import BannerViewSet
from goods.views import IndexCategoryViewSet
from trade.views import ShoppingCartViewSet
from trade.views import OrderViewSet
from trade.views import AliPayView
from users.views import SmsCodeViewSet
from users.views import UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet
from user_operation.views import AddressViewSet

router = DefaultRouter()

# 配置商品列表的路由
router.register(r'goods', GoodsAllViewSet, base_name="goods")

# 配置商品分类的路由
router.register(r'category', CategoryViewSet, base_name="category")

# 配置验证码的路由
router.register(r'code', SmsCodeViewSet, base_name="code")

# 配置用户登录路由
router.register(r'users', UserViewSet, base_name="users")

# 配置用户收藏的路由
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")

# 配置留言的路由
router.register(r'messages', LeavingMessageViewSet, base_name="messages")

# 配置收货地址的路由
router.register(r'address', AddressViewSet, base_name="address")

# 配置购物车的路由
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shopcarts")

# 配置订单相关的路由
router.register(r'orders', OrderViewSet, base_name="orders")

# 配置轮播图的路由
router.register(r'banners', BannerViewSet, base_name="banners")

# 配置首页商品类别的路由
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")

# goods_list = GoodsListViewSet.as_view({
#     'get': list,
# })

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 富文本框编辑, 用于xadmin/下 商品详情的编辑, 可以编辑图片
    path('ueditor/', include('DjangoUeditor.urls')),

    # DRF 后台登录 API 接口
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 处理图片显示的url,使用Django自带serve,
    # 传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # # 商品列表页
    # path('goods/', goods_list.as_view(), name="goods-list"),
    # 全局url的配置
    url(r'^', include(router.urls)),

    # DRF自动文档, 方便前后端交互的文档
    url(r'docs/', include_docs_urls(title="DRF SHOP DOCS")),

    # drf自带的登录注册验证, 生成token值
    url(r'^api-token-auth/', token_views.obtain_auth_token),

    # jwt的token认证, 验证jwt的token是否匹配
    url(r'^login/', obtain_jwt_token),

    # 支付宝返回接口
    url(r'alipay/return/', AliPayView.as_view(), name="alipay"),
]
