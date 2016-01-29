# -*-coding:utf-8 -*-
from django.db import models

# Create your models here.

TYPE = {
    0: u'自己浇水',
    1: u'第一次分享朋友圈',
    2: u'添加新年愿望',
    3: u'别人浇水',
    4: u'成功添加一位好友',
    5: u'祝福',
    6: u'吐槽'
}


class User(models.Model):
    """
    用户类，主要是用户是否种树等，还有朋友关系
    """
    # 用户openid/头像/昵称/加入时间
    openid = models.CharField(max_length=100)
    nickname = models.CharField(max_length=40)
    avatar = models.ImageField()
    create_time = models.DateTimeField()  # 待定

    # 用户积分相关，方便逻辑判断
    if_plant = models.BooleanField()
    tree_name = models.CharField(max_length=40)
    if_share = models.BooleanField()
    willing = models.CharField(max_length=300, default='none')
    count = models.IntegerField()  # 积分

    # 用户关系
    friends = models.ManyToManyField("self")  # 朋友

    class Meta:
        ordering = ['count']  # 默认积分排行来存储
        verbose_name_plural = verbose_name = u"用户"


class Tree(models.Model):
    """
    树表，主要是保存树的名字，
    """
    # 基本信息
    owner = models.OneToOneField(User)
    tree_name = models.CharField(max_length=40)
    count = models.IntegerField()

    # 互动信息保存
    type = models.IntegerField(choices=TYPE.items(), verbose_name=u'操作类型')
    action_time = models.DateTimeField()
    read = models.BooleanField(default=False)  # 消息是否已读，默认还没有
    source_id = models.CharField(default='na', max_length=100)  # 默认na,匿名的意思
    content = models.CharField(max_length=300)  # 主要是祝福吐槽的内容

    class Meta:
        ordering = ['-action_time']  # 默认互动信息从最新开始
        verbose_name_plural = verbose_name = u"用户"