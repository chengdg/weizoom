# __author__ : "师帅"
Feature:product_batch_shelves
		Jobs能通过管理系统在商城中对“商品”进行批量上架，批量下架


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
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 12:00",
			"sort": 0,
			"shelve_type": "上架"
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"price": 30.0,
			"stock_type": "无限",
			"sort":1,
			"create_time": "2015-08-02 12:00",
			"shelve_type": "上架"
		}, {
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":2,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "上架"
		}, {
			"name": "武昌鱼",
			"category": "分类3",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-07-31 12:00",
			"shelve_type": "下架"
		}, {
			"name": "水煮肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "无限",
			"create_time": "2015-07-30 12:00",
			"shelve_type": "下架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}]
	"""

Scenario:1 对上架商品进行批量下架
	When jobs获取在售商品列表
	"""
		[{
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":2,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "上架"
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"price": 30.0,
			"stock_type": "无限",
			"sort":1,
			"create_time": "2015-08-02 12:00",
			"shelve_type": "上架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}, {
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 12:00",
			"shelve_type": "上架"
		}]
	"""
	And jobs对上架商品进行批量下架
	Then jobs能在待售商品中获取商品列表
	"""
		[{
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "下架"
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"price": 30.0,
			"stock_type": "无限",
			"create_time": "2015-08-02 12:00",
			"shelve_type": "下架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}, {
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 12:00",
			"shelve_type": "下架"
		}, {
			"name": "武昌鱼",
			"category": "分类3",
			"price": 30.0,
			"stock_type": "有限",
			"create_time": "2015-07-31 12:00",
			"shelve_type": "下架"
		}, {
			"name": "水煮肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "无限",
			"create_time": "2015-07-30 12:00",
			"shelve_type": "下架"
		}]
	"""

Scenario:2 对下架商品进行批量上架
	When jobs获取待售商品列表
	"""
		[{
			"name": "武昌鱼",
			"category": "分类3",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-07-31 12:00",
			"shelve_type": "下架"
		}, {
			"name": "水煮肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "无限",
			"create_time": "2015-07-30 12:00",
			"shelve_type": "下架"
		}]
	"""
	And jobs对待售商品批量上架
	Then jobs获取在售商品列表
	"""
		[{
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":2,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "上架"
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"price": 30.0,
			"stock_type": "无限",
			"sort":1,
			"create_time": "2015-08-02 12:00",
			"shelve_type": "上架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}, {
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 12:00",
			"shelve_type": "上架"
		}, {
			"name": "武昌鱼",
			"category": "分类3",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-07-31 12:00",
			"shelve_type": "上架"
		}, {
			"name": "水煮肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "无限",
			"create_time": "2015-07-30 12:00",
			"shelve_type": "上架"
		}]
	"""

Scenario:3待售商品上架后，排序重复，自动变为0
	When jobs下架商品“叫花鸡”
	And jobs修改商品“东坡肘子”
	"""
		[{
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 12:00",
			"sort": 1,
			"shelve_type": "上架"
		}]
	"""


	Then jobs获取在售商品列表
	"""
		[{
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":2,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "上架"
		}, {
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 12:00",
			"sort": 1,
			"shelve_type": "上架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}]
	"""
	When jobs对待售商品批量上架
	Then jobs获取在售商品列表
	"""
		[{
			"name": "红烧肉",
			"category": "分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":2,
			"create_time": "2015-08-01 12:00",
			"shelve_type": "上架"
		}, {
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"create_time": "2015-08-03 12:00",
			"sort": 1,
			"shelve_type": "上架"
		}, {
			"name": "梅菜扣肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort": 0,
			"create_time": "2015-08-03 18:00",
			"shelve_type": "上架"
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"price": 30.0,
			"stock_type": "无限",
			"sort":0,
			"create_time": "2015-08-02 12:00",
			"shelve_type": "上架"
		}, {
			"name": "武昌鱼",
			"category": "分类3",
			"price": 30.0,
			"stock_type": "有限",
			"stocks": 3,
			"sort":0,
			"create_time": "2015-07-31 12:00",
			"shelve_type": "上架"
		}, {
			"name": "水煮肉",
			"category": "分类1,分类2,分类3",
			"price": 20.0,
			"stock_type": "无限",
			"sort":0,
			"create_time": "2015-07-30 12:00",
			"shelve_type": "上架"
		}]
	"""