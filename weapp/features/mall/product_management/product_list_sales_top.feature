# __author__ : "宋温馨"

Feature:商品销量排行
"""
	Jobs能通过管理系统通过点击"总销量"查看销量排行

"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"product_id":001
			"name": "商品1",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":002
			"name": "商品2",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":003
			"name": "商品3",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":004
			"name": "商品4",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":005
			"name": "商品5",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":006
			"name": "商品6",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":007
			"name": "商品7",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"product_id":008
			"name": "商品8",
			"status": "在售",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		[{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		},{
			"products": [{
				"name": "商品2",
				"count": 2
			}]
		},{
			"products": [{
				"name": "商品3",
				"count": 3
		},{
			"products": [{
				"name": "商品4",
				"count": 3
			}]
		},{
			"products": [{
				"name": "商品5",
				"count": 1
			}
		},{
			"products": [{
				"name": "商品6",
				"count": 2
			}]
		},{
			"products": [{
				"name": "商品7",
				"count": 3
			}]
		},{
			"products": [{
				"name": "商品8",
				"count": 1
			}]
		}]
		"""
	Then bill成功创建订单
		"""
		[{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品2",
				"price": 100.00,
				"count": 2
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品3",
				"price": 100.00,
				"count": 3
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品4",
				"price": 100.00,
				"count": 1
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品5",
				"price": 100.00,
				"count": 1
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品6",
				"price": 100.00,
				"count": 2
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品7",
				"price": 100.00,
				"count": 3
			}
		},{
			"status": "已完成",
			"final_price": 100.00,
			"products": {
				"name": "商品8",
				"price": 100.00,
				"count": 1
			}
		}]
		"""
	Given jobs登录系统
	Then jobs能获取在售商品列表
		"""
		[{
			"name": "商品8",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品7",
			"sales":3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品6",
			"sales":2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品5",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品4",
			"sales":3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"name": "商品3",
			"sales": 3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"name": "商品2",
			"sales": 2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 8
					}
				}
			}
		},{
			"name": "商品1",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""
	When jobs批量下架商品
		"""
		[
			"商品5", 
			"商品6",
			"商品7",
			"商品8"
		]
		"""
	Then jobs能获取待售商品列表
		"""
		[{
			"name": "商品8",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品7",
			"sales":3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品6",
			"sales":2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"name": "商品5",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""
Scenario:1：第一次点击在售商品列表'总销量'，在售列表按照销量的降序排列，销量相同按照商品id的降序排列（销量下箭头）
			第二次点击在售商品列表'总销量'，在售列表按照销量的升序排列，销量相同按照商品id的降序排列（销量上箭头）
	Given jobs登录系统
	And jobs点击在售商品列表'总销量'，
	Then jobs能获取在售商品列表
		"""
		[{
			"product_id":003
			"name": "商品3",
			"sales": 3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":002
			"name": "商品2",
			"sales": 2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 8
					}
				}
			}
		},{
			"product_id":004
			"name": "商品4",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"product_id":001
			"name": "商品1",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""
	When jobs点击在售商品列表'总销量'，
	Then jobs能获取在售商品列表
		"""
		[{
			"product_id":004
			"name": "商品4",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":001
			"name": "商品1",
			"sales": 1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":002
			"name": "商品2",
			"sales": 2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 8
					}
				}
			}
		},{
			"product_id":003
			"name": "商品3",
			"sales":3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""
Scenario:2：第一次点击待售商品列表'总销量'，在售列表按照销量的降序排列，销量相同按照商品id的降序排列（销量下箭头）
			第二次点击待售商品列表'总销量'，在售列表按照销量的升序排列，销量相同按照商品id的降序排列（销量上箭头）
	Given jobs登录系统
	And jobs点击待售商品列表'总销量'，
	Then jobs能获取待售商品列表
		"""
		[{
			"product_id":007
			"name": "商品7",
			"sales": 3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":006
			"name": "商品6",
			"sales": 2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 8
					}
				}
			}
		},{
			"product_id":008
			"name": "商品8",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		},{
			"product_id":005
			"name": "商品5",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""	
	When jobs点击待售商品列表'总销量'，
	Then jobs能获取待售商品列表
		"""
		[{
			"product_id":008
			"name": "商品8",
			"sales":1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":005
			"name": "商品5",
			"sales": 1,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 7
					}
				}
			}
		},{
			"product_id":006
			"name": "商品2",
			"sales": 2,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 8
					}
				}
			}
		},{
			"product_id":007
			"name": "商品3",
			"sales":3,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 9
					}
				}
			}
		}]
		"""

