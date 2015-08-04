Feature: 上下架管理
	Jobs能通过管理系统对商品进行上下架管理

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

@mall.product
Scenario: 下架商品
	Jobs下架商品后
	1. jobs能获取含有该商品的商品列表
	2. bill在webapp中不能看到该商品


@mall.product
Scenario: 下架后再上架商品
	Jobs下架商品，并再次上架后
	1. jobs能获取含有该商品的商品列表
	2. bill在webapp中能看到该商品


@mall.product
Scenario: 下架商品影响购物车
	Jobs下架商品后
	1. bill购物车中改商品不再可见
	2. jobs再次上架后，bill购物车中该商品依然不可见
	