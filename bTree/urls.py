__author__ = 'albert'

from django.conf.urls import include, url
from django.contrib import admin
from bTree.views import test, weixin_main, main_page
urlpatterns = [
    url(r'^$', weixin_main),
    url(r'^wechat/', main_page),
    url(r'^admin/', include(admin.site.urls)),
]