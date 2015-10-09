# _author_ "师帅8.27"
Feature:bill在webapp中进入到待评价列表，对已到货的商品进行评价,评价完成后，商品部在该列表中显示
#1.bill进入待评价列表，该列表中显示的是订单状态为"已完成"的订单，可以对商品进行评价
#2.同一商品，下过两个订单，不同订单对同一商品的评价不会相互影响
#3.同一商品，不同规格进行评价，不会互相影响
#4.评论后的商品在商品评论中按照评论顺序倒序排列


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
	And jobs已添加商品
	"""
		[{
			"name": "商品1",
			"price": 10.0
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": [{
				"model": [{
					"M": {
						"price": 20.0,
						"stock_type": "无限"
					}, 
					"S" {
						"price": 40.0,
						"stock_type": "无限"
					}
				}]
			}]
		}, {
			"name": "商品3",
			"price": 30.0
		}]
	"""
	And bill关注jobs的公众号
	And bill已添加订单
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}]
	"""
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""

Scenario: 1 bill进入待评价列表，该列表中显示的是订单状态为"已完成"的订单，可以对商品进行评价
	When bill登录个人中心
	And bill对订单1'发表评论'不上传图片
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	And bill对订单2'发表评论'并上传图片
	"""
		[{
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",,
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}]
	"""
	Then bill成功获得'待评价'列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""


Scenario: 2 同一商品，下过两个订单，不同订单对同一商品的评价不会相互影响
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
			"status": "待支付",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill使用'微信支付'
	And jobs进行'发货'操作
	And bill进行'确认收货'操作
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill对订单1'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill对订单3'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""

Scenario: 3 同一商品，不同规格进行评价，不会互相影响
	When bill访问jobs的webapp
	And bill购买jobs的商品
	"""
		[{
			"name": "商品2",
			"model": "S",
			"price": 40.0
			"count": 1
		}]
	"""
	Then bill成功创建订单
	"""
		[{
			"status": "待支付",
			"final_price": 40.0,
			"products": [{
				"name": "商品2",
				"model": "S"
				"price": 40.0,
				"count": 1
			}]
		}]
	"""
	When bill使用'微信支付'
	And jobs进行'发货'操作
	And bill进行'确认收货'操作
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "S"
				"price": 40.0,
				"count": 1
			}]
		}]
	"""
	When bill对订单2'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"price": 40.0,
				"model": "S"
				"count": 1
			}]
		}]
	"""
	When bill对订单3'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品2",
				"price": 40.0,
				"model": "S"
				"count": 1
			}]
		}]
	"""

Scenario: 4 评论后的商品在商品评论中按照评论顺序倒序排列
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
			"status": "待支付",
			"final_price": 10.0,
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill使用'微信支付'
	And jobs进行'发货'操作
	And bill进行'确认收货'操作
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill对订单1'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	When bill对订单3'发表评价'，不上传图片
	Then bill获得待评价列表
	"""
		[{
			"order_no": "1",
			"buy_time": 2015-08-10,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}, {
			"order_no": "2",
			"buy_time": 2015-8-15,
			"status": "已完成",
			"comment": "发表评价",
			"products": [{
				"name": "商品2",
				"model": "M",
				"price": 20.0,
				"count": 1
			}]
		}, {
			"order_no": "3",
			"buy_time": 2015-8-20,
			"status": "已完成",
			"comment": "追加晒图",
			"products": [{
				"name": "商品1",
				"price": 10.0,
				"count": 1
			}]
		}]
	"""
	And bill进入商品1详情页
	"""	
		[{
			"buyer": "bill",
			"comment_time": 2015-09-10,
			"comment_content": "11111111"
		}, {
			"buyer": "bill",
			"comment_time": 2015-09-09,
			"comment_content": "22222222222"
		}]
	"""


