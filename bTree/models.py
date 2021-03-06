# -*-coding:utf-8 -*-
from django.db import models
import time
# Create your models here.

TYPE = {
    0: u'自己浇水',
    1: u'第一次分享朋友圈',
    2: u'添加新年愿望',
    3: u'别人浇水',
    4: u'成功添加一位好友',
    5: u'祝福',
    6: u'吐槽',
    7: u'创建树木'
}


class User(models.Model):
    """
    用户类，主要是用户是否种树等，还有朋友关系
    """
    # 用户openid/头像/昵称/加入时间
    openid = models.CharField(max_length=50)  # 实际长为28
    nickname = models.CharField(max_length=20)  # 实际长为7个中文字符
    time_stamp = models.DateTimeField(auto_now_add=True)  # 待定
    avatar_url = models.CharField(max_length=300, blank=True)  # 这个只保存没有关注的用户的信息

    # 用户积分相关，方便逻辑判断exit
    # if_plant = models.BooleanField(default=)  # 没有种树就不要记录就好
    tree_name = models.CharField(max_length=40)
    is_plant = models.BooleanField(default=True)
    if_share = models.BooleanField(default=False)
    willing = models.CharField(max_length=300, default='none')  # 如果为none则没有填写willing，可以去填写啦啦啦
    count = models.IntegerField(default=0)  # 积分

    # 用户关系
    friends = models.ManyToManyField("self")  # 朋友

    class Meta:
        ordering = ['count']  # 默认积分排行来存储
        verbose_name_plural = verbose_name = u"用户"


class Tree(models.Model):
    """
    互动信息表，主要是保存互动信息，
    """
    # 基本信息
    owner = models.ForeignKey(User)
    tree_name = models.CharField(max_length=40)
    count = models.IntegerField(default=0)  # 这几积分没有用了

    # 互动信息保存
    type = models.IntegerField(choices=TYPE.items(), verbose_name=u'操作类型')
    action_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # 消息是否已读，默认还没有
    source_id = models.CharField(default='na', max_length=100)  # 默认na,匿名的意思
    content = models.CharField(max_length=300, blank=True)  # 主要是祝福吐槽的内容

    class Meta:
        ordering = ['-action_time']  # 默认互动信息从最新开始
        verbose_name_plural = verbose_name = u"用户"


