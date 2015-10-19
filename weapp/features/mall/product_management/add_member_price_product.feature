# __author__ : "冯雪静"
#editor:王丽 2015.10.15

Feature: 添加有会员折扣的商品
"""

	Jobs能通过管理系统在商城中添加有"会员折扣的商品"
"""

Background:
	Given jobs登录系统
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
	#系统默认一个会员等级"普通会员"、"自动升级"、
	#"所有关注过您的公众号的用户"、"购物折扣：10.0"
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

@mall2 @product @addProduct
Scenario:1 添加有会员折扣的商品
	jobs添加会员折扣的商品后，能获取他添加的商品

	#添加的商品使用了会员等级折扣
	Given jobs登录系统
	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "无限"
					},
					"S": {
						"price": 300,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品2'
		"""
		{
			"name": "商品2",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "无限"
					},
					"S": {
						"price": 300,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
