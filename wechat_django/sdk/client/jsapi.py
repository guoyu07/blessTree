# -*-coding:utf-8 -*-
__author__ = 'albert'
"""
    wechat_django.sdk.client.jsapi
    提供一些操作jsSDK的的api
"""
import time

from wechat_django.sdk.utils import WeChatSigner
from wechat_django.sdk.client.base import BaseWeChatAPI


class WeChatJSAPI(BaseWeChatAPI):

    def get_ticket(self, type='jsapi'):
        """
        获取微信js-sdk的ticket
        :param type:
        :return:返回的json包
        """
        return self._get('get_jsapi_ticket')

    def get_jsapi_ticket(self):
        """
        获取微信js-sdk的ticket
        :return:ticket
        """
        ticket = self.session.get('jsapi_ticket')
        expires_in = self.session.get('jsapi_ticket_expires_at', 0)


