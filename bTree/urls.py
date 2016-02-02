# -*-coding:utf-8 -*-
__author__ = 'albert'

from django.conf.urls import include, url
from django.contrib import admin
from bTree.views import weixin_main, home, visit, first, ajax_distribute


urlpatterns = [
    url(r'^$', weixin_main),  # 微信认证，自动回复消息关注消息等等
    url(r'^wechat/home/', home),  # 回到自己的主页或者第一次引导种树
    url(r'^wechat/visit', visit),  # 访问别人的主页链接方式
    url(r'wechat/first', first),
    url(r'wechat/ajax', ajax_distribute),
    url(r'^admin/', include(admin.site.urls)),

]