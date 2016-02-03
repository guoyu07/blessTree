# -*-coding:utf-8-*-

# Create your views here.
import hashlib
import json
import time

# Django 库文件

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie

# 我的wechat_django库
from wechat_django.sdk.utils import check_signature
from wechat_django.sdk.parser import parse_message
from wechat_django.sdk.replies import TextReply
from wechat_django.sdk.client import WeChatClient
from wechat_django.sdk.oauth import WeChatOAuth
from wechat_django.sdk import code_access_token, global_code

from bTree import appId, appsecret, WEIXIN_TOKEN, NONCESTR, TIMESTAMP, client, oauth
from bTree.models import User, Tree
from bTree.ajax_process import ajax_1, ajax_2, ajax_3, ajax_4, ajax_5, ajax_6, ajax_7, ajax_8, ajax_9, ajax_10, ajax_11

# client = WeChatClient(appId, appsecret)


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
                oauth_fir = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/first')
                reply.content = oauth_fir.authorize_url
            elif msg.content == "李启成爱地球":
                # client = WeChatClient(appId, appsecret)
                client.fetch_access_token()
                # oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
                menu = client.menu.create(client, {
                    "button": [
                        {
                            "type": "view",
                            "name": 'plant',
                            "url": oauth.authorize_url
                        },
                        {
                            "type": "click",
                            "name": 'click-me',
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

        if msg.type == 'event' and msg.event == 'unsubscribe':
            User.objects.get(openid=msg.source).is_plant = False  # 取消关注等于没有种树了

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
    # oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
    code = request.GET.get('code')  # 通过认证的code获取openid
    visit_index = request.GET.get('visit_index')
    return_openid = request.GET.get('return_openid')
    try:
        oauth.fetch_access_token(code)  # 包含获取用户信息的所有条件
    except KeyError:
        oauth.access_token = code_access_token[code]['access_token']
        oauth.open_id = code_access_token[code]['openid']
    try:
        user_db = User.objects.get(openid=oauth.open_id, is_plant=True)
    except ObjectDoesNotExist:
        user_db = 0

    # 如果数据库没有该open_id的记录的话
    if user_db == 0:
        first_outh = WeChatOAuth(appId, appsecret, "http://1.blesstree.sinaapp.com/wechat/first")
        first_plant_url = first_outh.authorize_url
        if visit_index and return_openid:
            visit = True
            return_url = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+return_openid)
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
        client.fetch_access_token()
        user_info = client.user.get(client, oauth.open_id)
        user_openid = oauth.open_id
        name = user_info['nickname']
        count = '0'
        imgUrl = avatar_addr = user_info['headimgurl']
        owner = User.objects.get(openid=user_openid)
        water_time = Tree.objects.filter(owner=owner, type=0 or 3).order_by('-action_time')[:1]
        tree_name = owner.tree_name
        # 分享的链接生成，别人点进去是一个get方法，同时，这个是经过转化的，就是加入认证的链接

        share_url = WeChatOAuth(appId, appsecret,
                                'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id).authorize_url
        add_friend_url = WeChatOAuth(appId, appsecret,
                                     'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id+'&add=yes')\
            .authorize_url

        return render_to_response('home.html', locals())


@csrf_exempt
def first(request):
    # oauth = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home')
    code = request.GET.get('code')  # 通过认证的code获取openid
    try:
        oauth.fetch_access_token(code)  # 包含获取用户信息的所有条件
    except KeyError:
        oauth.access_token = code_access_token[code]['access_token']
        oauth.open_id = code_access_token[code]['openid']

    user = 'http://1.blesstree.sinaapp.com/wechat/home/'+'?code='+code+'&state='
    # 以下信息是为了分享接口而使用的
    app_id = appId
    timestamp = TIMESTAMP
    noncestr = NONCESTR
    signature = share(user)['first']
    ticket = share(user)['second']

    # user_info = oauth.get_user_info(oauth.open_id) 这个是得不到user_info的，需要snsapi_userinfo才可以，尼玛
    # client.fetch_access_token()调用share()函数已经使用过，不会出现access_token非法的情况
    user_info = client.user.get(client, oauth.open_id)
    user_openid = oauth.open_id
    name = user_info['nickname']
    tree_name = name+'的树'
    count = '0'
    first_time = True  # 这里写如果是第一次种树，小部件需要引入的条件，配合模板if标签
    imgUrl = avatar_addr = user_info['headimgurl']
    # share_url = 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id
    try:
        owner = User.objects.get(openid=user_openid)
        tree = Tree.objects.filter(owner=owner, type=0 or 3).order_by('-action_time')
        water_time = tree[:1]*1000
    except ObjectDoesNotExist:
        water_time = 0

    share_url = WeChatOAuth(appId, appsecret,
                                 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id).authorize_url
    add_friend_url = WeChatOAuth(appId, appsecret,
                                 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id).authorize_url

    #  用户第一次进去种树了，返回去的时候会返回到前面的页面，所以需要再判断一次,如果已经点进去还点进去，需要修改条件
    try:
        user_db = User.objects.get(openid=oauth.open_id)
        count = user_db.count
        first_time = False  # 这里写如果是第一次种树，小部件需要引入的条件，配合模板if标签
    except ObjectDoesNotExist:
        user_db = 0

    return render_to_response('home.html', locals())


def visit(request):
    """
    处理访问别人的主页的逻辑
    :param request:
    :return:
    """
    sourceid = request.GET.get('openid', '')
    oauth_vis = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+sourceid)
    error = False
    try:
        owner_info = client.user.get(client, sourceid)
        owner = owner_info['nickname']
        avatar = owner_info['headimgurl']
        owner_db = User.objects.get(openid=sourceid)
        count = owner_db.count
        tree_name = owner_db.tree_name
    except KeyError:
        error = True
    code = request.GET.get('code', '')
    try:
        oauth_vis.fetch_access_token(code)
    except KeyError:
        oauth_vis.access_token = code_access_token[code]['access_token']
        oauth_vis.open_id = code_access_token[code]['openid']

    try:
        flip_id = openid = oauth_vis.open_id
    except AttributeError:
        flip_id = openid = code_access_token[code]['openid']
    try:
        user = User.objects.get(openid=openid, is_plant=True)
    except ObjectDoesNotExist:
        user = 0

    if user is not 0:
        # 用户已经中树，因为只有关注用户才能种树，不关注用户只能评论吐槽
        my_zone_url = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home/').authorize_url
        return render_to_response('visit.html', locals())

    # 用户没有种树,点击按钮都会跳到认证链接来获取信息，获取的信息要保存
    my_zone_url = WeChatOAuth(appId, appsecret,
                              'http://1.blesstree.sinaapp.com/wechat/home/'+"?visit_index='123'"+'return_openid'+sourceid)\
        .authorize_url
    if request.GET.get('add'):
        friendship = User(openid=oauth_vis, nickname='na', time_stamp=time.time(), tree_name='na', is_plant=False)
        source_fr = User.objects.get(openid=sourceid)
        friendship.friends.add(source_fr)  # 保存朋友关系，只是此时保存的关系的友人尚未种树
        friendship.save()
    return render_to_response('visit.html', locals())


@ensure_csrf_cookie
def ajax_distribute(request):
    """
    分发所有ajax请求的函数
    请求码类型：
    ajax_type{
        '1': 第一次种树填入树名字时候保存到数据库
        '2': 主页面， 请求刷新排行榜的时候
        '3': 主页面， 请求刷新消息的时候
        '4': 请求提交浇水获取的积分的时候
        '5': 主页面和访问页面 请求刷新祝福的时候
        '6': 主页面和访问页面 请求刷新吐槽的时候
        '7': 主页面和访问页面 请求刷新心愿的时候
        '8': 主页面， 请求提交输入心愿的时候
        '9': 访问页面， 祝福提交请求
        '10': 访问页面， 吐槽提交请求
        '11': 第一次分享朋友圈增加积分的请求，添加好友不需要ajax请求增加积分
              因为会在对方注册使用的时候发送一个json来同时增加双方的分数与建立朋友关系
        '12'： 预留备用的

    }
    :param request: 含有ajax请求数据的请求对象
    :return:response，含有一个ret值
    ret值声明：1--成功 2--失败
    """
    ajax_type = request.POST.get('ajax_type', '')
    try:
        {
            '1': ajax_1,
            '2': ajax_2,
            '3': ajax_3,
            '4': ajax_4,
            '5': ajax_5,
            '6': ajax_6,
            '7': ajax_7,
            '8': ajax_8,
            '9': ajax_9,
            '10': ajax_10,
            '11': ajax_11,
        }[ajax_type](request)
    except KeyError:
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        ret = '2'  # 返回错误码
        response.write(ret)
        return response


# 一些实用的方法
def share(url):
    """

    :param url:当前网页的URL，就是要提供分享接口的页面的
    :return:签名，用于生成页面签名
    """
    client.fetch_access_token()
    ticket = client.jsapi.get_jsapi_ticket(client)
    return {"first": client.jsapi.get_jsapi_signature(NONCESTR, ticket, TIMESTAMP, url), "second": ticket}



