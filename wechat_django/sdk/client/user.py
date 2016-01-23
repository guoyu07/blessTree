# -*-coding:utf-8 -*-
__author__ = 'albert'

"""
    获取用户基本信息的类
    参阅：http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
"""
from wechat_django.sdk.client.base import BaseWeChatAPI


class WeChatUser(BaseWeChatAPI):
    # def get(self, user_id, lang='zh_CN'):
    #     """
    #     获取用户的基本信息
    #     :param user_id: 用户id
    #     :param lang: 国家地区语言
    #     :return:返回json数据包
    #     """
    #     assert lang in ('zh_CN', 'zh_TW', 'en'), 'lang can only be one of \
    #         zh_CN, zh_TW, en language codes'
    #
    #     return self._get(
    #         'user/info',
    #         params={
    #             'openid': user_id,
    #             'lang': lang
    #             }
    #     )
    def get(self, user_id, access_token, lang='zh_CN'):
        """
        获取用户的基本信息
        :param user_id: 用户id
        :param lang: 国家地区语言
        :return:返回json数据包
        """
        assert lang in ('zh_CN', 'zh_TW', 'en'), 'lang can only be one of \
            zh_CN, zh_TW, en language codes'

        return self._get(
            'https://api.weixin.qq.com/cgi-bin/user/info',
            params={
                'access_token': access_token,
                'openid': user_id,
                'lang': lang
                }
        )
        # return access_token

    def get_followers(self, first_user_id=None):
        """
            获取关注者列表，微信服务器会保存关注者列表
            参考：http://mp.weixin.qq.com/wiki/3/17e6919a39c1c53555185907acf70093.html
        :param first_user_id:第一个拉取的用户id
        :return:返回的json包
        """
        params = {}
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get(
            'user/get',
            params=params
        )

    def update_remark(self, user_id, remark):
        """
            设置用户备注名字
            http://mp.weixin.qq.com/wiki/10/bf8f4e3074e1cf91eb6518b6d08d223e.html
        :param user_id:用户id
        :param remark:备注名
        :return:返回的json数据包
        """
        return self._post(
            'uer/info/updateremark',
            data={
                'openid': user_id,
                'remark': remark
            }
        )

    def get_group_id(self, user_id):
        """
        获取用户所在分组
        :param user_id:
        :return:
        """
        res = self._post(
            'groups/getid',
            data={'openid': user_id},
            result_processor=lambda x: x['groupid']
        )
        return res

    def get_batch(self, user_list):
        """
            批量获取用户基本信息
        :param user_list:
        :return:用户信息列表list对象
        """
        res = self._post(
            'user/info/batchget',
            data={'user_list': user_list},
            result_processor=lambda x: x['user_info_list']
        )
        return res