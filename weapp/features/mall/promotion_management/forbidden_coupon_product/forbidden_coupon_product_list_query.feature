#_author_:张三香
#editor:雪静 2015.10.16
Feature:禁用优惠券商品列表查询

Background:
	Given jobs登录系统
	When jobs已添加商品
		|   name    |  bar_code  | shelve_type  |
		|   商品1   |            |   上架       |
		|   商品2   |  1234562   |   上架       |
		|   商品3   |  1234563   |   上架       |
	When jobs添加禁用优惠券商品
		| products  |  start_date  |   end_date  |is_permanant_active  |
		| 商品1     |2015-8-10     | 明天        | 0                   |
		| 商品2     |              |             | 1                   |
		| 商品3     | 明天         |  3天后      | 0                   |

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 禁用优惠券商品列表查询
	Given jobs登录系统
	#空查询、默认查询
	When jobs设置查询条件
		"""
		{}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		},{
			"product_name": "商品2"
		},{
			"product_name": "商品1"
		}]
		"""

	#商品名称
	#查询结果为空
	When jobs设置查询条件
		"""
		{
			"product_name":"商 品"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""
	#完全匹配
	When jobs设置查询条件
		"""
		{
			"product_name":"商品1"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品1"
		}]
		"""
	#部分匹配
	When jobs设置查询条件
		"""
		{
			"product_name":"商品"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		},{
			"product_name": "商品2"
		},{
			"product_name": "商品1"
		}]
		"""

	#商品编码
	#查询结果为空
	When jobs设置查询条件
		"""
		{
			"bar_code":"123"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""
	#精确匹配
	When jobs设置查询条件
		"""
		{
			"bar_code":"1234563"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		}]
		"""

	#起止时间
	#查询结果为空
	When jobs设置查询条件
		"""
		{
			"start_date":"2015-07-15",
			"end_date":"2015-08-10"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[]
		"""
	#查询结果非空
	When jobs设置查询条件
		"""
		{
			"start_date":"2015-07-15",
			"end_date":"明天"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品1"
		}]
		"""

	#禁用状态
	When jobs设置查询条件
		"""
		{
			"status":"进行中"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		},{
			"product_name": "商品2"
		},{
			"product_name": "商品1"
		}]
		"""

	#组合查询
	When jobs设置查询条件
		"""
		{
			"product_name":"商品3",
			"bar_code":"1234563",
			"status":"未开始",
			"start_date":"明天",
			"end_date":"3天后"
		}
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "商品3"
		}]
		"""