# -*-coding:utf-8 -*-
__author__ = 'albert'
"""
    自定义菜单创建删除等的类
"""

from wechat_django.sdk.client.base import BaseWeChatAPI
import json

class WeChatMenu(BaseWeChatAPI):
    def get(self, client):
        """
        查询自定义菜单
        参阅：  http://mp.weixin.qq.com/wiki/16/ff9b7b85220e1396ffa16794a9d95adc.html
        :return:返回的json数据
        """
        try:
            return self._get(client, 'menu/get')
        except Exception :
            pass

    def create(self, client, menu_data):
        """
            创建自定义菜单
            client = WeChatClient("id", "secret")
            client.menu.create({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]
            })

        参阅
        http://mp.weixin.qq.com/wiki/13/43de8269be54a0a6f64413e4dfa94f39.html
        :param menu_data:python字典，菜单的信息
        :return:json数据
        """
        json_data = json.dumps(menu_data, ensure_ascii=False).encode('utf-8')
        return self._post(
            client,
            'menu/create',
            data=json_data,
        )


    update = create

    def delete(self):
        """
            删除自定义菜单
        :return:返回的json数据
        """
        return self._get('menu/delete')

    def get_menu_info(self):
        """
            获取自定义菜单的配置
        :return:json数据包
        """
        return self._get('get_current_selfmenu_info')