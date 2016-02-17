#watcher:zhangsanxiang@weizoom.com,fengxuejing@weizoom.com,benchi@weizoom.com
#author: 张三香
#editor: 雪静 2015.10.15

Feature:结束禁用优惠券商品

"""
	说明：
	1、点击【结束】弹出确认弹层。确认结束后，该商品将被移出禁用优惠券商品列表
	2、当商品过了有效期后，该商品将会自动移出禁用优惠券商品列表。
	3、批量结束未开始和进行中的禁用优惠券商品
"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"bar_code":"1234561",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"商品2",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"商品3",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		}]
		"""
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"商品1"
			}],
			"start_date": "明天",
			"end_date": "2天后",
			"is_permanant_active": 0
		},{
			"products":[{
				"name":"商品2"
			}],
			"start_date": "今天",
			"end_date": "1天后",
			"is_permanant_active": 0
		},{
			"products":[{
				"name":"商品3"
			}],
			"start_date": "",
			"end_date": "",
			"is_permanant_active": 1
		}]
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 1 手动结束单个禁用优惠券商品
	Given jobs登录系统
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3",
			"product_price": 100.0,
			"status": "进行中",
			"is_permanant_active": 1
		},{
			"product_name": "商品2",
			"product_price": 100.0,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "1天后"
		},{
			"product_name": "商品1",
			"product_price": 100.0,
			"status": "未开始",
			"start_date": "明天",
			"end_date": "2天后"
		}]
		"""
	#结束'永久有效'的禁用优惠券商品
	When jobs结束单个禁用优惠券商品'商品3'
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品2"
		},{
			"product_name": "商品1"
		}]
		"""
	#结束'进行中'的禁用优惠券商品
	When jobs结束单个禁用优惠券商品'商品2'
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品1"
		}]
		"""
	#结束'未开始'的禁用优惠券商品
	When jobs结束单个禁用优惠券商品'商品1'
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 2 批量结束多个禁用优惠券商品
	Given jobs登录系统
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3",
			"product_price": 100.0,
			"status": "进行中",
			"is_permanant_active": 1
		},{
			"product_name": "商品2",
			"product_price": 100.0,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "1天后"
		},{
			"product_name": "商品1",
			"product_price": 100.0,
			"status": "未开始",
			"start_date": "明天",
			"end_date": "2天后"
		}]
		"""
	#后面加一个“时”字，避免跟manage_mall_product_steps.py中的{user}批量{action}商品冲突
	When jobs批量结束禁用优惠券商品时
		"""
		[{
			"product_name": "商品3"
		},{
			"product_name": "商品2"
		},{
			"product_name": "商品1"
		}]
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 3 在查询结果中, 结束禁用优惠券商品
	#在'商品名称'的查询结果中,进行'结束'操作
	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"product_name":"商品3"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		}]
		"""
	When jobs结束单个禁用优惠券商品'商品3'
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""

	#在'商品编码'的查询结果中,进行'结束'操作
	When jobs设置查询条件
		"""
		{
			"bar_code":"1234561"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品1"
		}]
		"""
	When jobs结束单个禁用优惠券商品'商品1'
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""

