# __author__ : "王丽"

Feature: 会员列表-会员详情-浏览轨迹
"""
	会员浏览本店铺的轨迹记录
	1、【时间】：浏览网页的时间
	2、【链接】：浏览的网页的名称
"""
Scenario:1 会员详情-浏览轨迹

	Given jobs登录系统

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
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

	#bill下单购买jobs的商品1

		#待发货
			When bill访问jobs的webapp
			And bill购买jobs的商品
				"""
				{
					"order_no": "001",
					"products": [{
						"name": "商品1",
						"count": 1
					}],
					"pay_type": "微信支付"
				}
				"""
			When jobs'支付'订单'001'

		#jobs发货订单
			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "001",
					"logistics": "off",
					"shipper": ""
				}
				"""

	#When bill访问jobs的微站链接'个人中心'于'2015-08-27 18:34:15'
	#When bill访问jobs的微站链接'商品列表(全部)'于'2015-08-27 18:34:18'
	#When bill访问jobs的微站链接'商品2'于'2015-08-27 18:34:21'
	#When bill访问jobs的微站链接'编辑订单'于'2015-08-27 18:34:23'

	Given jobs登录系统
	Then jobs获得'bill'的浏览轨迹
		"""
		[{
			"date_time":"今天",
			"link":"个人中心"
		},{
			"date_time":"今天",
			"link":"商品列表(全部)"
		}]
		"""

