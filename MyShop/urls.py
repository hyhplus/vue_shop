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
from django.urls import path
from django.conf.urls import include, url
import xadmin
from django.views.static import serve
from MyShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)     # 配置goods的url路由

# goods_list = GoodsListViewSet.as_view({
#     'get': list,
# })

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    # drf 后台登录
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 处理图片显示的url,使用Django自带serve,
    # 传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),


    # # 商品列表页
    # path('goods/', goods_list.as_view(), name="goods-list"),

    url(r'^', include(router.urls)),

    # DRF自动文档
    url(r'docs/', include_docs_urls(title="drf电商系统")),
]
