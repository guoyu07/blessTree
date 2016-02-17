# --coding:utf-8 -*-
__author__ = 'albert'
# import json
import time

# Django 库文件

from django.shortcuts import HttpResponse

from bTree import client, appId, appsecret
from bTree.models import User, Tree
from django.core.exceptions import ObjectDoesNotExist
from wechat_django.sdk.oauth import WeChatOAuth
import simplejson as json

# 根据不同的ajax请求码分发给不同的视图函数处理
"""
    分发所有ajax请求的函数
    请求码类型：
    ajax_type{
        '1': 第一次种树填入树名字时候保存到数据库[]
        '2': 主页面， 请求刷新排行榜的时候[]
        '3': 主页面， 请求刷新消息的时候[]
        '4': 请求提交浇水获取的积分的时候[][
        '5': 主页面和访问页面 请求刷新祝福的时候[][
        '6': 主页面和访问页面 请求刷新吐槽的时候[][
        '7': 主页面和访问页面 请求刷新心愿的时候[][
        '8': 主页面， 请求提交输入心愿的时候[]
        '9': 访问页面， 祝福提交请求[]
        '10': 访问页面， 吐槽提交请求[]
        '11': 第一次分享朋友圈增加积分的请求(添加好友不需要ajax请求增加积分[]
              因为会在对方注册使用的时候发送一个json来同时增加双方的分数与建立朋友关系)
        '12'： 祝福吐槽果点击的ajax获取

    }
    :param request: 含有ajax请求数据的请求对象
    :return:response，含有一个ret值
    ret值声明：1--成功 2--失败
    注意，获取数据时候，json为空的时候一定是拉取完了所有的内容
 """


def ajax_1(request):
    """
    ajax_type='1': 第一次种树填入树名字时候保存到数据库
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    user_name = request.POST.get('nickname', '')
    tree_name = request.POST.get('tree_name', '')
    if user_id and user_name and tree_name:
        try:
            user = User.objects.get(openid=user_id)
            user.is_plant = True
            user.tree_name = tree_name
            user.friends.add(user)
            friend = user.friends.exclude(openid=user_id)[0]
            # friend = User.objects.get(openid=friend_id.openid)
            friend.count = friend.count + 3000
            friend.save()
            user.save()
            msg = Tree(owner=friend, tree_name=friend.tree_name, type=4, action_time=time.time(),
                       read=False, source_id=user_id, content='成功添加好友'+user_name)
            msg.save()
            tree = Tree(owner=user, tree_name=user.tree_name, type=7, action_time=time.time(),
                        source_id=user_id, content='种下了自己的幸福树')
            tree.save()
            ret = '4'
        except ObjectDoesNotExist:
            user = User(openid=user_id, nickname=user_name, time_stamp=time.time(), tree_name=tree_name)
            user.save()
            user.friends.add(user)
            user.save()
            tree = Tree(owner=user, tree_name=tree_name, type=7, action_time=time.time(), read=True, source_id=user_id,
                        content='创建了祝福树')
            tree.save()
            ret = '3'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_2(request):
    """
    :param request:
    :return:
    """
    response = HttpResponse()
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    if user_id and load_begin:
        user = User.objects.get(openid=user_id)
        try:
            user_list = user.friends.filter(is_plant=True)[0]
            user_list = user.friends.filter(is_plant=True).order_by('-count')
            user_dict = []
            for user in user_list:
                # 获取用户头像
                client.fetch_access_token()
                user_info = client.user.get(client, user.openid)
                # 生成用户页面访问链接
                user_home = WeChatOAuth(appId, appsecret,
                                    'http://1.blesstree.sinaapp.com/wechat/visit'+'?openid='+user.openid).authorize_url
                # 生成传输用的数据
                user_dict.append({"name": user.nickname,
                                  "avatar": user_info['headimgurl'],
                                  "count": user.count,
                                  "user_home": user_home})
        except IndexError:
            user_list = []
        response['Content-Type'] = 'application/json'
        # user_dict = [{"name": '启程'}, {'name': "标"}, {'name': "啦啦啦"}]
        json_dict = json.dumps(user_dict)
        response.write(json_dict)
    else:
        ret = '2'
        response.write(ret)
    return response

    # response = HttpResponse()
    # # response['Content-Type'] = 'text/javascript'
    # ret = '2'+user_id+load_begin  # 返回错误码
    # response.write(ret)
    # return response


def ajax_3(request):
    """
    消息获取
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        dict_msg = []
        try:
            msg_list = Tree.objects.filter(owner=owner, read=False)[0]
            msg_list = Tree.objects.filter(owner=owner, read=False).exclude(tree_name='na').order_by('action_time')
            for msg in msg_list:
                if msg.source_id == 'na':  # 匿名？
                    nickname = '匿名'
                    avatar = 'none'
                else:
                    source = User.objects.get(openid=msg.source_id)  # 是否关注
                    if source.is_plant == False:
                        nickname = source.nickname
                        avatar = source.avatar_url
                    else:
                        user_info = client.user.get(client, msg.source_id)
                        nickname = user_info['nickname']
                        avatar = user_info['headimgurl']
                if 8+int(msg.action_time.strftime("%H")) > 24:
                    time = msg.action_time.strftime("%m-")+\
                           str(int(msg.action_time.strftime("%d"))+1)+'\n'\
                               +str(int(msg.action_time.strftime("%H"))-16)+msg.action_time.strftime(":%I:%S")
                else:
                    time = msg.action_time.strftime("%m-%d")+'\n'\
                               +str(8+int(msg.action_time.strftime("%H")))+msg.action_time.strftime(":%I:%S")
                dict_msg.append({"msg_nick": nickname,
                                 "msg_avatar": avatar,
                                 "msg_con": msg.content,
                                 "msg_time": time})

                # 读取过一次就再也不读取了
                msg.read = True
                msg.save()
            json_msg = json.dumps(dict_msg)
            response.write(json_msg)
            return response
        except IndexError:
            ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_4(request):
    """
    浇水成功提交积分上去
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    user_id = request.POST.get('openid', '')
    source_id = request.POST.get('source_id', '')
    if user_id:
        user = User.objects.get(openid=user_id)
        if user_id == source_id:
            type = 0
        else:
            type = 3
        Tree(owner=user, tree_name=user.tree_name, count=user.count, type=type,
             action_time=time.time(), source_id=source_id,
             content=User.objects.get(openid=source_id).nickname+'给树木浇水了').save()

        user.count = user.count + 1000
        if source_id:
            try:
                friend = user.friends.get(openid=source_id)
            except ObjectDoesNotExist:
                friend = 0
            if friend != 0:
                user.friends.add(User.objects.get(openid=source_id))  # 通过朋友圈啊什么的浇水，自己浇水的时候自己是自己的朋友
        user.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_5(request):
    """
    收到的祝福的历史刷新
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        dict_bless = []
        try:
            bless_list = Tree.objects.filter(owner=owner, type=5)[0]
            bless_list = Tree.objects.filter(owner=owner, type=5).order_by('-action_time')
            for bless in bless_list:
                if bless.source_id == 'na':  # 匿名？
                    nickname = '匿名'
                    avatar = 'none'
                else:
                    source = User.objects.get(openid=bless.source_id)  # 是否关注
                    if source.is_plant == False:
                        nickname = source.nickname
                        avatar = source.avatar_url
                    else:
                        user_info = client.user.get(client, bless.source_id)
                        nickname = user_info['nickname']
                        avatar = user_info['headimgurl']
                if 8+int(bless.action_time.strftime("%H")) > 24:
                    time = bless.action_time.strftime("%m-")+\
                           str(int(bless.action_time.strftime("%d"))+1)+'\n'\
                               +str(int(bless.action_time.strftime("%H"))-16)+bless.action_time.strftime(":%I:%S")
                else:
                    time = bless.action_time.strftime("%m-%d")+'\n'\
                               +str(8+int(bless.action_time.strftime("%H")))+bless.action_time.strftime(":%I:%S")
                dict_bless.append({"bless_nick": nickname,
                                   'bless_avatar': avatar,
                                   'bless_con': bless.content,
                                   'bless_time': time})
            json_bless = json.dumps(dict_bless)
            response.write(json_bless)
            return response
        except IndexError:
            ret = '1'  # 数据库没有记录，说明没有祝福
    else:
        ret = '2'  # 不明原因的错误
    response.write(ret)
    return response


def ajax_6(request):
    """
    收到的吐槽刷新
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        dict_tucao = []
        try:
            tucao_list = Tree.objects.filter(owner=owner, type=6)[0]
            tucao_list = Tree.objects.filter(owner=owner, type=6).order_by('-action_time')
            for tucao in tucao_list:
                if tucao.source_id == 'na':  # 匿名？
                    nickname = '匿名'
                    avatar = 'none'
                else:
                    source = User.objects.get(openid=tucao.source_id)  # 是否关注
                    if source.is_plant == False:
                        nickname = source.nickname
                        avatar = source.avatar_url
                    else:
                        user_info = client.user.get(client, tucao.source_id)
                        nickname = user_info['nickname']
                        avatar = user_info['headimgurl']
                if 8+int(tucao.action_time.strftime("%H")) > 24:
                    time = tucao.action_time.strftime("%m-")+\
                           str(int(tucao.action_time.strftime("%d"))+1)+'\n'\
                               +str(int(tucao.action_time.strftime("%H"))-16)+tucao.action_time.strftime(":%I:%S")
                else:
                    time = tucao.action_time.strftime("%m-%d")+'\n'\
                               +str(8+int(tucao.action_time.strftime("%H")))+tucao.action_time.strftime(":%I:%S")
                dict_tucao.append({"tucao_nick": nickname,
                                   "tucao_avatar": avatar,
                                   "tucao_con": tucao.content,
                                   "tucao_time": time})
            json_tucao = json.dumps(dict_tucao)
            response.write(json_tucao)
            return response
        except IndexError:
            ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_7(request):
    """
    请求刷新心愿
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        if owner.willing == 'none':
            ret = '1'
        else:
            try:
                will_list = Tree.objects.filter(owner=owner, type=2)[0]
                will_list = Tree.objects.filter(owner=owner, type=2).order_by('action_time')
                will_dict = []
                for will in will_list:
                    if 8+int(will.action_time.strftime("%H")) > 24:
                        time = will.action_time.strftime("%m-")+\
                               str(int(will.action_time.strftime("%d"))+1)+'\n'\
                               +str(int(will.action_time.strftime("%H"))-16)\
                               +str((32+int(will.action_time.strftime(":%I"))) % 60)\
                               +str(will.action_time.strftime(":%S"))
                    else:
                        time = will.action_time.strftime("%m-%d")+'\n'\
                                +str(8+int(will.action_time.strftime("%H")))\
                                +str((32+int(will.action_time.strftime(":%I"))) % 60)\
                                +str(will.action_time.strftime(":%S"))
                    will_dict.append({'will_time': time,
                                      'will_con': will.content})
                response['Content-Type'] = 'application/json'
                json_bless = json.dumps(will_dict)
                response.write(json_bless)
                return response
            except IndexError:
                will_dict = []
                ret = '1'
        # 没有数据的时候返回1，表示没有新年愿望
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_8(request):
    """
    输入心愿提交到服务器
    :param request:
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    will_con = request.POST.get('will_con', '')
    ret = '0'
    if user_id and will_con:
        user = User.objects.get(openid=user_id)
        will = Tree(owner=user, tree_name=user.tree_name, type=2, action_time=time.time(), read=True, source_id=user_id,
                    content=will_con)
        if user.willing == 'none':
            user.count = user.count + 20000
        user.willing = 'yes'
        will.save()
        user.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_9(request):
    """
    :param request:
        给别人祝福,注意此处的_sourceid是推送的人的id，就是谁触发事件的
    :return:
    """
    response = HttpResponse()
    # response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    source_id = request.POST.get('source_id', '')
    bless_con = request.POST.get('bless_con', '')
    ret = '0'
    if user_id and source_id and bless_con:
        user = User.objects.get(openid=user_id)
        user.count = user.count + 5000
        user.save()
        bless = Tree(owner=user, tree_name=user.tree_name, type=5, action_time=time.time(),
                        read=False, source_id=source_id, content=bless_con)
        bless.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_10(request):
    """
    给别人吐槽
    :param request:
        注意此处的source_id是推送的人的id，就是谁触发事件的
    :return:
    """
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    source_id = request.POST.get('source_id', '')
    tucao_con = request.POST.get('tucao_con', '')
    ret = '0'
    if user_id and source_id and tucao_con:
        user = User.objects.get(openid=user_id)
        user.count = user.count - 8000
        user.save()
        tucao = Tree(owner=user, tree_name=user.tree_name, type=6, action_time=time.time(), read=False,
                    source_id=source_id, content=tucao_con)
        tucao.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_11(request):
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    ret = '0'
    if user_id:
        user = User.objects.get(openid=user_id)
        if user.if_share == False:
            user.count = user.count + 20000
            user.if_share = True
            user.save()
        else:
            ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response


def ajax_12(request):
    response = HttpResponse()
    response['Content-Type'] = 'application/json'

    user_id = request.POST.get('openid', '')
    ajax_type = request.POST.get('ajax_type', '')
    if ajax_type and user_id:
        try:
            user = User.objects.get(openid=user_id)
            if ajax_type == '12':
                type = '5'
            else:
                type = '6'
            fruit = Tree.objects.filter(owner=user, type=type)

        except ObjectDoesNotExist:
            ret = '2'


