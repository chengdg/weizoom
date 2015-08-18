Feature: 获得购买趋势信息
	jobs通过管理系统能获得购买趋势信息

Background:
	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	When jobs已添加商品
		"""
		[{
			"name": "东坡肘",
			"category": "分类1,分类2",
			"model": {
				"models": {
					"standard": {
						"price": 11.1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾",
			"category": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.0
					}
				}
			}
		}]
		"""
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的800会员积分
	Then bill在jobs的webapp中拥有800会员积分
	When jobs给会员bill"分配"测试权限
	Then bill获取测试权限
		"""
		{
			"test_whether_permission": "是"
		}
		"""
	Given tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom获得jobs的800会员积分
	Then tom在jobs的webapp中拥有800会员积分
	When jobs给会员tom"分配"测试权限
	Then tom获取测试权限
		"""
		{
			"test_whether_permission": "是"
		}
		"""
	Given nokia登录系统
	When nokia已添加商品
		"""
		[{
			"name": "酸菜鱼",
			"model": {
				"models": {
					"standard": {
						"price": 22.2,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When nokia已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given bill关注nokia的公众号
	When bill访问nokia的webapp


@mall2 @mall.outline1 @vippp1
Scenario: 获得购买趋势
	jobs的用户购买商品后，jobs能获得正确的购买趋势

	When 微信用户批量消费jobs的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    |
		| 7天前      | -nokia   | 购买 | jobs      |东坡肘,1  |          |  1      | 支付    |           |
		| 7天前      | bill     | 测试 | jobs      |叫花鸡,1  |          |  1      | 支付    |           |
		| 7天前      | tom      | 购买 | jobs      |水晶虾,2  |          |        | 支付    |           |
		| 7天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        |         | jobs,取消 |
		| 7天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        |         |           |
		| 6天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 5天前      | bill     | 测试 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 5天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 5天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        |         | jobs,取消 |
		| 5天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        |         |           |
		| 4天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 4天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        |         | jobs,取消 |
		| 4天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 4天前      | -tom1    | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 3天前      | tom      | 测试 | jobs      |东坡肘,1  |          |        |         |           |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | -nokia   | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        |         |           |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 今天       | bill     | 购买 | jobs      |东坡肘,1  |          |        |         |           |
		| 今天       | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 今天       | bill     | 测试 | jobs      |东坡肘,1  |          |        |         | jobs,取消 |
	When 微信用户批量消费nokia的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    |
		| 今天       | bill     | 购买 | nokia     |酸菜鱼,2  |          |        | 支付    |           |
	Given jobs登录系统
	Then jobs能获取'7天'购买趋势
		| date  	 | product_count | money |
		| 7天前      | 2             | 17.1  |
		| 6天前      | 1             | 11.1  |
		| 5天前      | 1             | 11.1  |
		| 4天前      | 3             | 33.3  |
		| 3天前      | 2             | 22.2  |
		| 2天前      | 0             | 0.0   |
		| 1天前      | 3             | 33.3  |



@mall2 @mall.outline
Scenario: 获得商铺首页的代发货订单列表
	jobs的用户购买商品后，jobs能获得正确的待发货订单列表

	When 微信用户批量消费jobs的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    | order_id |
		| 4天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 1        |
		| 4天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 2        |
		| 4天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 3        |
		| 4天前      | -tom1    | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 4        |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 5        |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 6        |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 7        |
		| 1天前      | -nokia   | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 8        |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 9        |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        |         |           | 10       |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 11       |
		| 1天前      | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           | 12       |
		| 今天       | bill     | 购买 | jobs      |水晶虾,2  |          |        | 支付    |           | 13       |
		| 今天       | bill     | 测试 | jobs      |东坡肘,1  |          |        | 支付    |           | 14       |
		| 今天       | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    | jobs,取消 | 15       |
	When 微信用户批量消费nokia的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    | order_id |
		| 今天       | bill     | 购买 | nokia     |酸菜鱼,2  |          |        | 支付    |           | 16       |
	Given jobs登录系统
	Then jobs能获取商铺首页的代发货订单列表
		"""
		{
			"count": 12,
			"orders_list": [{
				"date": "今天",
				"items": [{
					"order_id": "13",
					"order_money": 6.0,
					"product_count": 2
				}]
			}, {
				"date": "1天前",
				"items": [{
					"order_id": "12",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "11",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "9",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "8",
					"order_money": 11.1,
					"product_count": 1
				}]
			}, {
				"date": "3天前",
				"items": [{
					"order_id": "7",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "6",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "5",
					"order_money": 11.1,
					"product_count": 1
				}]
			}, {
				"date": "4天前",
				"items": [{
					"order_id": "4",
					"order_money": 11.1,
					"product_count": 1
				}, {
					"order_id": "3",
					"order_money": 11.1,
					"product_count": 1
				}]
			}]
		}
		"""


@mall2 @mall.outline @wip
Scenario: 获得商铺首页的订单数量信息
	jobs的用户购买商品后，jobs能获得正确的待发货订单列表

	When 微信用户批量消费jobs的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    |
		| 3天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | -nokia   | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 1天前      | bill     | 测试 | jobs      |东坡肘,1  |          |        |         |           |
		| 1天前      | tom      | 购买 | jobs      |东坡肘,1  |          |        |         |           |
		| 1天前      | bill     | 购买 | jobs      |水晶虾,2  |          |        | 支付    |           |
		| 1天前      | bill     | 购买 | jobs      |水晶虾,2  |          |        | 支付    | jobs,取消 |
		| 今天       | bill     | 购买 | jobs      |水晶虾,2  |          |        | 支付    |           |
		| 今天       | bill     | 测试 | jobs      |东坡肘,1  |          |        | 支付    |           |
		| 今天       | bill     | 购买 | jobs      |东坡肘,1  |          |        | 支付    | jobs,取消 |
	When 微信用户批量消费nokia的商品
		| date  	 | consumer | type |businessman|product   | integral | coupon | payment | action    |
		| 1天前      | bill     | 购买 | nokia     |酸菜鱼,2  |          |        | 支付    |           |
	Given jobs登录系统
	Then jobs能获取商铺首页的数量信息
		"""
		{
			"order_count_for_yesterday": 3,
			"order_money_for_yesterday": 28.2
		}
		"""


@mall2 @mall.outline @zy_ui_1
Scenario: 获得商铺首页的会员数量信息
	jobs的用户购买商品后，jobs能获得正确的待发货订单列表

	When bill取消关注jobs的公众号
	When tom取消关注jobs的公众号
	When tom1关注jobs的公众号于'1天前'
	When tom2关注jobs的公众号于'1天前'
	When tom3关注jobs的公众号于'1天前'
	When tom3取消关注jobs的公众号
	When tom4关注nokia的公众号于'1天前'
	When tom5关注jobs的公众号于'2天前'
	Given jobs登录系统
	Then jobs能获取商铺首页的数量信息
		"""
		{
			"member_count_for_yesterday": 2,
			"total_member_count": 6
		}
		"""
