# -*-coding:utf-8 -*-
__author__ = 'albert'
"""
    sdk.fields:定义一些对分析微信消息有用的描述(Field)
    参考：http://mp.weixin.qq.com/wiki/17/fc9a27730e07b9126144d9c96eaf51f9.html
"""

# from __future__ import absolute_import, unicode_literals
import time
from datetime import datetime
import base64
import copy

import six
from wechat_django.sdk.utils import to_binary, to_text, ObjectDict, timezone

default_timezone = timezone('Asia/Shanghai')


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.attr_name = field.name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            value = instance._data.get(self.attr_name)
            if value is None:
                value = copy.deepcopy(self.field.default)
                instance._data[self.attr_name] = value
            if isinstance(value, dict):
                value = ObjectDict(value)
            if value and not isinstance(value, (dict, list, tuple)) and six.callable(self.field.converter):
                value = self.field.converter(value)
            return value
        return self.field

    def __set__(self, instance, value):
        instance._data[self.attr_name] = value


class BaseField(object):
    converter = None  # 转换

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def to_xml(self, value):
        raise NotImplementedError()

    def __repr__(self):
        _repr = '{klass}({name})'.format(
            klass=self.__class__.__name__,
            name=repr(self.name)
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def add_to_class(self, klass, name):
        self.klass = klass
        klass._fields[name] = self
        setattr(klass, name, FieldDescriptor(self))


class StringField(BaseField):

    def __to_text(self, value):
        return to_text(value)

    converter = __to_text

    def to_xml(self, value):
        value = self.converter(value)
        tpl = '<{name}><![CDATA[{value}]]></{name}>'
        return tpl.format(name=self.name, value=value)


class IntegerField(BaseField):
    converter = int

    def to_xml(self, value):
        value = self.converter(value) if value is not None else self.default
        tpl = '<name>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class DateTimeField(BaseField):
    converter = float

    def to_xml(self, value):
        value = time.mktime(datetime.timetuple(value))
        value = int(value)
        tpl = '<name>{value}</{name}>'
        return tpl.format(name=self.name, value=value)


class FloatField(BaseField):
    converter = float

    def to_xml(self, value):
        value = self.converter(value)
        tpl = """<Image>
            <MediaId><![CDATA[{value}]]></MediaId>
        </Image>"""
        return tpl.format(value=value)


class VoiceField(StringField):

    def to_xml(self, value):
        value = self.converter(value)
        tpl = """<Image>
            <MediaId><![CDATA[{value}]]></MediaId>
        </Image>"""
        return tpl.format(value=value)


class VideoField(StringField):

    def to_xml(self, value):
        media_id = self.converter(value['media_id'])
        if 'title' in value:
            title = self.converter(value['title'])
        if 'description' in value:
            description = self.converter(value['description'])
        tpl = """<Video>
        <MediaId><![CDATA[{media_id}]]></MediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        </Video>"""
        return tpl.format(
            media_id=media_id,
            title=title,
            description=description
        )


class Base64EncodeField(StringField):

    def __base64_encode(self, value):
        return to_text(base64.encode(to_binary(value)))

    converter = __base64_encode


class Base64DecodeField(StringField):

    def __base64_decode(self, value):
        return to_text(base64.decode(to_binary(value)))

    converter = __base64_decode


# 其他类型以后再写
# class MusicField(StringField):
#
#     def to_xml(self, value):
#         thumb_media_id = self.converter(value['thumb_media_id'])
#         if 'title' in value:
#             title = self.converter(value['title'])
#         if 'description' in value:











































