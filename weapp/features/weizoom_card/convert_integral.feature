#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "冯雪静"
Feature: 微众卡兑换积分
	微众卡可以在商城兑换积分

Background:
	Given jobs登录系统
	And jobs已有微众卡支付权限
	And jobs已添加支付方式
		"""
		[{
			"type":"微众卡支付"
		}]
		"""
	And jobs已创建微众卡
		"""
		{
			"cards":[{
				"id":"0000001",
				"password":"1234567",
				"status":"未激活",
				"price":5.00
			},{
				"id":"0000002",
				"password":"1231231",
				"status":"已过期",
				"price":5.00
			}]
		}
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 1.00
		}]
		"""
	And bill关注jobs的公众号
	And jobs已有的会员
		"""
		[{
			"name":"bill",
			"integral":"100"
		}]
		"""
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan":100
		}
		"""
		
@market_tools @weizoom_card.integral
Scenario:用未使用的微众卡进行兑换积分
	bill用未使用的微众卡进行兑换积分后
	1.bill积分的增加
	2.微众卡余额为0元
	3.jobs查看微众卡日志

	Given jobs登录系统
	When jobs给id为'0000001'的微众卡激活
	When bill访问jobs的webapp
	And bill使用'微众卡兑换积分'进行兑换
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill在jobs的webapp中拥有600会员积分
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"已用完",
			"price":0.00,
			"log":[{
				"merchant":"jobs",
				"order_id":"激活",
				"price": 0
			},{
				"merchant":"jobs",
				"order_id":"积分兑换",
				"price": 5.00
			}]
		}
		"""

@market_tools @weizoom_card.integral
Scenario:用已使用的微众卡进行兑换积分
	bill用已使用的微众卡进行兑换积分后
	1.bill积分的增加
	2.微众卡余额为0元
	3.jobs查看微众卡日志

	Given jobs登录系统
	When jobs给id为'0000001'的微众卡激活
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products":[{
				"name":"商品1",
				"price":1.00,
				"count":3
			}]
		}
		"""
	And bill使用支付方式'微众卡支付'进行支付
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill查看订单
		"""
		{
			"status": "待发货",
			"pay_interface_type":"微众卡支付",
			"final_price":3.00,
			"products":[{
				"name":"商品1",
				"price":1.00,
				"count":3
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"已使用",
			"price":2.00
		}
		"""
	When bill访问jobs的webapp
	When bill使用'微众卡兑换积分'进行兑换
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill在jobs的webapp中拥有300会员积分
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"已用完",
			"price":0.00,
			"log":[{
				"merchant":"jobs",
				"order_id":"激活",
				"price": 0
			},{
				"merchant":"jobs",
				"order_id":"使用",
				"price": 3.00
			},{
				"merchant":"jobs",
				"order_id":"积分兑换",
				"price": 2.00
			}]
		}
		"""

@market_tools @weizoom_card.integral
Scenario:用已过期的微众卡进行兑换积分
	bill用已过期的微众卡进行兑换积分后
	1.bill积分的不变
	2.微众卡余额不变
	3.jobs查看微众卡日志

	When bill访问jobs的webapp
	And bill使用'微众卡兑换积分'进行兑换
		"""
		{
			"id":"0000002",
			"password":"1231231"
		}
		"""
	Then bill获得错误提示'微众卡己过期'
	Then bill在jobs的webapp中拥有100会员积分
	Given jobs登录系统
	Then jobs能获取微众卡'0000002'
		"""
		{
			"status":"已过期",
			"price":5.00,
			"log":[]
		}
		"""
		
@market_tools @weizoom_card.integral
Scenario:用已用完的微众卡进行兑换积分
	bill用已用完的微众卡进行兑换积分后
	1.bill积分的不变
	2.微众卡余额不变
	3.jobs查看微众卡日志

	Given jobs登录系统
	When jobs给id为'0000001'的微众卡激活
	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products":[{
				"name":"商品1",
				"price":1.00,
				"count":5
			}]
		}
		"""
	And bill使用支付方式'微众卡支付'进行支付
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill查看订单
		"""
		{
			"status": "待发货",
			"pay_interface_type":"微众卡支付",
			"final_price":5.00,
			"products":[{
				"name":"商品1",
				"price":1.00,
				"count":5
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"已用完",
			"price":0.00
		}
		"""
	When bill访问jobs的webapp
	When bill使用'微众卡兑换积分'进行兑换
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill在jobs的webapp中拥有100会员积分
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"已用完",
			"price":0.00,
			"log":[{
				"merchant":"jobs",
				"order_id":"激活",
				"price": 0
			},{
				"merchant":"jobs",
				"order_id":"使用",
				"price": 5.00
			}]
		}
		"""
@market_tools @weizoom_card.integral
Scenario:用未激活的微众卡进行兑换积分
	bill用未激活的微众卡进行兑换积分后
	1.bill积分的不变
	2.微众卡余额不变
	3.jobs查看微众卡日志

	When bill访问jobs的webapp
	And bill使用'微众卡兑换积分'进行兑换
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill获得错误提示'微众卡未激活'
	Then bill在jobs的webapp中拥有100会员积分
	Given jobs登录系统
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status":"未激活",
			"price":5.00,
			"log":[]
		}
		"""




