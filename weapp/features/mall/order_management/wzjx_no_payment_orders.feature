
#_author_:张三香

Feature:微众精选待支付状态订单,后台列表页供货商字段的校验

	"""
	说明：
		在多商品订单生成，并成为待支付状态时，订单和以前保持一致仍然为一个整单的形式，使用一个订单号：
			此时在待支付状态下：
			a.多商品订单多供货商商品供货商列显示为空，
			b.多商品同一个供货商显示为供货商名称，
			c.单商品同供货商显示供货商名称。
	"""

Background:
	Given jobs登录系统
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	And jobs已添加供货商
		"""
		[{
			"name": "土小宝",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"supplier": "土小宝",
			"name": "花生",
			"status": "在售",
			"price": 10.00,
			"purchase_price": 9.00
		}, {
			"supplier": "土小宝",
			"name": "花生油",
			"status": "在售",
			"price": 10.00,
			"purchase_price": 9.00
		}, {
			"supplier": "丹江湖",
			"name": "鸭蛋",
			"status": "在售",
			"price": 10.00,
			"purchase_price": 9.00
		}]
		"""
	And bill关注jobs的公众号

@mall2 @order @allOrder
Scenario: 1 购买同供货商单商品,生成待支付订单（显示供货商名称）
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no":"00001",
			"products": [{
				"name": "花生",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 20.0,
			"product_price": 20.0,
			"products": [{
					"name": "花生",
					"price": 10.0,
					"count": 2
				}]
		}
		"""
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
			[{
				"order_no":"00001",
				"status": "待支付",
				"final_price": "20.00",
				"member": "bill",
				"products": [{
					"name": "花生",
					"price":10.0,
					"count": 2,
					"supplier":"土小宝"
				}]
			}]
		"""

@mall2 @order @allOrder
Scenario: 2 购买参与买赠的商品(主商品：供货商A,赠品：供货商B),生成待支付订单,（只显示供货商A,不显示供货商B）
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "买花生赠鸭蛋",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "全部会员",
			"product_name": "花生",
			"premium_products": 
				[{
					"name": "鸭蛋",
					"count": 1
				}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no":"00001",
			"products": [{
				"name": "花生",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 10.0,
			"product_price": 10.0,
			"products": [{
					"name": "花生",
					"price": 10.0,
					"count": 1,
					"promotion": {
						"type": "premium_sale"
						}
				},{
					"name": "鸭蛋",
					"price": 0.0,
					"count": 1,
					"promotion": {
							"type": "premium_sale:premium_product"
						}
				}]
		}
		"""
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
			[{
				"order_no":"00001",
				"status": "待支付",
				"final_price": "10.00",
				"member": "bill",
				"products": [{
					"supplier":"土小宝",
					"name": "花生"
				},{
					"name": "鸭蛋"
				}]
			}]
		"""

@mall2 @order @allOrder
Scenario: 3 购买同供货商多商品,生成待支付订单（显示供货商名称）
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no":"00001",
			"products": [{
				"name": "花生",
				"count": 1
			},{
				"name": "花生油",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 20.0,
			"product_price": 20.0,
			"products": [{
				"name": "花生",
				"price": 10.0,
				"count": 1
			},{
				"name": "花生油",
				"price": 10.0,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"00001",
			"status": "待支付",
			"final_price": "20.00",
			"member": "bill",
			"products":
				[{
					"name": "花生",
					"price": 10.0,
					"supplier":"土小宝",
					"count": 1
				},{
					"name": "花生油",
					"price": 10.0,
					"supplier":"土小宝",
					"count": 1
				}]
		}]
		"""

@mall2 @order @allOrder
Scenario: 4 购买多供货商多商品,生成待支付订单（供货商显示为空）
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"order_no":"00001",
			"products": [{
				"name": "花生",
				"count": 1
			},{
				"name": "花生油",
				"count": 1
			},{
				"name": "鸭蛋",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 30.0,
			"product_price": 30.0,
			"products": 
				[{
					"name": "花生",
					"price": 10.0,
					"count": 1
				},{
					"name": "花生油",
					"price": 10.0,
					"count": 1
				},{
					"name": "鸭蛋",
					"price": 10.0,
					"count": 1
				}]
		}
		"""
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
			[{
				"order_no":"00001",
				"status": "待支付",
				"final_price": "30.00",
				"member": "bill",
				"products": 
					[{
						"supplier":"",
						"name": "花生",
						"price": 10.0,
						"count": 1
					},{
						"supplier":"",
						"name": "花生油",
						"price": 10.0,
						"count": 1
					},{
						"supplier":"",
						"name": "鸭蛋",
						"price": 10.0,
						"count": 1
					}]
			}]
		"""