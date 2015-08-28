# __author__ : "王丽"

Feature: 会员管理-会员列表-会员详情-购买信息
"""
	针对线上BUG3740补充feature

	当前会员的购买信息（包含订单状态如下的订单：待发货、已发货、已完成、退款中、退款完成）
	（1）【购买金额】：当前会员的订单（包含订单状态如下的订单：待发货、已发货、已完成、退款中、退款完成）的实付金额之和
				=∑订单.实付金额[(订单.买家 = "当前会员") and (订单.状态 in {待发货、已发货、已完成、退款中、退款完成})]

	（2）【购买次数】：当前会员的订单（包含订单状态如下的订单：待发货、已发货、已完成、退款中、退款完成）的个数
				=∑订单.个数[(订单.买家 = "当前会员") and (订单.状态 in {待发货、已发货、已完成、退款中、退款完成})]

	（3）【平均客单价】：=【购买金额】/【购买次数】

	（4）当前会员的购买订单列表，（包含订单状态如下的订单：待发货、已发货、已完成、退款中、退款完成）
"""

Background:

	Given jobs登录系统

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100,
				"stock_type": "无限"
			},{
				"name": "商品2",
				"postage":15,
				"price":100,
				"stock_type": "无限"
			}]
			"""
		And jobs已添加支付方式
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
			},{
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""
		And bill关注jobs的公众号
		When 微信用户批量消费jobs的商品
			|    date      |    order_id    | consumer |    type   |businessman|   product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2015-01-01   | 对应订单编号01 | bill     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 		  |        | 110         |              | 110    | 0      | 0    | jobs,支付         |  待发货         |
			| 2015-01-02   | 对应订单编号02 | bill     |    购买   | jobs      | 商品2,2   | 未支付  | 支付宝         | 15      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,取消         |  已取消         |	
			| 2015-02-01   | 对应订单编号03 | bill     |    购买   | jobs      | 商品2,2   | 支付    | 支付宝         | 15      | 100      |          |        | 215         |              | 215    | 0      | 0    | jobs,发货         |  已发货         |
			| 2015-02-02   | 对应订单编号04 | bill     |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      |          |        | 110         |              | 0      | 110    | 0    | jobs,完成         |  已完成         |
			| 2015-02-04   | 对应订单编号05 | bill     |    购买   | jobs      | 商品1,1   | 未支付  | 微信支付       | 10      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,无操作       |  未支付         |
			| 2015-03-04   | 对应订单编号06 | bill     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      |          |        | 115         |              | 0      | 115    | 0    | jobs,退款         |  退款中         |
			| 2015-03-05   | 对应订单编号07 | bill     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          |        | 110         |              | 110    | 0      | 0    | jobs,完成退款     |  退款完成       |

@member
Scenario: 当前会员的"会员详情"的"购买信息"数据

	Given jobs登录系统
	
	When jobs访问bill会员详情
	Then jobs获得bill的购买信息
		"""
		[{
			"purchase_amount":660.00,
			"purchase_number":5,
			"customer_price":132.00
		}]
		"""
	Then jobs获得bill的订单列表
		|   order_id    | order_amount |    date    | order_status |
		|对应订单编号07 |    110.00    | 2015-03-05 | 退款完成     |
		|对应订单编号06 |    115.00    | 2015-03-04 | 退款中       |
		|对应订单编号05 |    110.00    | 2015-02-04 | 未支付       |
		|对应订单编号04 |    110.00    | 2015-02-02 | 已完成       |
		|对应订单编号03 |    215.00    | 2015-02-01 | 已发货       |
		|对应订单编号02 |    215.00    | 2015-01-02 | 已取消       |
		|对应订单编号01 |    110.00    | 2015-01-01 | 待发货       |
