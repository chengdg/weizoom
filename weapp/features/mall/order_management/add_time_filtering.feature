# __author__ : "冯雪静"

Feature:订单筛选添加时间段筛选
"""
	jobs可以对订单进行"时间段筛选"
	1.根据下单时间，填写时间段查询订单
	2.根据支付时间，填写时间段查询订单
	3.根据发货时间，填写时间段查询订单
"""

Background:
	Given jobs登录系统
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given jobs已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000001",
				"password": "1",
				"status": "未激活",
				"price": 100.00
			},{
				"id": "0000002",
				"password": "1",
				"status": "未激活",
				"price": 50.00
			}]
		}
		"""
	When jobs给id为'0000001'的微众卡激活
	When jobs给id为'0000002'的微众卡激活
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":10.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And jobs选择'顺丰'运费配置
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "L"
			}, {
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
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 L": {
						"price": 100.00,
						"weight": 1
					},
					"红色 M": {
						"price": 100.00,
						"weight": 1
					},
					"红色 S": {
						"price": 100.00,
						"weight": 1
					}
				}
			},
			"unified_postage_money": 10.00
		},{
			"name": "商品2",
			"price": 100.00,
			"weight": 1,
			"unified_postage_money": 10.00
		},{
			"name": "商品3",
			"price": 100.00,
			"weight": 0
		}]
		"""
	And bill关注jobs的公众号
	Given jobs登录系统
	And jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral": 500
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券",
			"money": 100.00,
			"count": 3,
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": 50
		}
		"""

@mall2 @order @allOrder @tg
Scenario: 1 选择时间段查询订单
	jobs选择时间段确认后
	1.jobs选择时间段时,可以看到订单列表列表

	When 微信用户批量消费jobs的商品
		| order_id | date  | payment_time | consumer |      product   | payment   | pay_type   | price*    | integral |    coupon           | weizoom_card | paid_amount*   |  action      | order_status* | delivery_time |
		|  000001  | 3天前 |    3天前     | bill     | 商品1,红色 L,1 |   支付    |  微信支付  |  100.00   |          |                     |              |    110.00      |              |   待发货      |               |
		|  000002  | 3天前 |    今天      | bill     | 商品3,1        |   支付    |  支付宝    |  100.00   |          |                     |              |    100.00      |jobs,发货     |   已发货      |       今天    |
		|  000003  | 2天前 |    2天前     | bill     | 商品2,1        |   支付    |  支付宝    |  100.00   |          |                     |              |    110.00      |jobs,完成     |   已完成      |       1天前   |
		|  000004  | 2天前 |    2天前     | bill     | 商品2,1        |   支付    |  支付宝    |  100.00   |          | 优惠券,coupon1_id_1 |              |    10.00       |jobs,完成     |   已完成      |       2天前   |
		|  000005  | 1天前 |    1天前     | bill     | 商品2,2        |   支付    | 货到付款   |  200.00   |          |                     |              |    210.00      |              |   待发货      |               |
		|  000006  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  微信支付  |  100.00   |   100    |                     |              |     50.00      |              |   待发货      |               |
		|  000007  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  支付宝    |  100.00   |          |                     | 0000002,1    |     50.00      |jobs,完成     |   已完成      |       今天    |
		|  000008  | 今天  |    今天      | bill     | 商品2,1        |   支付    |  支付宝    |  100.00   |          | 优惠券,coupon1_id_2 |              |     10.00      |jobs,退款     |   退款中      |       今天    |
		|  000009  | 今天  |              | bill     | 商品3,1        |           |  微信支付  |  100.00   |   100    |                     |              |     50.00      |              |   待支付      |               |
		|  000010  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  微信支付  |  100.00   |          |                     |              |   100.00       |jobs,完成退款 |   退款成功    |       今天    |
		|  000011  | 今天  |    今天      | bill     | 商品3,1        |   支付    |  货到付款  |  100.00   |          |                     |              |     50.00      |jobs,取消     |   已取消      |               |
		|  000012  | 今天  |    今天      | bill     | 商品3,1        |           |  微信支付  |  100.00   |          | 优惠券,coupon1_id_3 |              |    0.00        |jobs,取消     |   已取消      |       今天    |
		|  000013  | 今天  |    今天      | bill     | 商品1,红色 S,1 |   支付    |  货到付款  |  100.00   |          |                     | 0000001,1    |     10.00      |jobs,取消     |   已取消      |               |

	Given jobs登录系统
	#查询下单时间
	When jobs根据给定条件查询订单
		"""
		{
			"date":"3天前-1天前"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000005"
		},{
			"order_no":"000004"
		},{
			"order_no":"000003"
		},{
			"order_no":"000002"
		},{
			"order_no":"000001"
		}]
		"""

	When jobs根据给定条件查询订单
		"""
		{
			"date":"5天前-4天前"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[]
		"""
	#查询付款时间
	When jobs根据给定条件查询订单
		"""
		{
			"payment_time":"今天-明天"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000013"
		},{
			"order_no":"000012"
		},{
			"order_no":"000011"
		},{
			"order_no":"000010"
		},{
			"order_no":"000008"
		},{
			"order_no":"000007"
		},{
			"order_no":"000006"
		},{
			"order_no":"000002"
		}]
		"""
	When jobs根据给定条件查询订单
		"""
		{
			"payment_time":""
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000013"
		},{
			"order_no":"000012"
		},{
			"order_no":"000011"
		},{
			"order_no":"000010"
		},{
			"order_no":"000009"
		},{
			"order_no":"000008"
		},{
			"order_no":"000007"
		},{
			"order_no":"000006"
		},{
			"order_no":"000005"
		},{
			"order_no":"000004"
		},{
			"order_no":"000003"
		},{
			"order_no":"000002"
		},{
			"order_no":"000001"
		}]
		"""
	#查询发货时间
	When jobs根据给定条件查询订单
		"""
		{
			"delivery_time":"2天前-1天前"
		}
		"""
  # TODO 需要去完善，这个地方的发货是存在问题的
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000004"
		},{
			"order_no":"000003"
		}]
		"""
	When jobs根据给定条件查询订单
		"""
		{
			"product_name": "商品3",
			"delivery_time":"2天前-今天"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000012"
		},{
			"order_no":"000010"
		},{
			"order_no":"000007"
		},{
			"order_no":"000002"
		}]
		"""
	When jobs根据给定条件查询订单
		"""
		{
			"order_status": "已取消",
			"delivery_time":"7天前-今天"
		}
		"""
	Then jobs可以看到订单列表
		"""
		[{
			"order_no":"000012"
		}]
		"""
