
#_author_:张三香

Feature:微众精选-查看订单操作日志

	"""
		1、对多供货商多商品的订单,进行不同的操作后,订单操作日志选项卡，在操作列，对“发货”、“修改物流”、“完成”三个状态后增加供货商名称,示例数据如下：
			| 时间                | 操作            |操作人|
			| 2015-09-11 10:35:59 |下单             |客户  |
			| 2015-09-11 10:36:59 |支付             |客户  |
			| 2015-09-11 10:37:59 |发货-土小宝      |张一  |
			| 2015-09-11 11:35:59 |修改物流-米奇尔  |张二  |
			| 2015-09-11 12:35:59 |完成-丹江湖      |李一  |
			| 2015-09-11 13:35:59 |退款             |李二  |
	"""


Background:
	Given jobs登录系统
	And jobs已添加供货商
		"""
		[{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}, {
			"name": "米奇尔",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "卖大米"
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
	And jobs已添加商品
		"""
		[{
			"supplier": "土小宝",
			"name": "花生",
			"price": 100.00
		}, {
			"supplier": "丹江湖",
			"name": "鸭蛋",
			"price": 100.00
		}, {
			"supplier": "土小宝",
			"name": "花生油",
			"price": 100.00
		}, {
			"supplier": "米奇尔",
			"name": "大米",
			"price": 100.00
		}]
		"""
	And bill关注jobs的公众号

@mall2 @order
Scenario: 1 查看多供货商多商品订单的操作日志
	#bill购买商品后，使用微信支付
	#1. 能在不同状态下执行各种操作
	#3. 订单详情里能看到对应的操作日志

	#bill下单
		When bill访问jobs的webapp
  		And bill设置jobs的webapp的收货地址
			"""
			{
				"ship_name": "AAA",
				"ship_tel": "13811223344",
				"area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦"
			}
			"""
		And bill加入jobs的商品到购物车
			"""
			[{
				"name": "花生",
				"count": 1
			}, {
				"name": "鸭蛋",
				"count": 1
			}, {
				"name": "花生油",
				"count": 1
			}, {
				"name": "大米",
				"count": 1
			}]
			"""
		When bill从购物车发起购买操作
			"""
			{
				"action": "pay",
				"context": [{
					"name": "花生"
				}, {
					"name": "鸭蛋"
				}, {
					"name": "花生油"
				}, {
					"name": "大米"
				}]
			}
			"""
		And tom在购物车订单编辑中点击提交订单
			"""
			{
				"pay_type": "货到付款",
				"order_no": "001"
			}
			"""
		Then bill成功创建订单
			"""
			{
				"order_no": "001",
				"status": "待支付",
				"ship_name": "AAA",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"final_price": 400.00,
				"postage": 0.00,
				"products": [{
					"name": "花生",
					"price": 100.00,
					"count": 1
				}, {
					"name": "鸭蛋",
					"price": 100.00,
					"count": 1
				}, {
					"name": "花生油",
					"price": 100.00,
					"count": 1
				}, {
					"name": "大米",
					"price": 100.00,
					"count": 1
				}],
				"actions": ["取消订单", "支付"]
			}
			"""
	#bill支付
		When bill访问jobs的webapp
		And bill使用支付方式'微信支付'进行支付
	#发货-土小宝
		Given jobs登录系统
		When jobs对订单进行发货
			"""
			{
				"order_no":"001-土小宝",
				"logistics":"顺丰速运",
				"number":"123456789",
				"shipper":"jobs"
			}
			"""
	#发货-米奇尔
		When jobs对订单进行发货
			"""
			{
				"order_no":"001-米奇尔",
				"logistics":"顺丰速运",
				"number":"123456789",
				"shipper":"jobs|备注"
			}
			"""
	#发货-丹江湖
		When jobs对订单进行发货
			"""
			{
				"order_no":"001-丹江湖",
				"logistics":"顺丰速运",
				"number":"123456789",
				"shipper":"jobs|备注"
			}
			"""
	#修改物流-米奇尔
		When jobs通过后台管理系统对'001'的物流信息进行修改
			"""
			{
				"order_no":"001-米奇尔",
				"logistics":"申通快递",
				"number":"987654321",
				"status":"已发货"
			}
			"""
	#标记完成-土小宝
		When jobs完成订单"001-土小宝"
			"""
			{
				"order_no":"001-土小宝"
			}
			"""
	#校验各个操作的日志信息
		Then jobs能获得订单"001"操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 订单发货 - 土小宝       | jobs     |
			| 订单发货 - 米奇尔       | jobs     |
			| 订单发货 - 丹江湖       | jobs     |
			| 修改发货信息 - 米奇尔   | jobs     |
			| 完成 - 土小宝           | jobs     |
