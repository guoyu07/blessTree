# -*-coding:utf-8 -*-
__author__ = 'albert'

import time

from wechat_django.sdk.client.base import BaseWeChatClient
from wechat_django.sdk.client.user import WeChatUser


class WeChatClient(BaseWeChatClient):

    """
    微信api操作类，很多主动接口调用都需要的
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    # 以下实现让具体功能类成为这个统一接口的属性，便于调用

    user = WeChatUser()

    def __init__(self, appid, secret, access_token=None, session=None, timeout=None):
        super(WeChatClient, self).__init__(
            appid, access_token, session, timeout
        )
        self.appid = appid
        self.secret = secret

    def fetch_access_token(self):
        """
        获取access-token
        http://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html
        :return:json数据包
        """

        return self._fetch_access_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )