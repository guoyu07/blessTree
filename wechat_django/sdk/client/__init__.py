# -*-coding:utf-8 -*-
__author__ = 'albert'

import time

from wechat_django.sdk.client.base import BaseWeChatAPI

class WeChatClient(BaseWeChatAPI):

    """
    微信api操作类，很多主动接口调用都需要的
    """

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

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

        return self._fetch_acess_token(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
        )