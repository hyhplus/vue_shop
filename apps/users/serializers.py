# coding:utf-8 
# author: Evan
# datetime: 18-9-18 下午9:27

import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model

from MyShop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 手机是否注册，存在一条即存在
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号非法")

        # 验证码发送频率, 这里设置为60s
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 验证码频率的时间判断, add_time的时间大于60s
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码：",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 label="验证码",
                                 write_only=True,
                                 help_text="验证码")

    username = serializers.CharField(required=True, allow_blank=False, label="手机号码",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        if verify_records:
            last_record = verify_records[0]

            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago >= last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")