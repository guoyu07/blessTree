# -*-coding:utf-8 -*-
from wechat_django.sdk.client import WeChatClient
from wechat_django.sdk.oauth import WeChatOAuth


# 全局变量
# appId = 'wx96e5255e64f71a4d'
# appsecret = '04c6d39407f0e882bcf87f207758d0d5'
appId = 'wx02188968cc966e28'
appsecret = 'a805cf260cad4ee9be1aaaa073cb7902'
WEIXIN_TOKEN = 'weixin'

NONCESTR = 'Wm3WZYTPz0wzccnW'

# 获取access_token，定时刷新
client = WeChatClient(appId, appsecret)
jsapi_ticket = {'expires_in': 0}
oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')