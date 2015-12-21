# __author__ : "师帅"
#editor:王丽 2015.10.13

Feature:商品批量上下架
"""
	Jobs能通过管理系统在商城中对“商品”进行批量上架，批量下架
"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "东坡肘子",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0,
			"shelve_type": "上架"
		}, {
			"name": "叫花鸡",
			"price": 30.0,
			"stock_type": "无限",
			"display_index":1,
			"shelve_type": "上架"
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index":2,
			"shelve_type": "上架"
		}, {
			"name": "武昌鱼",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"shelve_type": "下架"
		}, {
			"name": "水煮肉",
			"price": 20.0,
			"stock_type": "无限",
			"shelve_type": "下架"
		}, {
			"name": "梅菜扣肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0,
			"shelve_type": "上架"
		}]
		"""

@mall2 @product @saleingProduct @toSaleProduct
Scenario:1 对上架商品进行批量下架
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "叫花鸡",
			"price": 30.0,
			"stock_type": "无限",
			"display_index":1
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stocks": 3,
			"display_index":2
		}, {
			"name": "梅菜扣肉",
			"price": 20.0,
			"stocks": 3
		}, {
			"name": "东坡肘子",
			"price": 20.0,
			"stocks": 3,
			"display_index": 0
		}]
		"""
	When jobs暂停1秒
	And jobs批量下架商品
		"""
		[
			"红烧肉",
			"叫花鸡",
			"梅菜扣肉",
			"东坡肘子"
		]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "梅菜扣肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"name": "叫花鸡",
			"price": 30.0,
			"stock_type": "无限"
		}, {
			"name": "东坡肘子",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"name": "水煮肉",
			"price": 20.0,
			"stock_type": "无限"
		}, {
			"name": "武昌鱼",
			"price": 30.0,
			"stock_type": "有限"
		}]
		"""

# __editor__ : "新新"待售商品上架后,排序为0
@mall2 @product @saleingProduct @toSaleProduct
Scenario:2 对下架商品进行批量上架
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水煮肉",
			"price": 20.0,
			"stock_type": "无限"
		}, {
			"name": "武昌鱼",
			"price": 30.0,
			"stocks": 3
		}]
		"""
	When jobs批量上架商品
		"""
		[
			"武昌鱼",
			"水煮肉"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "叫花鸡",
			"price": 30.0,
			"stock_type": "无限",
			"display_index":1
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index":2
		}, {
			"name": "梅菜扣肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0
		}, {
			"name": "水煮肉",
			"price": 20.0,
			"stock_type": "无限",
			"display_index": 0
		}, {
			"name": "武昌鱼",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0
		}, {
			"name": "东坡肘子",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0
		}]
		"""

@mall2 @product @saleingProduct @toSaleProduct
Scenario:3 待售商品上架后，排序重复，自动变为0
	When jobs'下架'商品'叫花鸡'
	And jobs更新商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"price": 20.0,
			"display_index": 1,
			"stocks": 3
		}
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "东坡肘子",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 1
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index":2
		}, {
			"name": "梅菜扣肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0
		}]
		"""
	When jobs批量上架商品
		"""
		[
			"水煮肉",
			"武昌鱼"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "东坡肘子",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 1
		}, {
			"name": "红烧肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index":2
		}, {
			"name": "梅菜扣肉",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index": 0
		}, {
			"name": "水煮肉",
			"price": 20.0,
			"stock_type": "无限",
			"display_index":0
		}, {
			"name": "武昌鱼",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"display_index":0
		}]
		"""
