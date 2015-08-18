@func:webapp.modules.mall.views.list_products
Feature: 在webapp中浏览商品列表
	bill能在webapp中看到jobs添加的"商品列表"

Background:
	Given jobs登录系统
	And bill关注jobs的公众号


@ui @ui-mall @ui-mall.webapp
Scenario: 浏览全部商品列表
	jobs添加商品后
	1. bill能在webapp中看到jobs添加的商品列表
	2. 商品按添加顺序倒序排序
	
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
			"name": "商品11",
			"category": "分类1"
		}, {
			"name": "商品12",
			"category": "分类1"
		}, {
			"name": "商品2",
			"category": "分类2"
		}, {
			"name": "商品3"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品列表页:ui
	Then webapp页面标题为'商品列表(全部)':ui
	And webapp页面上'能'选择商品分类:ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品2"
		}, {
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""

@ui @ui-mall @ui-mall.webapp
Scenario: 商品上下架影响商品列表
	jobs添加商品后
	1. 下架的商品不能出现在商品列表中
	2. 重新上架后的商品出现在商品列表中
	
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品11"
		}, {
			"name": "商品12"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3",
			"shelve_type": "下架"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品列表页:ui
	Then bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品2"
		}, {
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""
	Given jobs登录系统:ui
	When jobs更新商品'商品3':ui
		"""
		{
			"name": "商品3",
			"shelve_type": "上架"
		}	
		"""
	When bill浏览jobs的webapp的'全部'商品列表页:ui
	Then bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品2"
		}, {
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 按分类浏览商品
	jobs添加多个商品后
	1. bill能在webapp中按分类浏览商品
	2. 每个分类中"商品列表"会按照添加的顺序倒序排列
	
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
			"name": "商品11",
			"category": "分类1"
		}, {
			"name": "商品12",
			"category": "分类1"
		}, {
			"name": "商品2",
			"category": "分类2"
		}, {
			"name": "商品3"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'分类1'商品列表页:ui
	Then webapp页面标题为'商品列表(分类1)':ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""
	When bill浏览jobs的webapp的'分类2'商品列表页:ui
	Then webapp页面标题为'商品列表(分类2)':ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品2"
		}]
		"""
	When bill浏览jobs的webapp的'分类3'商品列表页:ui
	Then bill获得webapp商品列表:ui
		"""
		[]
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 浏览全部商品列表，无分类时，不能选择分类
	jobs没有创建分类，添加商品后
	1. 不能选择分类
	
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品11"
		}, {
			"name": "商品12"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
		}]
		"""
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品列表页:ui
	Then webapp页面标题为'商品列表(全部)':ui
	And webapp页面上'不能'选择商品分类:ui
