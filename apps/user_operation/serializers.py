# coding: utf-8
__author__ = 'Evan'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav


class UserFavSerializer(serializers.ModelSerializer):

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
