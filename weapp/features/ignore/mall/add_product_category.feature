Feature: 添加商品分类
	Jobs能通过管理系统为管理商城添加的"商品分类"

@ui-mall.product_category @ui-mall @ui
Scenario: 添加商品分类
	Jobs添加一组"商品分类"后，"商品分类列表"会按照添加的顺序倒序排列

	Given jobs登录系统:ui
	When jobs添加商品分类:ui
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	Then jobs能获取商品分类列表:ui
		"""
		[{
			"name": "分类3"
		}, {
			"name": "分类2"
		}, {
			"name": "分类1"
		}]
		"""
	Given bill登录系统:ui
	Then bill能获取商品分类列表:ui
		"""
		[]
		"""
