# __author__ : "新新8.27"

Feature: 在webapp中收藏商品
"""
	bill能在webapp中收藏jobs添加的"商品"
	该feature中需要修改和补充,涉及到场景如下
	#个人中心显示有"*件收藏";无收藏显示"无收藏";根据收藏件数,更新"*件收藏";
	#我的收藏按收藏的倒序显示
	1.收藏单个无规格商品,我的收藏显示该商品名称及原价
	2.收藏有规格商品,我的收藏显示该商品名称及最低规格原价
	3.收藏商品后,下架,我的收藏中仍显示
	#下架后,点击该商品,已下架
	4.收藏商品后,删除,我的收藏中仍显示
	#删除后,点击该商品,提示"抱歉!该商品已停售"
	4.收藏多个商品，包括无规格和有规格的商品
	5.从我的收藏里面取消收藏商品
	6.从商品详情,取消收藏商品
	7.收藏无规格商品后，后台对此商品进行修改
	#包括价格或名称修改,我的收藏列表数据更新
	#包括无规格变有规格,我的收藏列表数据更新价格为最低价格原价
"""



Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 50.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 100.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品3",
			"price": 100.00
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号


Scenario: 收藏单个无规格商品
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品收藏
	2. bill能在个人中心我的收藏，查看已收藏的商品
	3. tom的个人中心我的收藏不受bill操作的影响

	When bill访问jobs的webapp
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	When tom访问jobs的webapp
	Then tom能获得我的收藏
		"""
		[]
		"""


Scenario: 收藏多个商品，包括无规格和有规格的商品
	jobs添加商品后
	1. bill能在webapp中将jobs添加的商品收藏
	2. bill能在个人中心我的收藏，查看已收藏的商品
	3. 收藏的商品按时间的倒序排列

	When bill访问jobs的webapp
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品2"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品2",
			"price": 50.00
		}, {
			"name": "商品1",
			"price": 100.00
		}]
		"""


Scenario: 从我的收藏里面取消收藏商品
	bill在webapp收藏jobs的商品后
	1. bill能取消收藏已收藏的商品

	When bill访问jobs的webapp
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	When bill取消收藏已收藏的商品
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[]
		"""
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品1"
		}
		"""
	And bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品2"
		}
		"""
	And bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品3"
		}
		"""

	Then bill能获得我的收藏
		"""
		[{
			"name": "商品3",
			"price": 100.00
		}, {
			"name": "商品2",
			"price": 50.00
		}, {
			"name": "商品1",
			"price": 100.00
		}]
		"""
	When bill取消收藏已收藏的商品
		"""
		{
			"name": "商品2"
		}
		"""
	And bill取消收藏已收藏的商品
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品3",
			"price": 100.00
		}]
		"""


Scenario: 收藏商品后，后台对此商品进行修改
	bill在webapp收藏jobs的商品后
	1. jobs对此商品进行修改价格

	When bill访问jobs的webapp
	When bill收藏jobs的商品到我的收藏
		"""
		{
			"name": "商品1"
		}
		"""
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}]
		"""
	Given jobs登录系统
	When  jobs更新商品'商品1'
		"""
		{
			"name": "商品1",
			"price": 50.00
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得我的收藏
		"""
		[{
			"name": "商品1",
			"price": 50.00
		}]
		"""




