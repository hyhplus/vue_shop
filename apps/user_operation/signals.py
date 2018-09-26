# coding: utf-8
__author__ = 'Evan'

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfavs(sender, instance=None, created=False, **kwargs):
    """添加收藏"""
    if created:
        goods = instance.goods
        if goods.fav_num >= 0:
            goods.fav_num = goods.fav_num + 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfavs(sender, instance=None, created=False, **kwargs):
    """取消收藏"""
    goods = instance.goods
    goods.fav_num -= 1
    if goods.fav_num <=0:
        goods.fav_num = 0
    goods.save()