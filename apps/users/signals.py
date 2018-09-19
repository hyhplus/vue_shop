# coding:utf-8 
# author: Evan
# datetime: 18-9-20 上午1:36

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    """
    django信号量的简单应用：遵循原来加密方式对密码加密
    """
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
