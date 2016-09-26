# __author__ : "李娜" 2016-09-26

Feature:商品池同步商品（多规格）
"""
	给商家池同步商品
"""
Background:
	#商家bill的商品信息
		Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name": "商品池商品供货商"
		}
		"""
		Then 可以查到该供货商
		"""
		{
			"supplier_name": "商品池商品供货商"
		}
		"""
###特殊说明：zy1, zy2表示自营商家, zymanager表示特殊商品池的那个商家webapp_type=2的那个

###特殊说明,次场景必须带有ziying这个字符串，否则，跑完后，会把自应平台全部更新成普通平台
@product_pool_sync_product @bert-g
Scenario:1 给商品池同步商品，ziying
	#给商品池同步商品，
		Given 给自营平台同步商品
			"""
			{
				"accounts": ["zy2", "zy1"],
				"supplier_name": "商品池商品供货商",
				"name": "商品池商品测试zy",
				"promotion_title": "商品池商品测试zy-title",
				"weight": 1,
				"image": "love.png",
				"detail": "商品1-1描述信息",
				"model": {
					"models":{
							"M": {
								"price": 301.00,
								"stocks": 101
							},
							"S": {
								"price": 300.00,
								"stocks": 101
							}
						}
					}
			}
			"""

		Then 给供货商添加运费配置
			"""
			{
				"supplier_name": "商品池商品供货商",
				"postage":5,
				"condition_money": "10"
			}
			"""
		Then 自营平台可以在商品池看到该商品
			"""
			{
				"accounts": ["zy1", "zy2"],
				"product_name": "商品池商品测试zy"

			}
			"""

		Given zy1登录系统
		When zy1上架商品池商品“商品池商品测试zy”
		Then zy1能获得'在售'商品列表
		"""
		[{
			"name": "商品池商品测试zy"
		}]
		"""


