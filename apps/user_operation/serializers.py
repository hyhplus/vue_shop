# coding: utf-8
__author__ = 'Evan'

import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from MyShop.settings import REGEX_MOBILE
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    """
    默认的用户收藏的序列化
    """

    # 默认到当前用户 DRF官网:CurrentUserDefault
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="已收藏"
            )
        ]

        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 设置当天提交的时间 ready_only=True, 只返回不提交
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage

        fields = ("user", "message_type", "subject", "message", "add_time", "file", "id")


class AddressSerializer(serializers.ModelSerializer):
    """
    收货地址序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    def validated_mobile(self, signer_mobile):
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号非法")

        return signer_mobile

    # def validate_empty_values(self, signer_name):
    #     if signer_name == None:
    #         raise serializers.ValidationError("收件人非空")
    #     return signer_name

    class Meta:
        model = UserAddress
        # fields = "__all__"
        fields = ("id", "add_time", "user", "province", "city", "district",
                  "address", "signer_name", "signer_mobile")