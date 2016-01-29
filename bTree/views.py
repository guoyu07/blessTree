# -*-coding:utf-8-*-
# python内置库
import hashlib
import json
# from lxml import etree


# Django 库文件
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from wechat_django.sdk.utils import check_signature
from wechat_django.sdk.parser import parse_message
from wechat_django.sdk.replies import TextReply
from wechat_django.sdk.client import WeChatClient
from wechat_django.sdk.oauth import WeChatOAuth
from wechat_django.sdk.client.user import WeChatUser

from wechat_django.sdk.client.user import WeChatUser
from wechat_django.sdk.utils import to_text
# Create your views here.

import json

appId = 'wx96e5255e64f71a4d'
appsecret = '04c6d39407f0e882bcf87f207758d0d5'
WEIXIN_TOKEN = 'weixin'


@csrf_exempt
def weixin_main(request):
    """
        微信接入验证(GET)
        微信正常接收信息(POST)
    """

    # 中文编码问题
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if request.method == 'GET':
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        if check_signature(token, signature, timestamp, nonce):
            return HttpResponse(echostr)
    else:
        msg = parse_message(request.body)  # request.body就是post的xml格式文件
        if msg.type == 'text':
            reply = TextReply()
            reply.source = msg.target
            reply.target = msg.source
            if msg.content == '祝福树':
                reply.content = 'http://1.blesstree.sinaapp.com/wechat/'
            elif msg.content == '我':
                client = WeChatClient(appId, appsecret)
                client.fetch_access_token()  # 这句话必须有，先获取接口api调用权限
                user = client.user.get(client, msg.source)  # TODO：这句话有问题，查看逻辑调用
                reply.content = user
            elif msg.content == '分享':
                oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/', "snsapi_userinfo")
                reply.content = oauth.authorize_url
            elif msg.content == "创建":
                client = WeChatClient(appId, appsecret)
                client.fetch_access_token()
                menu = client.menu.create(client, {
                    "button":[
                        {
                            "type": "click",
                            "name": u"今日歌曲",
                            "key": "V1001_TODAY_MUSIC"
                        },
                        {
                            "type": "click",
                            "name": u"歌手简介",
                            "key": "V1001_TODAY_SINGER"
                        },
                        {
                            "name": u"菜单",
                            "sub_button": [
                                {
                                    "type": "view",
                                    "name": u"搜索",
                                    "url": "http://www.soso.com/"
                                },
                                {
                                    "type": "view",
                                    "name": u"视频",
                                    "url": "http://v.qq.com/"
                                },
                                {
                                    "type": "click",
                                    "name": u"赞一下我们",
                                    "key": "V1001_GOOD"
                                }
                            ]
                        }
                    ]
                }
                )
                reply.content = menu

            else:
               reply.content = msg.content

        # 用户点击链接获取跳转测试
        # if msg.type == '':
        #     test(request)


            xml = reply.render()
            return HttpResponse(xml)


def main_page(request):
    return render_to_response('main.html', locals())


def test(request):
    reply = TextReply()
    reply.content = parse_message(request.body)
    return HttpResponse(reply.render())

