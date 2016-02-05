# --coding:utf-8 -*-
__author__ = 'albert'
# import json
import time

# Django 库文件

from django.shortcuts import HttpResponse

from bTree import client
from bTree.models import User, Tree
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import simplejson as json

# 根据不同的ajax请求码分发给不同的视图函数处理
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
        '11': 第一次分享朋友圈增加积分的请求(添加好友不需要ajax请求增加积分
              因为会在对方注册使用的时候发送一个json来同时增加双方的分数与建立朋友关系)
        '12'： 预留备用的

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
            num = user.friends.all()[0:1].get().count
            user.friends.all()[0:1].get().count = num + 20000  # 蛋疼。。。
            user.friends.all()[0:1].get().save()
            user.save()
            # msg = Tree(owner=user.friends[0], tree_name=user.friends.tree_name, type=4, action_time=time.time(),
            #            read=False, source_id=user_id, content='创建了祝福树')
            # msg.save()

            ret = '4'
        except ObjectDoesNotExist:
            # user = User(openid=user_id, nickname=user_name, time_stamp=time.time(), tree_name=tree_name)
            # user.save()
        # tree = Tree(owner=user, tree_name=tree_name, type=7, action_time=time.time(), read=True, source_id=user_id,
        #             content='创建了祝福树')
        # tree.save()
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
        # user_list = User.friends.filter(user_id=user_id).order_by('-count')[load_begin:load_begin+4]
        # dict_user = {'user_nick': [], 'user_avatar': [], 'user_count': [], 'user_home': []}
        # for user in user_list:
        #     user_info = client.user.get(client, user_id)
        #     dict_user['user_nick'].append(user.nickname)
        #     dict_user['user_avatar'].append(user_info['headimgurl'])
        #     dict_user['user_count'].append(user.count)
        #     dict_user['user_home'].append("test")  # TODO:去别人家的链接还没弄
        # json_rank = json.dumps(dict_user, ensure_ascii=False)
        # response.write(json_rank)
        # # 注意成功不反悔ret1，省去处理的麻烦
        response['Content-Type'] = 'application/json'
        # name_dict = {"twz": load_begin, "zqxt": "I am teaching Django"}
        name_dict = [{"name": '启程'}, {'name': "标"}, {'name': "啦啦啦"}]
        json_dict = json.dumps(name_dict)
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
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        msg_list = Tree.objects.filter(owner=owner, read=False).order_by('-action_time')[load_begin:load_begin+4]
        dict_msg = {'msg_nick': [], 'msg_avatar': [], 'msg_type': [], 'msg_time': []}
        for msg in msg_list:
            user_info = client.user.get(client, msg.owner.openid)
            dict_msg['msg_nick'].append(user_info['nickname'])
            dict_msg['msg_avatar'].append(user_info['headimgurl'])
            dict_msg['msg_type'].append(msg.type)
            dict_msg['msg_time'].append(msg.action_time)
            msg.read = True
            msg.save()  # 因为发送完了消息会认为消息已经读了
        json_msg = json.dumps(dict_msg, ensure_ascii=False)
        response.write(json_msg)
        # 注意成功不反悔ret1，省去处理的麻烦
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
    response['Content-Type'] = 'text/javascript'
    user_id = request.POST.get('openid', '')
    source_id = request.POST.get('source_id', '')
    if user_id:
        user = User.objects.get(openid=user_id)
        user.count = user.count + 1000
        if source_id:
            try:
                friend = User.friends.get(openid=source_id)
            except ObjectDoesNotExist:
                friend = 0
            if friend == 0:
                user.friends.add(User.objects.get(source_id))
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
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        bless_list = Tree.objects.filter(owner=owner, type=5).order_by('-action_time')[load_begin:load_begin+4]
        dict_bless = {'bless_nick': [], 'bless_avatar': [], 'bless_con': [], 'bless_time': []}
        for bless in bless_list:
            user_info = client.user.get(client, bless.owner.openid)
            dict_bless['bless_nick'].append(user_info['nickname'])
            dict_bless['bless_avatar'].append(user_info['headimgurl'])
            dict_bless['bless_con'].append(bless.type)
            dict_bless['bless_time'].append(bless.action_time)
        json_bless = json.dumps(dict_bless, ensure_ascii=False)
        response.write(json_bless)
        # 注意成功不反悔ret1，省去处理的麻烦
    else:
        ret = '2'
        response.write(ret)
    return response


def ajax_6(request):
    """
    收到的吐槽刷新
    :param request:
    :return:
    """
    response = HttpResponse()
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        tucao_list = Tree.objects.filter(owner=owner, type=6).order_by('-action_time')[load_begin:load_begin+4]
        dict_tucao = {'tucao_nick': [], 'tucao_avatar': [], 'tucao_con': [], 'tucao_time': []}
        for tucao in tucao_list:
            user_info = client.user.get(client, tucao.owner.openid)
            dict_tucao['tucao_nick'].append(user_info['nickname'])
            dict_tucao['tucao_avatar'].append(user_info['headimgurl'])
            dict_tucao['tucao_con'].append(tucao.type)
            dict_tucao['tucao_time'].append(tucao.action_time)
        json_tucao = json.dumps(dict_tucao, ensure_ascii=False)
        response.write(json_tucao)
        # 注意成功不反悔ret1，省去处理的麻烦
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
    user_id = request.POST.get('openid', '')
    load_begin = request.POST.get('load_begin', '')
    client.fetch_access_token()
    ret = '0'
    if user_id and load_begin:
        owner = User.objects.get(openid=user_id)
        will_list = Tree.objects.filter(owner=owner, type=2).order_by('-action_time')[load_begin:load_begin+4]
        dict_will = {'will_con': [], 'will_time': []}
        for will in will_list:
            dict_will['bless_con'].append(will.type)
            dict_will['bless_time'].append(will.action_time)
        json_bless = json.dumps(dict_will, ensure_ascii=False)
        response.write(json_bless)
        # 注意成功不反悔ret1，省去处理的麻烦
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
        user.count = user.count + 20000
        user.save()
        ret = '1'
    else:
        ret = '2'
    response.write(ret)
    return response

