
#_author_:张三香

Feature:促销管理-查看买赠活动详情信息

	#说明：
		#针对线上"bug3752"补充feature
		#bug3752-（功能问题）【促销管理】-【买赠】买赠详情页，赠品信息中的“总销量”显示-1

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price":100.00
		},{
			"name": "赠品",
			"price":100.00
		}]
		"""

Scenario: 查看买赠活动详情信息
	Given jobs登录系统
	Then jobs能获取商品'商品1'
		"""
		{
			"name":"商品1",
			"price":100.00,
			"sales":1
		}
		"""
	And jobs能获取商品'赠品'
		"""
		{
			"name":"赠品",
			"price":100.00,
			"sales":2
		}
		"""
	When jobs创建买赠活动
		"""
			[{
				"name": "商品1买一赠一",
				"promotion_title":"",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"product_name": "商品1",
				"premium_products": 
				[{
					"name": "赠品",
					"sales":2,
					"count": 1
				}],
				"count": 1,
				"is_enable_cycle_mode": false
			}]
		"""
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "商品1买一赠一",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""
	And jobs能获取买赠活动'商品1买一赠一'
		"""
			[{
				"main_product":
				{
					"name":"商品1",
					"price":100.00,
					"sales":1
				},
				"premium_products"
					{
						"name":"商品1",
						"price":100.00,
						"sales":2
					},
				"name": "商品1买一赠一",
				"promotion_title":"",
				"start_date": "今天",
				"end_date": "1天后",
				"member_grade": "全部会员",
				"count": 1,
				"is_enable_cycle_mode": false
			}]
		"""