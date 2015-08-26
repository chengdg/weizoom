
#_author_:张三香

Feature:新建商品和下架商品时，待售商品列表排序校验
	#说明：
		#针对线上"bug3897"补充feature
		#bug3897:功能问题【待售商品管理】排序错乱
		#新建商品，保存后在待售商品列表第一个显示
		#在售商品下架后，在待售商品列表第一个显示

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
			[{
				"name": "商品0",
				"price": 20.0,
				"shelve_type": "上架"
			},{
				"name": "商品1",
				"price": 20.0,
				"shelve_type": "下架"
			}, {
				"name": "商品2",
				"price": 30.0,
				"shelve_type": "下架"
			}, {
				"name": "商品3",
				"price": 20.0,
				"shelve_type": "下架"
			}]
		"""

@product @toSaleProduct
Scenario: 1 新建商品,在待售商品列表中第一个显示
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
			[{
				"name": "商品3",
				"price": 20.0
			}, {
				"name": "商品2",
				"price": 30.0
			}, {
				"name": "商品1",
				"price": 20.0
			}]
		"""
	When jobs添加商品
		"""
			[{
				"name": "商品4",
				"price": 20.0,
				"shelve_type": "下架"
			}]
		"""
	Then jobs能获得'待售'商品列表
		"""
			[{
				"name": "商品4",
				"price": 20.0
			},{
				"name": "商品3",
				"price": 20.0
			}, {
				"name": "商品2",
				"price": 30.0
			}, {
				"name": "商品1",
				"price": 20.0
			}]
		"""

@product @toSaleProduct
Scenario: 2 下架商品,在待售商品列表中第一个显示
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
			[{
				"name": "商品3",
				"price": 20.0
			}, {
				"name": "商品2",
				"price": 30.0
			}, {
				"name": "商品1",
				"price": 20.0
			}]
		"""
	And jobs能获得'在售'商品列表
		"""
			[{
				"name":"商品0",
				"price":20.0
			}]
		"""
	When jobs-下架商品'商品0'
	Then jobs能获得'待售'商品列表
		"""
			[{
				"name": "商品0",
				"price": 20.0
			},{
				"name": "商品3",
				"price": 20.0
			}, {
				"name": "商品2",
				"price": 30.0
			}, {
				"name": "商品1",
				"price": 20.0
			}]
		"""
	And jobs能获得'在售'商品列表
		"""
		[]
		"""