#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.thanks_card
Feature: 感恩贺卡
	Jobs能通过管理系统设置可以制作感恩贺卡的商品
	
Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9
		}, {
			"name": "商品2",
			"price": 8.8
		}]	
		"""
	And jobs已添加了支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号

@weapp.market_tools @weapp.market_tools.thanks_card
Scenario: 商品可以设置为可制作感恩贺卡, 也可以设置为不可以制作感恩贺卡，默认是不可以制作感恩贺卡

	Given jobs登录系统
	Then jobs获取到商品列表
	"""
		[{
			"name": "商品1",
			"support_make_thanks_card": "否"
		}, {
			"name": "商品2",
			"support_make_thanks_card": "否"
		}]
	"""
	When jobs设置'商品1,商品2'可以制作感恩贺卡
	Then jobs获取到商品列表
	"""
		[{
			"name": "商品1",
			"support_make_thanks_card": "是"
		}, {
			"name": "商品2",
			"support_make_thanks_card": "是"
		}]
	"""
	When jobs设置'商品1'可以制作感恩贺卡
	"""
		[{
			"name": "商品1",
			"support_make_thanks_card": "是"
		}, {
			"name": "商品2",
			"support_make_thanks_card": "否"
		}]
	"""

@weapp.market_tools @weapp.market_tools.thanks_card
Scenario: 对可制作贺卡的商品，当购买支付完成之后可以点击感恩密码制作贺卡

	Given jobs登录系统
	When jobs设置'商品1'可以制作感恩贺卡
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品1"
			}]
		}
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 2
			}],
			"customer_message": "bill的订单备注2"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品2"
			}]
		}
		"""
	Then bill获得2个感恩贺卡

@weapp.market_tools @weapp.market_tools.thanks_card
Scenario: 对可制作贺卡的商品，当购买支付完成之后可以点击感恩密码制作贺卡

	Given jobs登录系统
	When jobs设置'商品1'可以制作感恩贺卡
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品1"
			}]
		}
		"""
	When bill制作一张贺卡
	"""
		{
			"content": "中秋快乐, 祝爸爸妈妈身体健康"
		}
	"""
	Then bill成功制作贺卡
	"""
		{
			"content": "中秋快乐, 祝爸爸妈妈身体健康",
			"is_used": "是"
		}
	"""
	And bill剩余1张可制作贺卡

@weapp.market_tools @weapp.market_tools.thanks_card
Scenario: 对可制作贺卡的商品，当购买支付完成之后可以点击感恩密码制作贺卡

	Given jobs登录系统
	When jobs设置'商品1'可以制作感恩贺卡
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品1"
			}]
		}
		"""
	When bill制作一张贺卡
	"""
		{
			"content": "中秋佳节倍思亲"
		}
	"""
	And jobs对已制作贺卡修改密码
	Then bill剩余2张可制作贺卡

@weapp.market_tools @weapp.market_tools.thanks_card
Scenario: 制作图片、视频类型的贺卡
	
	Given jobs登录系统
	When jobs设置'商品1'可以制作感恩贺卡
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 3
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill支付订单成功
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品1"
			}]
		}
		"""
	When bill制作贺卡
		"""
			{
				"content": "带图片的贺卡",
				"type": "图片",
				"att_content": "img,12jkh4324ljkk",
				"card_img": "person.jpg"
			}
		"""
	Then bill可以查看到贺卡
		"""
			{
				"content": "带图片的贺卡",
				"type": "图片"
			}
		"""
	When bill制作贺卡
		"""
			{
				"content": "带视频的贺卡",
				"type": "视频",
				"att_content": "video,12jkh4324ljkk",
				"card_img": "person.mp4"
			}
		"""
	Then bill可以查看到贺卡
		"""
			{
				"content": "带视频的贺卡",
				"type": "视频"
			}
		"""
	When bill制作贺卡
		"""
			{
				"content": "带视频的贺卡",
				"type": "视频",
				"att_content": "video,12jkh4324ljkk",
				"card_img": "person.3gp"
			}
		"""
	Then bill可以查看到贺卡
		"""
			{
				"content": "制作贺卡失败"
			}
		"""