# -*- coding: utf-8 -*-
"""
    wechatpy.replies
    ~~~~~~~~~~~~~~~~~~
    This module defines all kinds of replies you can send to WeChat

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import time
import six

from wechat_django.sdk.fields import(
    StringField,
    IntegerField,
)
from wechat_django.sdk.messages import BaseMessage, MessageMetaClass
from wechat_django.sdk.utils import to_text, to_binary


REPLY_TYPES = {}


def register_reply(reply_type):
    def register(cls):
        REPLY_TYPES[reply_type] = cls
        return cls
    return register


class BaseReply(six.with_metaclass(MessageMetaClass)):
    """Base class for all replies"""
    source = StringField('FromUserName')
    target = StringField('ToUserName')
    time = IntegerField('CreateTime', time.time())
    type = 'unknown'

    def __init__(self, **kwargs):
        self._data = {}
        message = kwargs.pop('message', None)
        if message and isinstance(message, BaseMessage):
            if 'source' not in kwargs:
                kwargs['source'] = message.target
            if 'target' not in kwargs:
                kwargs['target'] = message.source
            if hasattr(message, 'agent') and 'agent' not in kwargs:
                kwargs['agent'] = message.agent
        if 'time' not in kwargs:
            kwargs['time'] = time.time()
        for name, value in kwargs.items():
            field = self._fields.get(name)
            if field:
                self._data[field.name] = value
            else:
                setattr(self, name, value)

    def render(self):
        """Render reply from Python object to XML string"""
        tpl = '<xml>\n{data}\n</xml>'
        nodes = []
        msg_type = '<MsgType><![CDATA[{msg_type}]]></MsgType>'.format(
            msg_type=self.type
        )
        nodes.append(msg_type)
        for name, field in self._fields.items():
            value = getattr(self, name, field.default)
            node_xml = field.to_xml(value)
            nodes.append(node_xml)
        data = '\n'.join(nodes)
        return tpl.format(data=data)

    def __str__(self):
        if six.PY2:
            return to_binary(self.render())
        else:
            return to_text(self.render())


@register_reply('text')
class TextReply(BaseReply):
    """
    文本回复
    详情请参阅 http://mp.weixin.qq.com/wiki/9/2c15b20a16019ae613d413e30cac8ea1.html
    """
    type = 'text'
    content = StringField('Content')

def create_reply(reply, message=None, render=False):
    """
    Create a reply quickly
    """
    r = None
    if isinstance(reply, BaseReply):
        r = reply
        if message:
            r.source = message.target
            r.target = message.source
    elif isinstance(reply, six.string_types):
        r = TextReply(
            message=message,
            content=reply
        )
    # elif isinstance(reply, (tuple, list)):
    #     if len(reply) > 10:
    #         raise AttributeError("Can't add more than 10 articles"
    #                              " in an ArticlesReply")
    #     r = ArticlesReply(
    #         message=message,
    #         articles=reply
    #     )
    if r and render:
        return r.render()
    return r

