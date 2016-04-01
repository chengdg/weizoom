#author: 王丽
#editor: 新新 2016.3.28

Feature: 会员列表-会员详情-收货信息
"""

	1.Jobs能通过管理系统在商城中的会员详情查看到会员在手机端的管理地址中使用的地址信息列表
	2.会员设置默认地址，后台查看会员地址列表默认置顶

"""
@mall2 @member @memberList @yanhaonan
Scenario:1 会员添加地址，后台查看会员地址列表
	Given jobs登录系统
	And 开启手动清除cookie模式

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp

	When bill设置jobs的webapp的收货地址
		"""
		{
			"ship_name": "收货人A",
			"ship_tel": "13811223344",
			"area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill设置jobs的webapp的收货地址
		"""
		{
			"ship_name": "收货人B",
			"ship_tel": "13811223355",
			"area": "北京市,北京市,朝阳区",
			"ship_address": "泰兴大厦"
		}
		"""
	When bill设置jobs的webapp的收货地址
		"""
		{
			"ship_name": "收货人C",
			"ship_tel": "13811223366",
			"area": "天津市,天津市,河西区",
			"ship_address": "泰兴大厦"
		}
		"""

	Given jobs登录系统
	Then jobs获得'bill'的收货信息列表
		"""
		[{
			"ship_name": "收货人C",
			"ship_tel": "13811223366",
			"area": "天津市,天津市,河西区",
			"ship_address": "泰兴大厦"
		},{
			"ship_name": "收货人A",
			"ship_tel": "13811223344",
			"area": "北京市,北京市,海淀区",
			"ship_address": "泰兴大厦"
		},{
			"ship_name": "收货人B",
			"ship_tel": "13811223355",
			"area": "北京市,北京市,朝阳区",
			"ship_address": "泰兴大厦"
		}]
		"""
#本场景没有实现过
#@yanhaonan
#Scenario:2 会员设置默认地址，后台查看会员地址列表默认置顶
#	Given jobs登录系统
#	And 开启手动清除cookie模式
#
#	When 清空浏览器
#	When bill关注jobs的公众号
#	When bill访问jobs的webapp
#
#	When bill设置jobs的webapp的收货地址
#		"""
#		{
#			"ship_name": "收货人A",
#			"ship_tel": "13811223344",
#			"area": "北京市,北京市,海淀区",
#			"ship_address": "泰兴大厦"
#		}
#		"""
#	When bill设置jobs的webapp的收货地址
#		"""
#		{
#			"ship_name": "收货人B",
#			"ship_tel": "13811223355",
#			"area": "北京市,北京市,朝阳区",
#			"ship_address": "泰兴大厦"
#		}
#		"""
#	When bill设置jobs的webapp的收货地址
#		"""
#		{
#			"ship_name": "收货人C",
#			"ship_tel": "13811223366",
#			"area": "天津市,天津市,河西区",
#			"ship_address": "泰兴大厦"
#		}
#		"""
#	When bill设置jobs的webapp的默认收货地址
#		"""
#		{
#			"ship_name": "收货人B",
#			"ship_tel": "13811223355",
#			"area": "北京市,北京市,朝阳区",
#			"ship_address": "泰兴大厦"
#		}
#		"""
#	Given jobs登录系统
#	Then jobs获得'bill'的收货信息列表
#		"""
#		[{
#			"ship_name": "收货人B",
#			"ship_tel": "13811223355",
#			"area": "北京市,北京市,朝阳区",
#			"ship_address": "泰兴大厦"
#		},{
#			"ship_name": "收货人A",
#			"ship_tel": "13811223344",
#			"area": "北京市,北京市,海淀区",
#			"ship_address": "泰兴大厦"
#		},{
#			"ship_name": "收货人C",
#			"ship_tel": "13811223366",
#			"area": "天津市,天津市,河西区",
#			"ship_address": "泰兴大厦"
#		}]
#		"""