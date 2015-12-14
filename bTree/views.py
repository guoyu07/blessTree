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
from wechat_django.sdk.parser import parse_message
# Create your views here.

WEIXIN_TOKEN = 'weixin'

@csrf_exempt
def weixin_main(request):
    """
        微信接入验证(GET)
        微信正常接收信息(POST)
    """

    if request.method == 'GET':
        signature  =request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = WEIXIN_TOKEN
        if check_signature(token, signature, timestamp, nonce):
            return HttpResponse(echostr)
    else:
        msg = parse_message(request.body)  # request.body就是post的xml格式文件
        return HttpResponse(msg)

def test(request):
    html = "<p>你好</p>"
    return HttpResponse(html)