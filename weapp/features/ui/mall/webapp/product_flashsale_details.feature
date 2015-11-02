# __edit__ : "新新9.17"

Feature: 商品是活动时,商品详情页显示
	bill能在webapp中商品详情页中看到提示信息
	"""
	1 商品限时抢购时,商品详情页
	2 商品买赠时,商品详情页
	3 商品积分时,商品详情页
	4 商品禁用优惠券时,商品详情页
	"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100
		},{
			"name": "商品2",
			"price": 100
		},{
			"name": "商品3",
			"price": 200
		},{
			"name": "商品4",
			"price": 50
		}]	
		"""

	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"promotion_price": 80
		}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品2买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"premium_products": [{
				"name": "商品2",
				"gifts_from":"单位",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"discount": 50,
			"discount_money": 100.0,
			"is_permanant_active": false
		}
		"""
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"商品4"
			}],
			"start_date": "今天",
			"end_date": "1天后",
			"is_permanant_active": 0
		}]
		"""
		And bill关注jobs的公众号


@ProductDetail
Scenario:1 商品限时抢购时,商品详情页
	When bill访问jobs的webapp
	When bill查看详情
	"""
		[{
			"name": "商品1"
		}]
	"""
	Then bill商品详情页中看到提示信息"限时抢购已优惠20.00元"


@ProductDetail
Scenario:2 商品买赠时,商品详情页
	When bill访问jobs的webapp
	When bill查看详情
	"""
		[{
			"name": "商品2"
		}]
	"""
	Then bill商品详情页中看到提示信息"买赠商品2 * 1单位"


@ProductDetail
Scenario:3 商品积分时,商品详情页
	When bill访问jobs的webapp
	When bill查看详情
	"""
		[{
			"name": "商品3"
		}]
	"""
	Then bill商品详情页中看到提示信息"积分抵扣最多可使用200积分,抵扣100.00元"


@ProductDetail
Scenario:4 商品禁用优惠券时,商品详情页
	When bill访问jobs的webapp
	When bill查看详情
	"""
		[{
			"name": "商品4"
		}]
	"""
	Then bill商品详情页中看到提示信息"该商品不参与全场优惠券使用!"