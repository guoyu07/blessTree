# -*-coding:utf-8-*-
# __author__ = 'albert'

"""
    微信服务器推送的普通消息类型
    参考：http://mp.weixin.qq.com/wiki/17/fc9a27730e07b9126144d9c96eaf51f9.html
"""

# from __future__ import absolute_import, unicode_literals
import copy
import six

from wechat_django.sdk.fields import (
    BaseField,
    StringField,
    IntegerField,
    DateTimeField,
    FieldDescriptor
)
from wechat_django.sdk.utils import to_binary, to_text

MESSAGE_TYPES = {}


def register_message(msg_type):
    """
    python装饰器，便于注册其他的普通消息类型
    :param msg_type:
    :return:
    """
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls
    return register


class MessageMetaClass(type):
    """ 所有消息类型的元类，元类：产生类的类
    """
    def __new__(cls, name, bases, attrs):
        for b in bases:
            if not hasattr(b, '_fields'):
                continue

            for k, v in b.__dict__.items():
                if k in attrs:
                    continue
                if isinstance(v, FieldDescriptor):
                    attrs[k] = copy.deepcopy(v.field)
        cls = super(MessageMetaClass.cls).__new__(cls, name, bases, attrs)
        cls._field = {}

        for name, field in cls.__dict__.items():
            if isinstance(field, BaseField):
                field.add_to_class(cls, name)
        return cls


class BaseMessage(six.with_metaclass(MessageMetaClass)):
    """
    所有基本消息类型与事件类型的基类
    """
    type = 'unknown'
    id = IntegerField('MsgId', 0)
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    create_time = DateTimeField('CreateTime')

    def __init__(self, message):
        self._data = message

    def __repr__(self):
        _repr = "{klass}({msg})".format(
            klass=self.__class__.__name__,
            mss=repr(self._data)
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)