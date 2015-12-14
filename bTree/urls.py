__author__ = 'albert'

from django.conf.urls import include, url
from django.contrib import admin
from bTree.views import test
urlpatterns = [
    url(r'', test),
    url(r'^admin/', include(admin.site.urls)),
]