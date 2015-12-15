# -*-coding:utf-8-*-
__author__ = 'albert'
"""
    wechat_django.sdk.utils:
    一些有用的函数
"""

# from __future__ import absolute_import, unicode_literals
import string
import random
import hashlib
import six


class ObjectDict(dict):
    """
        重载字典类型
    """
    def __getattr__(self, item):
        if item in self:
            return self[item]
        return None

    def __setattr__(self, key, value):
        self[key] = value

class WeChatSigner(object):
    """WeChat data signer"""

    def __init__(self, delimiter=b''):
        self._data = []
        self._delimiter = to_binary(delimiter)

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = self._delimiter.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def check_signature(token, signature, timestamp, nonce):
    """Check WeChat callback signature, raises InvalidSignatureException
    if check failed.

    :param token: WeChat callback token
    :param signature: WeChat callback signature sent by WeChat server
    :param timestamp: WeChat callback timestamp sent by WeChat server
    :param nonce: WeChat callback nonce sent by WeChat sever
    """
    signer = WeChatSigner()
    signer.add_data(token, timestamp, nonce)
    if signer.signature != signature:
        # from wechatpy.exceptions import InvalidSignatureException
        #
        # raise InvalidSignatureException()
        return False
    return True
# class WeChatSigner(object):
#     """wechat 数据签名,用于微信与服务器验证校验 """
#     def __init__(self, delimiter=b''):
#         self._data = []
#         self._delimiter = to_binary(delimiter)
#
#     def add_data(self, *args):
#         """ 把数据加到singer上"""
#         for data in args:
#             self._data.append(to_binary(data))
#
#     @property  # 这个内置的装饰器可以让函数像属性一样访问：WeChatSignerObj.signature
#     def signature(self):
#         """得到数据签名 """
#         self._data.sort()
#         str_to_sign = self._delimiter.join(self._data)  # 将列表转化为字符串，为了给hashlib.sha1处理
#         return hashlib.sha1(str_to_sign).hexdigest()


def to_binary(value, encoding='utf-8'):
    """
        six.binary_type:主要是兼容python2的str()与python3的bytes()
        :param value:被转化的数据
        :param encoding:编码类型
    """
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


# def check_signature(token, signature, timestamp, nonce):
#     """ 检验微信服务器端回调过来的值
#         用于微信服务器端与本服务器端的链接验证
#
#     :param token:微信回调的token，你自己定义的
#     :param signature: 微信服务器生成的签名，在GET方法中可以得到
#     :param timestamp: 微信服务器生成的，在GET方法中可以得到
#     :param nonce: 微信服务器生成的，在GET方法中可以得到
#     :return:None
#     """
#
#     signer = WeChatSigner()
#     signer.add_data(token, timestamp, nonce)
#     if signer.signature != signature:
#         return False
#     return True


def to_text(value, encoding='unicode'):
    """ 将数据转换为文本，默认编码是unicode

    :param value: 被转换的数据
    :param encoding: 编码规则
    :return:text类型的数据
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def timezone(zone):
    """
        尝试获取时区
    :param zone: timezone str
    :return:timezone tzinfo 或者None
    """
    try:
        import pytz
        return pytz.timezone(zone)
    except ImportError:
        pass
    try:
        from dateutil.tz import gettz
        return gettz(zone)
    except ImportError:
        return None


def random_string(length=16):
    """
    截取随机的字符串并返回
    :param length: 返回字符串的长度
    :return:随机字符串
    """
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return ''.join(rand_list)











