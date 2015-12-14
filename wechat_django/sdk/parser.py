# -*-coding:utf-8-*-
__author__ = 'albert'

"""
    wechat_django.sdk.parser:
    解析post过来的消息类型
    使用示范：
    if request.method == 'POST':
        parse_message(request.body)
"""
import xmltodict

from wechat_django.sdk.messages import MESSAGE_TYPES, UnknownMessage
from wechat_django.sdk.events import EVENT_TYPES
from wechat_django.sdk.utils import to_text

def parse_message(xml):
    """
        微信服务器推送过来的消息使用POST方法，消息内容是xml格式的内容
    :param xml: xml格式消息
    :return:消息类型或者事件类型
    """

    if not xml:
        return
    message = xmltodict.parse(to_text(xml))['xml']
    message_type = message['MsgType'].lower()
    if message_type in('event', 'device_event'):  # 若接收到事件推送
        event_type = message['Event'].lower()  # 事件类型

        if message_type =='device_event':  # 设备事件
            event_type ='device_{event}'.format(event=event_type)
        if event_type == 'subscribe' and message.get('EventKey'):
            event_type = 'subscribe_scan'
            message['Event'] = event_type
            message['EventKey'] = message['EventKey'].replace('qrscene_', '')
        message_class = EVENT_TYPES.get(event_type, UnknownMessage)
    else:
        message_class = MESSAGE_TYPES.get(message_type, UnknownMessage)
    return message_class(message)