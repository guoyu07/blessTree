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

from bTree import appId, appsecret, WEIXIN_TOKEN, NONCESTR, client, oauth, jsapi_ticket
from bTree.models import User, Tree
from bTree.ajax_process import ajax_1, ajax_2, ajax_3, ajax_4, ajax_5, \
    ajax_6, ajax_7, ajax_8, ajax_9, ajax_10, ajax_11, ajax_12


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
                            "name": u'中文',
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
            user = User.objects.get(openid=msg.source)
            user.is_plant = False  # 取消关注等于没有种树了
            user.save()

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
            return_url = WeChatOAuth(appId, appsecret,
                                     'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+return_openid)\
                .authorize_url
        return render_to_response('index.html', locals())
    else:
        user = 'http://1.blesstree.sinaapp.com/wechat/home/'+'?code='+code+'&state='
        # 以下信息是为了分享接口而使用的
        app_id = appId
        timestamp = int(time.time())
        noncestr = NONCESTR
        signature = share(user, timestamp)['first']
        ticket = share(user, timestamp)['second']

        # user_info = oauth.get_user_info(oauth.open_id) 这个是得不到user_info的，需要snsapi_userinfo才可以，尼玛
        client.fetch_access_token()
        user_info = client.user.get(client, oauth.open_id)
        user_openid = oauth.open_id
        name = user_info['nickname']
        count = User.objects.get(openid=user_openid).count
        count_bar = count/3000
        imgUrl = avatar_addr = user_info['headimgurl']
        owner = User.objects.get(openid=user_openid)
        # water_time = time.mktime(Tree.objects.filter(
        #     owner=owner, type=7).order_by('action_time')[0].action_time.timetuple())+28800  # 时区差别
        water_time = int(time.time())
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

    user = 'http://1.blesstree.sinaapp.com/wechat/first'+'?code='+code+'&state='
    # 以下信息是为了分享接口而使用的
    app_id = appId
    timestamp = int(time.time())
    noncestr = NONCESTR
    signature = share(user, timestamp)['first']
    ticket = share(user, timestamp)['second']

    # user_info = oauth.get_user_info(oauth.open_id) 这个是得不到user_info的，需要snsapi_userinfo才可以，尼玛
    # client.fetch_access_token()调用share()函数已经使用过，不会出现access_token非法的情况
    user_info = client.user.get(client, oauth.open_id)
    user_openid = oauth.open_id
    name = user_info['nickname']
    tree_name = name+'的树'
    count = 0
    count_bar = 0
    first_time = True  # 这里写如果是第一次种树，小部件需要引入的条件，配合模板if标签
    imgUrl = avatar_addr = user_info['headimgurl']

    water_time = int(time.time())

    share_url = WeChatOAuth(appId, appsecret,
                                'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id).authorize_url
    add_friend_url = WeChatOAuth(appId, appsecret,
                                     'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+oauth.open_id+'&add=yes')\
        .authorize_url

    #  用户第一次进去种树了，返回去的时候会返回到前面的页面，所以需要再判断一次,如果已经点进去还点进去，需要修改条件
    try:
        user_db = User.objects.get(openid=oauth.open_id, is_plant=True)
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
    high_verify = request.GET.get('state', '')
    if high_verify == 'high_verify':
        oauth_vis = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+sourceid)
    else:
        oauth_vis = WeChatOAuth(appId, appsecret,
                                'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+sourceid,
                                scope='snsapi_userinfo',
                                state='high_verify')

    # 这里是防止用户种树后取消关注了(不种树了)老的链接被别人点进去了
    error = False
    try:
        client.fetch_access_token()
        owner_info = client.user.get(client, sourceid)
        owner = owner_info['nickname']
        avatar = owner_info['headimgurl']
        owner_db = User.objects.get(openid=sourceid)
        # 获取最近一次浇水事件，没有浇过水就是创建树木时间，所以一定会有的，而且是访问的，一定有种树了
        # if owner_db.tree_set.filter(type=0) or owner_db.tree_set.filter(type=3):
        #     owner_tree = owner_db.tree_set.filter(type=3)[0] or owner_db.tree_set.filter(type=0)[0]
        #     # water_time = int(owner_tree.action_time.timestamp())
        # else:
        #     owner_tree = owner_db.tree_set.filter(type=7)[0]
        #     # water_time = int(owner_tree.action_time.timestamp())
        water_time = 0  # TODO:时间转化问题
        count = owner_db.count
        count_bar = count/3000
        tree_name = owner_db.tree_name
    except KeyError:
        error = True
    code = request.GET.get('code', '')

    # ios系统返回按钮出现的bug的解决方法
    try:
        oauth_vis.fetch_access_token(code)
    except KeyError:
        oauth_vis.access_token = code_access_token[code]['access_token']
        oauth_vis.open_id = code_access_token[code]['openid']

    try:
        flip_id = openid = oauth_vis.open_id
    except AttributeError:
        flip_id = openid = code_access_token[code]['openid']
    # 经过高级用户认证后的访问就有了获取头像与昵称的能力
    flip_nickname = False
    if high_verify == 'high_verify':
        flip_user = oauth_vis.get_user_info(openid=flip_id, access_token=oauth_vis.access_token)
        flip_nickname = flip_id['nickname']
        flip_avatar = flip_id['headimgurl']
        flip_nickname = True
    else:
        # TODO：这里是没有关注公众号的时候用户点进去，想祝福/吐槽/浇水/的时候
        try:
            client.fetch_access_token()
            user_from_wechat = client.user.get(client, flip_id)
            flip_nickname = user_from_wechat['nickname']
            flip_avatar = user_from_wechat['headimgurl']
        except AttributeError:
            flip_nickname = False
            # 获取一个高级认证作为点击浇水/祝福/吐槽事件的跳转链接，认证之后回调到原来的位置
            btn_redirect_url = WeChatOAuth(appId, appsecret,
                                           'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+sourceid,
                                           scope='snsapi_userinfo',
                                           state='high_verify').authorize_url

    try:
        user = User.objects.get(openid=openid, is_plant=True)
    except ObjectDoesNotExist:
        user = 0

    if user is not 0:
        # 用户已经中树，因为只有关注用户才能种树，不关注用户只能评论吐槽,但是朋友关系要保存
        try:
            user.friends.get(openid=sourceid)
        except ObjectDoesNotExist:
            user.friends.add(User.objects.get(openid=sourceid))
            user.save()
            msg = Tree(owner=owner_db, tree_name=owner_db.tree_name, type=4, action_time=time.time(),
                           read=False, source_id=user.openid, content='成功添加好友'+user.nickname)
            msg.save()
        my_zone_url = WeChatOAuth(appId, appsecret, 'http://1.blesstree.sinaapp.com/wechat/home/').authorize_url
        return render_to_response('visit.html', locals())

    # 用户没有种树,点击按钮都会跳到认证链接来获取信息，获取的信息要保存
    my_zone_url = WeChatOAuth(appId, appsecret,
                              'http://1.blesstree.sinaapp.com/wechat/home/'+"?visit_index='123'&return_openid="+sourceid)\
        .authorize_url
    if request.GET.get('add') and flip_nickname:  # 通过点击别人分享进去的都需要保存，这里互动了的
        try:
            friendship = User.objects.get(openid=oauth_vis.open_id)
            friendship.nickname = flip_nickname
            friendship.avatar_url = flip_avatar
            friendship.save()
        except ObjectDoesNotExist:
            friendship = User(openid=oauth_vis.open_id, nickname=flip_nickname, avatar_url=flip_avatar, time_stamp=time.time(), tree_name='na', is_plant=False)
            friendship.save()
            source_fr = User.objects.get(openid=sourceid)
            friendship.friends.add(source_fr)  # 保存朋友关系，只是此时保存的关系的友人尚未种树
            friendship.save()
    elif request.GET.get('add'):  # 通过点击别人分享进去的都需要保存,这里用户只是点击进去过没有互动
        try:
            friendship = User.objects.get(openid=oauth_vis.open_id)
            friendship.nickname = flip_nickname
            friendship.avatar_url = flip_avatar
            friendship.save()
        except ObjectDoesNotExist:
            friendship = User(openid=oauth_vis.open_id, nickname='na', time_stamp=time.time(), tree_name='na', is_plant=False)
            friendship.save()
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
    response = HttpResponse()

    # 最不情愿写的代码
    if ajax_type == '1':
        return ajax_1(request)
    elif ajax_type == '2':
        return ajax_2(request)
    elif ajax_type == '3':
        return ajax_3(request)
    elif ajax_type == '4':
        return ajax_4(request)
    elif ajax_type == '5':
        return ajax_5(request)
    elif ajax_type == '6':
        return ajax_6(request)
    elif ajax_type == '7':
        return ajax_7(request)
    elif ajax_type == '8':
        return ajax_8(request)
    elif ajax_type == '9':
        return ajax_9(request)
    elif ajax_type == '10':
        return ajax_10(request)
    elif ajax_type == '11':
        return ajax_11(request)
    elif ajax_type == '12' or ajax_type == '13':
        return ajax_12(request)
    else:
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        ret = '2'  # 返回错误码
        response.write(ret)
    # return response
    # name_dict = {"twz": "Love python and Django", "zqxt": "I am teaching Django"}
    # return JsonResponse(name_dict)


# 一些实用的方法
def share(url, timstamp):
    """

    :param url:当前网页的URL，就是要提供分享接口的页面的
    :return:签名，用于生成页面签名
    """
    client.fetch_access_token()
    if timstamp-int(jsapi_ticket['expires_in']) > 7000:
        ticket = client.jsapi.get_jsapi_ticket(client)
        jsapi_ticket['expires_in'] = time.time()
        jsapi_ticket['ticket'] = ticket
    else:
        ticket = jsapi_ticket['ticket']
    return {"first": client.jsapi.get_jsapi_signature(NONCESTR, ticket, timestamp=timstamp, url=url), "second": ticket}



