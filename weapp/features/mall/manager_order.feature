@func:webapp.modules.mall.order
Feature:订单管理
	Jobs能通过管理系统获取到订单列表(商品详情、过滤)、订单详情(发货、完成等)

Background:
	Given jobs登录系统
	And jobs已有微众卡支付权限
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
			"model": {
				"models": {
					"standard": {
						"price": 9.9,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}, {
			"name": "商品2",
			"model": {
				"models": {
					"standard": {
						"price": 10,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""
	And jobs已创建微众卡
		"""
		{
			"cards": [{
				"id": "0000001",
				"password": "1234567",
				"status": "未激活",
				"price": 8.7
			}]
		}
		"""

	And jobs已添加支付方式
		"""
		[{
			"type": "微众卡支付"
		}, {
			"type": "货到付款"
		}]
		"""
	And bill关注jobs的公众号
	And jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券规则1",
			"money": "1",
			"count": 0,
			"expire_days": "1",
			"using_limit": "无限制",
			"start_date": "前天",
			"end_date": "后天"
		}, {
			"name": "优惠券规则2",
			"money": "10",
			"count": 2,
			"expire_days": "1",
			"using_limit": "无限制",
			"start_date": "前天",
			"end_date": "后天"
		}, {
			"name": "优惠券规则3",
			"money": "10",
			"count": 3,
			"expire_days": "2",
			"using_limit": "满10元可以使用",
			"start_date": "前天",
			"end_date": "后天"
		}, {
			"name": "过期优惠券规则",
			"money": "1",
			"count": 4,
			"expire_days": "1",
			"using_limit": "无限制",
			"start_date": "前天",
			"end_date": "昨天"
		}]
		"""
	When jobs为会员发放优惠券
		'''
		{
			"name": "优惠券规则1",
			"count": 1,
			"members": ["bill"]
		}
		'''
	Then jobs获得优惠券规则列表
		"""
		[{
			"coupon_rule": "过期优惠券规则",
			"money": "1.00",
			"create_date": "前天",
			"expire_date": "昨天",
			"status": "已结束"
		}, {
			"coupon_rule": "优惠券规则3",
			"money": "10.00",
			"create_date": "前天",
			"expire_date": "后天",
			"status": "进行中"
		}, {
			"coupon_rule": "优惠券规则2",
			"money": "10.00",
			"create_date": "前天",
			"expire_date": "后天",
			"status": "进行中"
		}, {
			"coupon_rule": "优惠券规则1",
			"money": "1.00",
			"create_date": "前天",
			"expire_date": "后天",
			"status": "进行中"
		}]
		"""
@mall @mall2 @mall.order @zy_mo1 @eugene
Scenario: 购买商品后，可以获得订单列表
	bill购买了商品1(只下单, 未支付)和商品2(已支付)

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}],
			"customer_message": "bill的订单备注2"
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Given jobs登录系统
	Then jobs可以看到订单列表
		"""
		[{
			"status": "待发货",
			"price": "10.00",
			"customer_message": "bill的订单备注2",
			"buyer": "bill",
			"products": [{
				"product_name": "商品2",
				"count": 1,
				"total_price": "10.00"
			}]
		}, {
			"status": "待支付",
			"price": 9.9,
			"customer_message": "bill的订单备注1",
			"buyer": "bill",
			"products": [{
				"product_name": "商品1",
				"count": 1,
				"total_price": "9.90"
			}]
		}]
		"""

@mall @mall2 @mall.order @mall_a @zy_mo2
Scenario: 购买商品后，管理员通过后台管理系统可以查看订单详情
	bill购买商品后
	1. 能看到订单详情
	2. 能在不同状态下执行各种操作

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"customer_message": "bill的订单备注1"
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "待支付",
			"actions": ["取消", "支付"],
			"total_price": 9.9,
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区 泰兴大厦",
			"customer_message": "bill的订单备注1",
			"products": [{
				"name": "商品1",
				"count": 1,
				"total_price": 9.9
			}]
		}
		"""
	When jobs'支付'最新订单
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "待发货",
			"actions": ["发货", "取消"]
		}
		"""
	When jobs对最新订单进行发货
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已发货",
			"actions": ["完成", "修改物流", "取消"]
		}
		"""
	When jobs'完成'最新订单
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已完成",
			"actions": ["修改物流", "取消"]
		}
		"""
	When jobs'取消'最新订单
		"""
		{
			"reason": "不想要了"
		}
		"""
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已取消",
			"actions": [],
			"reason": "不想要了"
		}
		"""

@mall @mall.order @zy_mo3
#验证待发货状态的订单可以取消
Scenario: 购买商品后并支付,管理员通过后台管理系统点击'取消'取消订单
	bill购买商品后
	1. 能取消订单
	2. 取消订单后库存回退
	3. 取消订单之后使用的优惠券回退
	4. 取消订单之后使用的积分回退
	5. 取消订单之后使用的微众卡回退

	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"一元等价的积分数量": 100,
			"订单积分抵扣上限": 100
		}
		"""
	When jobs给id为'0000001'的微众卡激活
	When bill访问jobs的webapp
	When bill获得jobs的100会员积分
	Then bill在jobs的webapp中拥有100会员积分
	When bill购买jobs的商品
		"""
		{

			"coupon": "coupon_1",
			"integral": 50,
			"products": [{
				"name": "商品1",
				"count": 1
			}],
			"weizoom_card": [{
				"card_name": "0000001",
				"card_pass": "1234567"
			}]
		}
		"""
	Given jobs登录系统
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"stocks": 99
					}
				}
			}
		}
		"""

	Then jobs能获得优惠券'优惠券规则1'的码库
		'''
		{
			"coupon_1": {
				"money": 1.0,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			}
		}
		'''

	Then jobs能获取微众卡'0000001'
		"""
		{
			"status": "已用完",
			"price": 0
		}
		"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有50会员积分
	Given jobs登录系统
	When jobs'取消'最新订单
		"""
		{
			"reason": "不想要了"
		}
		"""
	Then jobs可以获得最新订单详情
		"""
		{
			"order_type": "普通订单",
			"status": "已取消",
			"actions": [],
			"reason": "不想要了"
		}
		"""
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"stocks": 100
					}
				}
			}
		}
		"""
	Then jobs能获得优惠券'优惠券规则1'的码库
		'''
		{
			"coupon_1": {
				"money": 1.0,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			}
		}
		'''
	Then jobs能获取微众卡'0000001'
		"""
		{
			"status": "已使用",
			"price": 8.7,
			"log": [{
				"merchant": "jobs",
				"order_id": "使用",
				"price": 8.7
			}, {
				"merchant": "jobs",
				"order_id": "返还",
				"price": -8.7
			}]
		}
		"""
	When bill访问jobs的webapp
	Then bill在jobs的webapp中拥有100会员积分

