from rest_framework import serializers
from .models import Goods, GoodsCategory

# # Serializer方式
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#
#         :param validated_data:
#         :return:
#         """
#         return Goods.objects.create(**validated_data)


# ModelSerializer方式
"""
goods的外键category --> 直接嵌套展示category表中的字段
"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
    """
    list all goods
    """
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = '__all__'