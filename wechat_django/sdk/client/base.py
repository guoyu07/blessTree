# -*-coding:utf-8 -*-
__author__ = 'albert'

"""
    wechat api 基类
"""
import sys
import time
import inspect
import six
import json
import requests

from wechat_django.sdk.session.memorystorage import MemoryStorage


class BaseWeChatAPI(object):

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, client=None):
        self._client = client

    # def _get(self, url, params):
    #     res = requests.get(
    #         url=url,
    #         params=params
    #     )
    #     result = res.json()
    #
    #     return result['nickname'] + result['province']

    def _get(self, wechat_client, url, kwargs):
        # if getattr(self, 'API_BASE_URL', None):
        #     kwargs['api_base_url'] = self.API_BASE_URL
        # return wechat_client.get(url, **kwargs)
        return "lqczzz"

    # TODO:下面三个方法的修改
    def _post(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def session(self):
        return self._client.session


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatAPI)


class BaseWeChatClient(object):

    API_BASE_URL = ''

    def __new__(cls, *args, **kwargs):
        self = super(BaseWeChatClient, cls).__new__(cls)
        if sys.version_info[:2] == (2, 6):
            # Python 2.6 inspect.gemembers bug workaround
            # 参考http://bugs.python.org/issue1785
            for _class in cls.__mro__:
                if issubclass(_class, BaseWeChatClient):
                    for name, api in _class.__dict__.items():
                        if isinstance(api, BaseWeChatAPI):
                            api_cls = type(api)
                            api = api_cls(self)
                            setattr(self, name, api)
        else:
            api_endpoints = inspect.getmembers(self, _is_api_endpoint)
            for name, api in api_endpoints:
                api_cls = type(api)
                api = api_cls(self)
                setattr(self, name, api)
        return self

    def __init__(self, appid, access_token=None, session=None, timeout=None):
        self.appid = appid
        self.expires_at = None
        self.session = session or MemoryStorage()
        self.timeout = timeout

        if isinstance(session, six.string_types):
            pass

        self.session.set(self.access_token_key, access_token)

    @property
    def access_token_key(self):
        return '{0}_access_token'.format(self.appid)

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith('http://', 'https://'):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        # 群发消息上传接口集成
        if url.startswith('https://file.api.weixin.qq.com'):
            kwargs['verify'] = False

        if 'params' not in kwargs:
            kwargs['params'] = {}

        if isinstance(kwargs['params'], dict) and \
            'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token

        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        # res.raise_for_status() 异常抛出

        return self._handle_result(
            res, method, url, result_processor, **kwargs
        )

    def _decode_result(self, res):
        res.encoding = 'utf-8'
        result = res.json()
        return result

    def _handle_result(self, res, method=None, url=None,
                       result_process=None, **kwargs):
        if not isinstance(res, dict):
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        if 'base_resp' in result:
            result = result['base_resp']

        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result['errmsg']
            # 出错原因在于access_token时候的处理
            if errcode in (40001, 40014, 42001):
                self.fetch_access_token()
                access_token = self.session.get(self.access_token_key)
                kwargs['params']['access_token'] = access_token
                return self._request(
                    method=method,
                    url_or_endpoint=url,
                    result_process=result_process,
                    **kwargs
                )
            elif errcode == 45009:
                pass
            else:
                pass
            # 某些错误处理先不做

        return result if not result_process else result_process(result)

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    _get = get

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )
    _post = post

    def _fetch_access_token(self, url, params):
        """
        获取access_token 的方法
        :param url:
        :param params:
        :return:
        """
        res = requests.get(
            url=url,
            params=params
        )
        result = res.json()
        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            self.access_token_key,
            result['access_token']
        )
        self.session.set(
            'expires_in',
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        # return result

    def fetch_access_token(self):
        raise NotImplementedError()

    # @property
    def access_token(self):
        """
        wechat access_token
        :return:
        """
        access_token = self.session.get(self.access_token_key)

        if access_token:
            if not self.expires_at:
                return access_token

            timstamp = time.time()
            if self.expires_at-timstamp > 60:
                return access_token

        self.fetch_access_token()
        return self.access_token
        # return self.session.get(self.access_token_key)
        # if self.session.get(self.access_token_key)==None:
        #     return "lqczzz"


        # TODO session改为使用django自带的session来实现，暂时采用自己实现的session


