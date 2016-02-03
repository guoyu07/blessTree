# -*-coding:utf-8 -*-
__author__ = 'albert'

"""
    wechat_django.oauth.py:用户点击链接获取用户信息
"""
import json
import six
import requests
import time
from wechat_django.sdk.session.memorystorage import MemoryStorage

from  wechat_django.sdk import global_code


class WeChatOAuth(object):
    """
    微信公众平台网页授权
    """
    API_BASE_URL = 'https://api.weixin.qq.com/'
    OAUTH_BASE_URL = 'https://open.weixin.qq.com/connect/'

    def __init__(self, app_id, secret, redirect_uri, scope='snsapi_base', state=''):
        """
        参阅：http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html
        :param app_id:公众号的唯一标志
        :param secret: 这个是认证用的，获取网页授权的access_token
        :param redirect_uri:授权后重定向的回调链接
        :param scope:应用授权作用域
        :param state:重定向后带上的参数
        :return:
        """
        self.app_id = app_id
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    def _get(self, url, params):
        res = requests.get(
            url=self.API_BASE_URL + url,
            params=params
        )
        return res.json()

    @property
    def authorize_url(self):
        """
        生成认证链接
        :return:认证链接
        """
        redirect_uri = six.moves.urllib.parse.quote_plus(self.redirect_uri)
        url_list = [
            self.OAUTH_BASE_URL,
            'oauth2/authorize?appid=',
            self.app_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=',
            self.scope
        ]
        if self.state:
            url_list.extend(['&state=', self.state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    @property
    def qrconnect_url(self):
        """
        产生qrconnect url
        :return:url
        """
        redirect_uri = six.moves.urllib.parse.quote_plus(self.redirect_uri)
        url_list = [
            self.OAUTH_BASE_URL,
            'qrconnect?appid=',
            self.app_id,
            '&redirect_uri=',
            redirect_uri,
            '&response_type=code&scope=',
            'snsapi_login'  # scope
        ]
        if self.state:
            url_list.extend(['&state=', self.state])
        url_list.append('#wechat_redirect')
        return ''.join(url_list)

    @property
    def access_token_key(self):
        return '{0}_access_token_key'.format(self.app_id)

    def _fetch_access_token(self, code):
        """
        获取网页oauth的access_token
        :param code: url的参数
        :return:json
        """
        res = self._get(
            'sns/oauth2/access_token',
            params={
                'appid': self.app_id,
                'secret': self.secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )

        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        return res


    def fetch_access_token(self, code):
        """
        对外接口
        :return:
        """
        # 防止微信客户端重复多次使用code导致的bug
        if code in global_code:
            if global_code[code] > 0:
                global_code[code] = global_code[code]-1
                return self.access_token
            else:
                del global_code[code]
        else:
            global_code[code] = 3
            return self._fetch_access_token(code)


    def refresh_access_token(self, refresh_token):
        """
        refresh oauth2 access_token
        :param refresh_token: oauth2 access_token
        :return:json
        """
        res = self._get(
            'sns/oauth2/refresh_token',
            params={
                'appid': self.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        self.access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.expires_in = res['expires_in']
        return res

    def get_user_info(self, openid=None, access_token=None, lang='zh_CN'):
        """
        获取用户信息
        :param openid:
        :param access_token:
        :param lang:
        :return:
        """
        # openid = openid or self.open_id
        # access_token = access_token or self.session.get(self.access_token_key)
        # return self._get(
        #     'sns/userinfo',
        #     params={
        #         'access_token': access_token,
        #         'openid': openid,
        #         'lang': lang
        #     }
        # )
        openid = openid or self.open_id
        # access_token = access_token or self.session.get(self.access_token_key)
        access_token = access_token or self.access_token
        return self._get(
            'sns/userinfo',
            params={
                'access_token': access_token,
                'openid': openid,
                'lang': lang
            }
        )


    def check_access_token(self, openid=None, access_token=None):
        """
        access_token 的有效性
        :param openid:
        :param access_token:
        :return:
        """
        openid = openid or self.open_id
        access_token = access_token or self.access_token
        res = self._get(
            'sns/auth',
            params={
                'access_token': access_token,
                'openid': openid
            }
        )
        if res['errcode'] == 0:
            return True
        return False

























