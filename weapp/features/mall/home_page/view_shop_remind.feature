#_author_:张三香
#editor:王丽 2015.10.13

Feature:查看店铺提醒
	"""
		1、商品管理：
			在售商品(x):
				x为当前系统中'在售商品管理'列表中所有商品的数量;
				点击链接,打开新页面跳转到'在售商品管理'页面
			库存不足商品(x):
				x为当前系统中'在售商品管理'列表中库存为0的所有商品数量;
				点击链接,打开新页面跳转到'在售商品管理'页面,并携带查询条件'商品库存:0~0'
		2、订单管理：
			待发货(x):
				x为当前系统中所有状态为'待发货'的订单数量;
				点击链接,打开新页面跳转到'所有订单'页面，并携带查询条件'订单状态：待发货'
			退款中(x):
				x为当前系统中所有状态为'退款中'的订单数量;
				点击链接,打开新页面跳转到'所有订单'页面，并携带查询条件'订单状态：退款中'
		3、即将到期的活动：只提醒24小时内要结束且未过期的活动,筛选条件为2014.4.1至第二天零点之前到期的活动
			限时抢购(x):
				x为24小时内要结束的限时抢购活动;
				点击链接,打开新页面跳转到'限时抢购'页面,将快结束的活动展示出来
			买赠(x):
				x为24小时内要结束的买赠活动;
				点击链接,打开新页面跳转到'买赠'页面,将快结束的活动展示出来
			积分应用(x):
				x为24小时内要结束的积分应用活动;
				点击链接,打开新页面跳转到'积分应用'页面,将快结束的活动展示出来
			优惠券(x):
				x为24小时内要结束的优惠券活动;
				点击链接,打开新页面跳转到'优惠券'页面,将快结束的活动展示出来
			分享红包(x):
				x为24小时内要结束的分享红包活动;
				点击链接,打开新页面跳转到'分享红包'页面,将快结束的活动展示出来
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
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"stock_type": "有限",
			"stocks": 0,
			"status":"待售"
		}, {
			"name": "商品2",
			"price": 100.00,
			"stock_type": "有限",
			"stocks":0,
			"status":"在售"
		}, {
			"name": "商品3",
			"price": 100.00,
			"stock_type": "有限",
			"stocks":1,
			"status":"在售"
		}, {
			"name": "商品4",
			"price": 100.00,
			"stock_type": "无限",
			"status":"在售"
		}, {
			"name": "商品5",
			"is_enable_model": "启用规格",
			"status":"在售",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}]
		"""
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号

@mall2 @homePage @statistics
Scenario: 1 查看商品管理
	Given jobs登录系统
	Then jobs能获取店铺提醒信息
		"""
		{
			"onshelf_product_count":4,
			"sellout_product_count":2
		}
		"""

	#上架或下架对'商品管理-出售中的商品'的影响
		When jobs'上架'商品'商品1'
		Then jobs能获取店铺提醒信息
			"""
			{
				"onshelf_product_count":5,
				"sellout_product_count":3
			}
			"""
		When jobs'下架'商品'商品4'
		Then jobs能获取店铺提醒信息
			"""
			{
				"onshelf_product_count":4,
				"sellout_product_count":3
			}
			"""

	#库存修改对'商品管理-库存不足的商品'的影响
		When jobs更新商品'商品2'
			"""
			{
				"name": "商品2",
				"price": 100.00,
				"stock_type": "有限",
				"stocks":2,
				"status":"在售"
			}
			"""
		Then jobs能获取店铺提醒信息
			"""
			{
				"onshelf_product_count":4,
				"sellout_product_count":2
			}
			"""

		When bill访问jobs的webapp
		When bill购买jobs的商品
			"""
			{
				"products": [{
					"name": "商品3",
					"count": 1
				}]
			}
			"""
		Given jobs登录系统
		Then jobs能获取店铺提醒信息
			"""
			{
				"onshelf_product_count":4,
				"sellout_product_count":3
			}
			"""

@mall2 @homePage @statistics
Scenario: 2 查看订单管理

	When 微信用户批量消费jobs的商品
		|order_id| date  | consumer |product   | payment | pay_type  | action        | status*  |
		|00001   | 3天前 | bill     |商品4,1   |         | 微信支付  |               | 待支付   |
		|00002   | 3天前 | bill     |商品5,M,1 |   支付  | 货到付款  | jobs,取消     | 已取消   |
		|00003   | 3天前 | tom      |商品5,M,1 |   支付  | 货到付款  |               | 待发货   |
		|00004   | 3天前 | bill     |商品5,M,1 |   支付  | 支付宝    | jobs,发货     | 已发货   |
		|00005   | 3天前 | bill     |商品5,M,1 |   支付  | 微信支付  | jobs,完成     | 已完成   |
		|00006   | 2天前 | bill     |商品5,M,1 |   支付  | 微信支付  | jobs,退款     | 退款中   |
		|00007   | 2天前 | bill     |商品5,M,1 |   支付  | 微信支付  | jobs,完成退款 | 退款成功 |
		|00008   | 1天前 | bill     |商品5,M,1 |   支付  | 微信支付  |               | 待发货   |
		|00009   | 今天  | tom      |商品4,1   |   支付  | 微信支付  | jobs,退款     | 退款中   |
		|00010   | 今天  | bill     |商品5,M,1 |   支付  | 支付宝    |               | 待发货   |
	Given jobs登录系统
	Then jobs能获取店铺提醒信息
		"""
		{
			"to_be_shipped_order_count":3,
			"refunding_order_count":2
		}
		"""

	#购买或进行发货操作影响'待发货'订单数
		#进行购买操作
			When bill访问jobs的webapp
			When bill购买jobs的商品
				"""
				{
					"order_id": "00011",
					"products": [{
						"name": "商品4",
						"count": 1
					}]

				}
				"""
			And bill使用支付方式'货到付款'进行支付
			When tom访问jobs的webapp
			When tom购买jobs的商品
				"""
				{
					"order_id": "00012",
					"products": [{
						"name": "商品4",
						"count": 1
					}]
				}
				"""
			And bill使用支付方式'微信支付'进行支付
			Given jobs登录系统
			Then jobs能获取店铺提醒信息
				"""
				{
					"to_be_shipped_order_count":5,
					"refunding_order_count":2
				}
				"""
		#进行发货操作
			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no":"00003",
					"logistics":"顺丰速运",
					"number":"123456789",
					"shipper":"jobs"
				}
				"""
			Then jobs能获取店铺提醒信息
				"""
				{
					"to_be_shipped_order_count":4,
					"refunding_order_count":2
				}
				"""
	#申请退款或完成退款影响'退款中'订单数
		Given jobs登录系统
		When jobs'申请退款'订单'00005'
		Then jobs能获取店铺提醒信息
			"""
			{
				"to_be_shipped_order_count":4,
				"refunding_order_count":3
			}
			"""
		When jobs通过财务审核'退款成功'订单'00005'
		Then jobs能获取店铺提醒信息
			"""
			{
				"to_be_shipped_order_count":4,
				"refunding_order_count":2
			}
			"""
