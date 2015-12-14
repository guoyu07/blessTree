# -*-coding:utf-8-*-
# python内置库
import hashlib
import json
# from lxml import etree


# Django 库文件
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render,HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.http import Http404
from wechat_django.sdk.utils import check_signature
# Create your views here.

WEIXIN_TOKEN = 'weixin_token'

# def weixin_main(request):
#
#     """
#     微信接入验证(GET)
#     微信正常接收信息(POST)
#     """
#
#     if request.method == 'GET':  # 获取微信服务器的认证接入
#         signature = request.GET.get('signature', None)
#         timestamp = request.GET.get('timestamp', None)
#         nonce = request.GET.get('nonce', None)
#         echostr = request.GET.get('echostr', None)
#         token = WEIXIN_TOKEN
#
#         if check_signature(token, signature, timestamp, nonce):
#             return HttpResponse(echostr)
#     else:
#         xml_str = smart_str(request.body)
#         request_xml = etree.fromstring(xml_str)

def test(request):
    html = "<p>你好</p>"
    return render_to_response(locals())