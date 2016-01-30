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

    def get_ticket(self, wechat_client, type='jsapi'):
        """
        获取微信js-sdk的ticket
        :param type:
        :return:返回的json包
        """
        return self._get(
            wechat_client,
            'ticket/getticket',
            params={
                'access_token': wechat_client.fetch_access_token(),
                'type': type
            }
        )

    def get_jsapi_ticket(self, wechat_client):
        """
        获取微信 JS-SDK ticket

        该方法会通过 session 对象自动缓存管理 ticket

        :return: ticket
        """
        ticket = self.session.get('jsapi_ticket')
        expires_at = self.session.get('jsapi_ticket_expires_at', 0)
        if not ticket or expires_at < int(time.time()):
            jsapi_ticket = self.get_ticket(wechat_client, 'jsapi')
            ticket = jsapi_ticket['ticket']
            expires_at = int(time.time()) + int(jsapi_ticket['expires_in'])  # 保存过期事件
            self.session.set('jsapi_ticket', ticket)
            self.session.set('jsapi_ticket_expires_at', expires_at)
        return ticket

    def get_jsapi_signature(self, noncestr, ticket, timestamp, url):
        data = [
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'jsapi_ticket={ticket}'.format(ticket=ticket),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = WeChatSigner(delimiter=b'&')
        signer.add_data(*data)
        return signer.signature

