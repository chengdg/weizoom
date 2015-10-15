#_edit_:张三香
#editor:王丽 2015.10.13

Feature: 上下架管理
	"""
		Jobs能通过管理系统对商品进行上下架管理
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"categories": "分类1,分类2",
			"price":100.00,
			"shelve_type": "上架"
		},{
			"name": "商品2",
			"categories": "分类1",
			"price":200.00,
			"shelve_type": "上架"
		}]
		"""
	And bill关注jobs的公众号

@mall2 @product @saleingProduct @toSaleProduct   @mall.product
Scenario: 1 下架商品对后台及手机端商品列表的影响
	Jobs下架商品后
	1. jobs不能获取含有该商品的商品列表
	2. bill在webapp中不能看到该商品

	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品2"
		},{
			"name": "商品1"
		}]
		"""
	And jobs能获得'待售'商品列表
		"""
		[]
		"""
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品2"
		}, {
			"name": "商品1"
		}]
		"""

	#jobs下架商品2，jobs不能获取含有该商品的'在售'商品列表
	Given jobs登录系统
	When jobs-下架商品'商品2'
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品1"
		}]
		"""
	And jobs能获得'待售'商品列表
		"""
		[{
			"name": "商品2"
		}]
		"""

	#bill在webapp中不能看到商品2
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品1"
		}]
		"""

@mall2 @product @saleingProduct @toSaleProduct   @mall.product
Scenario: 2 下架后再上架商品对后台及手机端商品列表的影响
	Jobs下架商品，并再次上架后
	1. jobs能获取含有该商品的商品列表
	2. bill在webapp中能看到该商品

	Given jobs登录系统
	When jobs-下架商品'商品2'
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品1"
		}]
		"""
	And jobs能获得'待售'商品列表
		"""
		[{
			"name": "商品2"
		}]
		"""

	#bill在webapp中不能看到商品2
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品1"
		}]
		"""

	#jobs再上架商品2，bill在webapp中能看到该商品
	Given jobs登录系统
	When jobs-上架商品'商品2'
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品2"
		},{
			"name": "商品1"
		}]
		"""
	And jobs能获得'待售'商品列表
		"""
		[]
		"""
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then webapp页面标题为'商品列表'
	And bill获得webapp商品列表
		"""
		[{
			"name": "商品2"
		},{
			"name": "商品1"
		}]
		"""



