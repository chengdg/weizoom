# _edit_ : "新新8.24"
@func:webapp.modules.mall.views.list_products
Feature: 在webapp中浏览商品列表
	bill能在webapp中看到jobs添加的"商品列表"

# _edit_ : "新新8.24"
@ui @ui-mall @ui-mall.webapp
Scenario: 浏览全部商品列表
	jobs添加商品后
	1. bill能在webapp中看到jobs添加的商品列表
	2. 商品按添加顺序倒序排序
	3. bill看不到被下架的商品
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}, {
			"name": "分类4"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品11",
			"categories": "分类1,分类2,分类3"
		}, {
			"name": "商品12",
			"categories": "分类1,分类2"
		}, {
			"name": "商品2",
			"categories": "分类2,分类3"
		}, {
			"name": "商品3"
		}, {
			"name": "商品4",
			"shelve_type": "下架"
		}]
		"""
	And bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
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
# _edit_ : "新新8.24"
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
	And bill关注jobs的公众号
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

# _edit_ : "新新8.24"
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
		}, {
			"name": "分类4"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品11",
			"categories": "分类1,分类2,分类3"
		}, {
			"name": "商品12",
			"categories": "分类1,分类2"
		}, {
			"name": "商品2",
			"categories": "分类2,分类3"
		}, {
			"name": "商品3"
		}, {
			"name": "商品4",
			"shelve_type": "下架"
		}]
		"""
	And bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'分类1'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""
	When bill浏览jobs的webapp的'分类2'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品2"
		}, {
			"name": "商品12"
		}, {
			"name": "商品11"
		}]
		"""
	When bill浏览jobs的webapp的'分类3'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
	And bill获得webapp商品列表:ui
		"""
		[{
			"name": "商品2"
		}, {
			"name": "商品11"
		}]
		"""
	When bill浏览jobs的webapp的'分类4'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
	And bill获得webapp商品列表:ui
		"""
		[]
		"""

# _edit_ : "新新8.24"
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
	And bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品列表页:ui
	Then webapp页面标题为'商品列表':ui
	And webapp页面上'不能'选择商品分类:ui

# _inert_ : "新新8.24"		
Scenario: 浏览会员价的商品列表
	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员",
		},{
			"name": "bill",
			"member_rank": "铜牌会员",
		}]
		"""
	
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"category": "分类1",
			"physical_unit": "包",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "商品1的简介",
			"detail": "商品1的详情",
			"remark": "商品1的备注",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"property": {},
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	And tom关注jobs的公众号
	And bill关注jobs的公众号
	#无会员折扣显示
	When tom访问jobs的webapp:ui
	And tom浏览jobs的webapp的'全部'商品页:ui
	Then webapp页面标题为'商品列表':ui
	Then tom获得webapp商品列表:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 11.0,
			"weight": 5.0,
			"stocks": "无限",
			"postage_config_name": "免运费"
		}
		"""
		#有会员折扣显示
	When bill访问jobs的webapp:ui
	And bill浏览jobs的webapp的'全部'商品页:ui
	Then webapp页面标题为'商品列表':ui
	Then bill获得webapp商品列表:ui
		"""
		{
			"name": "商品1",
			"detail": "商品1的详情",
			"price": 9.9,
			"weight": 5.0,
			"stocks": "无限",
			"postage_config_name": "免运费"
		}
		"""
