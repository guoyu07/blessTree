# -*-coding:utf-8-*-

# Create your views here.
import hashlib
import json
import time

# Django 库文件

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie

# 我的wechat_django库
from wechat_django.sdk.utils import check_signature
from wechat_django.sdk.parser import parse_message
from wechat_django.sdk.replies import TextReply
from wechat_django.sdk.client import WeChatClient
from wechat_django.sdk.oauth import WeChatOAuth

from bTree.access import appId, appsecret, WEIXIN_TOKEN, NONCESTR, TIMESTAMP
from bTree.models import User, Tree

client = WeChatClient(appId, appsecret)

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
            # 消息自动回复
            if msg.content == '我':
                client.fetch_access_token()  # 这句话必须有，先获取接口api调用权限
                user = client.user.get(client, msg.source)
                reply.content = user['nickname']
            elif msg.content == '分享':
                oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/first')
                reply.content = oauth.authorize_url
            elif msg.content == "李启成爱地球":
                # client = WeChatClient(appId, appsecret)
                client.fetch_access_token()
                oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
                menu = client.menu.create(client, {
                    "button": [
                        {
                            "type": "view",
                            "name": 'plant',
                            "url": oauth.authorize_url
                        },
                        {
                            "type": "click",
                            "name": "about",
                            "key": "v1002"
                        }
                    ]
                }
                )
                reply.content = menu
            else:
                reply.content = msg.content
            xml = reply.render()
            return HttpResponse(xml)
        # 事件处理：关注事件|点击按钮推送|
        if msg.type == 'event' and msg.event == 'subscribe':
            reply = TextReply()
            reply.source = msg.target
            reply.target = msg.source
            reply.content = "欢迎关注华工创维俱乐部，我们将不定期推送新鲜有趣的福利哦～"

            xml = reply.render()
            return HttpResponse(xml)

        if msg.type == 'event' and msg.event == 'click':
            reply = TextReply()
            reply.source = msg.target
            reply.target = msg.source
            reply.content = "小编冬眠ing～"

            xml = reply.render()
            return HttpResponse(xml)


@csrf_exempt
def home(request):
    """
    处理进入自己的主页或者第一次使用引导种树的逻辑
    :param request:
    :return:
    """
    oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
    code = request.GET.get('code')  # 通过认证的code获取openid
    oauth.fetch_access_token(code)  # 包含获取用户信息的所有条件
    try:
        user_db = User.objects.get(openid=oauth.open_id)
    except ObjectDoesNotExist:
        user_db = 0

    # if request.GET.get('state') == '1':
    #     # user = 'http://1.blesstree.sinaapp.com/wechat/home/'+'?code='+code+'&state='
    #     # # 以下信息是为了分享接口而使用的
    #     # app_id = appId
    #     # timestamp = TIMESTAMP
    #     # noncestr = NONCESTR
    #     # signature = share(user)['first']
    #     # ticket = share(user)['second']
    #     return render_to_response('hello.html', locals())

    # 如果数据库没有该open_id的记录的话
    if user_db == 0:
        first_outh = WeChatOAuth(appId, appsecret, "http://1.blesstree.sinaapp.com/wechat/first")
        first_plant_url = first_outh.authorize_url
        return render_to_response('index.html', locals())
    else:
        user = 'http://1.blesstree.sinaapp.com/wechat/home/'+'?code='+code+'&state='
        # 以下信息是为了分享接口而使用的
        app_id = appId
        timestamp = TIMESTAMP
        noncestr = NONCESTR
        signature = share(user)['first']
        ticket = share(user)['second']

        # user_info = oauth.get_user_info(oauth.open_id) 这个是得不到user_info的，需要snsapi_userinfo才可以，尼玛
        user_info = client.user.get(client, oauth.open_id)
        user_openid = oauth.open_id
        name = user_info['nickname']
        count = '0'
        avatar_addr = user_info['headimgurl']
        share_url = 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id

        return render_to_response('home.html', locals())


# TODO:跳转链接生成失败原因
@csrf_exempt
def first(request):
    oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
    code = request.GET.get('code')  # 通过认证的code获取openid
    oauth.fetch_access_token(code)  # 包含获取用户信息的所有条件

    user = 'http://1.blesstree.sinaapp.com/wechat/home/'+'?code='+code+'&state='
    # 以下信息是为了分享接口而使用的
    app_id = appId
    timestamp = TIMESTAMP
    noncestr = NONCESTR
    signature = share(user)['first']
    ticket = share(user)['second']

    # user_info = oauth.get_user_info(oauth.open_id) 这个是得不到user_info的，需要snsapi_userinfo才可以，尼玛
    user_info = client.user.get(client, oauth.open_id)
    user_openid = oauth.open_id
    name = user_info['nickname']
    count = ''
    avatar_addr = user_info['headimgurl']
    # 保存用户信息使用ajax异步发送过去
    # user_save = User(openid=user_info['openid'], nickname=user_info['nickname'], timestamp=time.time(), )
    share_url = 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id
    first_time = True  # 这里写如果是第一次种树，小部件需要引入的条件，配合模板if标签
    return render_to_response('home.html', locals())


def visit(request):
    """
    处理访问别人的主页的逻辑
    :param request:
    :return:
    """
    pass


@ensure_csrf_cookie
def ajax_handle(request):
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    user_name = request.POST.get('nickname', '')
    tree_name = request.POST.get('tree_name', '')
    ret = '0'
    if user_id and user_name:
        user = User(openid=user_id, nickname=user_name, time_stamp=time.time(), tree_name='test')
        user.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def test(request, params):
    test_p = params['openid']
    return render_to_response('test.html', locals())


def test2(request):
    openid = request.GET['openid']
    return render_to_response('test2.html', locals())


def share(url):
    """

    :param url:当前网页的URL，就是要提供分享接口的页面的
    :return:签名，用于生成页面签名
    """
    client.fetch_access_token()
    ticket = client.jsapi.get_jsapi_ticket(client)
    return {"first": client.jsapi.get_jsapi_signature(NONCESTR, ticket, TIMESTAMP, url), "second": ticket}



