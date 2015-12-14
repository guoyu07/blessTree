__author__ = 'albert'

from django.conf.urls import include, url
from django.contrib import admin
from bTree.views import test, weixin_main
urlpatterns = [
    url(r'', test),
    url(r'^wechat/', weixin_main),
    url(r'^admin/', include(admin.site.urls)),
]