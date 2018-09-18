# coding:utf-8 
# author: Evan
# datetime: 18-9-18 下午9:27

import re
from datetime import datetime, timedelta
from MyShop.settings import REGEX_MOBILE
from rest_framework import serializers
from django.contrib.auth import get_user_model
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