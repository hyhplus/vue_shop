from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from random import choice

from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from MyShop.settings import API_KEY

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个， get只能有一个
            user = User.objects.get(Q(username=username)|Q(mobile=username))

            # django的后台中密码加密的，所以不能password==password
            # UserProfile继承的AbstractUser中有
            # def check_password(self, raw_password)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """

    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        """

        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """
        重写CreateModelMixin的create方法
        """

        # serializer这两个配置直接使用CreateModelMixin的create()的
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(API_KEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status = status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status = status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """

    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    # 登录验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 设置动态序列化
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    # 设置动态权限配置, 用户注册无需判断登录状态
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        # 重写CreateModelMixin的create()方法

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 用于返回当前用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save()
