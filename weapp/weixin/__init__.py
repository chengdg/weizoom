# -*- coding: utf-8 -*-

__author__ = 'chuter'

NAV_NAME = 'weixin'

WEIXIN_QA_KEYWORD_QA_NAV_NAME = 'keyword_qa'
WEIXIN_QA_AUTO_QA_NAV_NAME = 'auto_qa'
WEIXIN_QA_FOLLOW_QA_NAV_NAME = 'follow_qa'

WEIXIN_QA_MATERAL_NEWS_NAV_NAME = 'material_news'
WEIXIN_MANAGE_MENU_NAV_NAME = 'menu'

WEIXIN_MESSAGE_NAV_NAME = 'message'

#===============================================================================
# get_weixin_second_navs : 获取微信二级导航列表
#===============================================================================
def get_weixin_second_navs():
	second_navs = [
		{
			"section" : "自动回复",
			"navs" : [
				{
				"url" : "/weixin/message/qa/follow_rule/",
				"title" : "关注回复",
				"name" : WEIXIN_QA_FOLLOW_QA_NAV_NAME,
				},
				{
				"url" : "/weixin/message/qa/unmatch_rule/",
				"title" : "自动回复",
				"name" : WEIXIN_QA_AUTO_QA_NAV_NAME,
				},
				{
				"url" : "/weixin/message/qa/",
				"title" : "关键词回复",
				"name" : WEIXIN_QA_KEYWORD_QA_NAV_NAME,
				}
			]
		},

		{
			"section" : "微信消息",
			"navs" : [
				{
				"url" : "/weixin/message/message/",
				"title" : "实时消息",
				"name" : WEIXIN_MESSAGE_NAV_NAME,
				}
			]
		},

		{
			"section" : "高级管理",
			"navs" : [
				{
				"url" : "/weixin/message/material/newses/",
				"title" : "图文管理",
				"name" : WEIXIN_QA_MATERAL_NEWS_NAV_NAME,
				},
				{
				"url" : "/weixin/manage/customized_menu/",
				"title" : "自定义菜单",
				"name" : WEIXIN_MANAGE_MENU_NAV_NAME,
				}
			]
		},
	]

	return second_navs
