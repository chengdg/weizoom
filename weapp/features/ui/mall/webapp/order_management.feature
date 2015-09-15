# _author_ "师帅8.27"
Feature:在webapp中查看订单管理
#1.用户使用“货到付款”支付，订单列表显示“待发货”状态
#2.用户使用“支付宝”和“微信支付”支付，订单列表显示“待发货”状态
#3.用户提交订单后，取消订单，显示“已取消”状态
#4.用户提交订单后，后台发货为“不需要物流”，在订单列表页显示“已完成”状态
#5.用户提交订单后，后台发货，在订单列表显示“待收货”状态，并能查询物流
#6.订单列表按钮提交订单顺序，倒序排列
#7.用户提交订单后,后台申请退款后,在前台订单列表中显示"退款中"状态
#8.用户提交订单后,后台申请退款后,审核通过后,在前台订单列表中显示"退款成功"状态

Background:
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品1",
			"price": 10.0
		}, {
			"name": "商品2",
			"price": 20.0
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
		}, {
			"type": "支付宝支付",
			"is_active": "启用"
		}]
	"""
	And bill关注jobs的公众号

Scenario: 1 用户使用“货到付款”，“支付宝”和“微信支付”支付，订单列表显示“待发货”状态
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货"
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	#使用'货到付款'
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	#使用'支付宝支付'和'微信支付'
	When bill使用'支付宝支付'和'微信支付'
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""

Scenario: 2 用户提交订单后，取消订单，显示“已取消”状态
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When bill进行'取消订单'操作
	Then bill可以看到订单列表
	"""
		[{
			"status": "已取消",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""

Scenario: 3 用户提交订单后，后台发货为“不需要物流”，在订单列表页显示“已完成”状态
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When jobs在后台发货使用'不需要物流'
	And bill登录个人中
	Then bill可以看到订单列表
	"""
		[{
			"status": "已完成",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""

Scenario: 4 用户提交订单后，后台发货，在订单列表显示“待收货”状态，并能查询物流
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When jobs在后台进行'发货'操作
	And bill登录个人中
	Then bill可以看到订单列表
	"""
		[{
			"status": "待收货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	And bill能查询物流信息

Scenario: 5 订单列表按钮提交订单顺序，倒序排列
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When bill购买jobs的商品
	"""
		[{
			"name": "商品2",
			"price": 20.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 20.0,
			"products": [{
				"name": "商品2",
				"price": 20.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 20.0,
			"buy_time": 2015-09-10
			"products": [{
				"product_name": "商品2",
				"count": 1,
				"total_price": 20.0
			}]
		}, {
			"status": "待发货",
			"price": 10.0,
			"buy_time": 2015-09-09
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0
			}]
		}]
	"""
	When bill使用'货到付款'支付
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"buyer": "bill",
			"buy_time": 2015-09-10
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}, {
			"status": "待发货",
			"price": 20.0,
			"buyer": "bill",
			"buy_time": 2015-09-09
			"products": [{
				"product_name": "商品2",
				"count": 1,
				"total_price": 20.0
			}]
		}, {
			"status": "待发货",
			"price": 10.0,
			"buyer": "bill",
			"buy_time": 2015-09-08


			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""

Scenario: 6 用户提交订单后,后台申请退款后,在前台订单列表中显示"退款中"状态
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0
			"products": [{
				"name": "商品1",
				"price": 10.0,
			}]
		}]
	"""
	When bill使用'支付宝支付'
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When jobs进行'申请退款'操作
	Then bill可以看到订单列表
	"""
		[{
			"status": "退款中",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""

Scenario: 7 用户提交订单后,后台申请退款后,审核通过后,在前台订单列表中显示"退款成功"状态
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品1",
			"price": 10.0,
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待发货",
			"final_price": 10.0
			"products": [{
				"name": "商品1",
				"price": 10.0,
			}]
		}]
	"""
	When bill使用'支付宝支付'
	And bill登录个人中心
	Then bill可以看到订单列表
	"""
		[{
			"status": "待发货",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When jobs进行'申请退款'操作
	Then bill可以看到订单列表
	"""
		[{
			"status": "退款中",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""
	When jobs进行'退款成功'操作
	Then bill可以看到订单列表
	"""
		[{
			"status": "退款成功",
			"price": 10.0,
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": 10.0
			}]
		}]
	"""




