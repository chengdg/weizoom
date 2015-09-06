# __author__ : "王丽"

Feature: 会员列表-会员详情-浏览轨迹
"""
	会员浏览本店铺的轨迹记录
	1、【时间】：浏览网页的时间
	2、【链接】：浏览的网页的名称
"""

Scenario:1 会员详情-浏览轨迹

	Given jobs登录系统
	And 开启手动清除cookie模式

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品2",
				"price":100
			}]
			"""
		And jobs已添加支付方式
			"""
			[{
				"type": "货到付款",
				"is_active": "启用"
			},{
				"type": "微信支付",
				"is_active": "启用"
			},{
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""

	When bill关注jobs的公众号

	When bill访问jobs的微站链接'个人中心'于'2015-08-27 18:34:15'
	When bill访问jobs的微站链接'商品列表(全部)'于'2015-08-27 18:34:18'
	When bill访问jobs的微站链接'商品2'于'2015-08-27 18:34:21'
	When bill访问jobs的微站链接'编辑订单'于'2015-08-27 18:34:23'

	Given jobs登录系统
	Then jobs获得'bill'的浏览轨迹
		"""
		[{
			"date_time":"2015-08-27 18:34:15",
			"link":"个人中心"
		},{
			"date_time":"商品列表(全部)",
			"link":""
		},{
			"date_time":"2015-08-27 18:34:21",
			"link":"商品2"
		},{
			"date_time":"2015-08-27 18:34:23",
			"link":"编辑订单"
		}]
		"""

