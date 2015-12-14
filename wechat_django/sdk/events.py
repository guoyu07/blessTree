# -*-coding:utf-8 -*-
__author__ = 'albert'
"""
    wechat_django.sdk.event:
    包含所有微信回调的事件，这是事件推送
    参考：http://mp.weixin.qq.com/wiki/14/f79bdec63116f376113937e173652ba2.html
"""

from __future__ import absolute_import, unicode_literals

from wechat_django.sdk.fields import (
    BaseField,
    StringField,
    FloatField,
    IntegerField,
    DateTimeField,
    Base64DecodeField
)
from wechat_django.sdk.messages import BaseMessage

EVENT_TYPE = {}


def register_event(event_type):
    """
    注册事件类,使用了python装饰器
    :param event_type:Event type
    :return:
    """
    def register(cls):
        EVENT_TYPE[event_type] = cls
        return cls
    return register


class BaseEvent(BaseMessage):
    """
    所有事件的基类
    """
    type = 'event'
    event = ''


@register_event('subscribe')
class SubscribeEvent(BaseEvent):
    """
        用户关注事件
        参阅：http://mp.weixin.qq.com/wiki/14/f79bdec63116f376113937e173652ba2.html#.E5.85.B3.E6.B3.A8.2F.E5.8F.96.E6.B6.88.E5.85.B3.E6.B3.A8.E4.BA.8B.E4.BB.B6
    """
    event = 'subscribe'


@register_event('unsubscribe')
class UnsubscribeEvent(BaseEvent):
    """
        用户取消关注事件
        参阅：上
    """
    event = 'unsubscribe'


@register_event('subscribe_scan')
class SubscribeScanEvent(BaseEvent):
    """
        用户扫描二维码关注事件
    """
    event = 'subscribe_scan'
    scene_id = StringField('EventKey')
    ticket = StringField('Ticket')


@register_event('click')
class ClickEvent(BaseEvent):
    """
        点击菜单拉取消息事件
    """
    event = 'click'
    key = StringField('EventKey')


@register_event('view')
class ViewEvent(BaseEvent):
    """
        点击菜单跳转链接事件
    """
    event = 'view'
    url = StringField('EventKey')

















