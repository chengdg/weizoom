# __author__ : "新新 2015.10.21"
# _edit_ : "雪静 2015.11.09"
Feature: 被删除跳转页面
"""
	bill能在接收到正确的跳转提示及页面

	【商品分组】：
				bill在删除的分组页面,显示'404页面'
				bill在空的分组页面,显示'无商品页面'
				bill在分组下的商品全部下架,显示'无商品页面'
				bill在分组下的商品全部删除,显示'无商品页面'
					#并且都手机端都显示上方分类表头
	【商品】：bill在删除商品页面,显示'404页面'
	"根据bug-5865补充"
	【404页面-返回首页】：
				1.设置店铺主页开启，点击'404页面-返回首页'
				返回到店铺主页
				2.店铺主页没有开启，点击'404页面-返回首页'
				返回到商品列表页
	【无商品页面-去逛逛】：
				1.设置店铺主页开启，点击'无商品页面-去逛逛'
				返回到店铺主页
				2.店铺主页没有开启，点击'无商品页面-去逛逛'
				返回到商品列表页
"""

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
			"name": "商品1",
			"shelve_type":"上架",
			"categories": "分类2"
		}, {
			"name": "商品2",
			"shelve_type":"上架",
			"categories": "分类1"
		}, {
			"name": "商品3",
			"shelve_type":"上架",
			"categories": "分类1"
		}, {
			"name": "商品4",
			"shelve_type":"上架",
			"categories": ""
		}]
		"""

	And bill关注jobs的公众号

Scenario: 1 删除分组

	#bill在删除的分组页面,显示'404页面'
	#jobs开启店铺主页
	When bill访问jobs的webapp:ui
	Then bill浏览jobs的webapp的'全部'商品分类:ui
		|   name   |
		|  分类1   |
		|  分类2   |
		|  分类3   |
	
	Given jobs登录系统
	When jobs开启店铺主页
	When jobs删除商品分类'分类1'
	When bill访问jobs的webapp:ui
	When bill浏览jobs的webapp的'分类1'商品列表页:ui
	Then bill获得webapp商品列表'404页面':ui
	When bill-返回首页
	Then bill获得jobs的webapp'店铺首页':ui


Scenario: 2 分组下的商品全部下架
	#bill在分组下的商品全部下架,显示'无商品页面'
	#jobs开启店铺主页
	Given jobs登录系统
	When jobs开启店铺主页
	When jobs-下架商品'商品1'
	When bill访问jobs的webapp:ui
	When bill浏览jobs的webapp的'分类2'商品列表页:ui
	Then bill获得webapp商品列表'无商品页面':ui


	#bill在空的分组页面,显示'无商品页面'
	When bill浏览jobs的webapp的'分类3'商品列表页:ui
	Then bill获得webapp商品列表'无商品页面':ui
	When bill-去逛逛
	Then bill获得jobs的webapp'店铺首页':ui

Scenario: 3 分组下的商品删除
	#bill在分组下的商品全部删除,显示'无商品页面'
	#jobs不开启店铺首页

	Given jobs登录系统
	When jobs-永久删除商品'商品2'
	When bill访问jobs的webapp:ui
	When bill浏览jobs的webapp的'分类1'商品列表页:ui
	Then bill获得webapp商品列表:ui
		|   name   |
		|  商品3   |
	
	When jobs-永久删除商品'商品3'
	When bill访问jobs的webapp:ui
	When bill浏览jobs的webapp的'分类1'商品列表页:ui
	Then bill获得webapp商品列表'无商品页面':ui
	When bill-去逛逛
	Then bill获得jobs的webapp'商品列表页':ui

Scenario: 4 删除商品
	#bill在删除商品页面,显示'404页面'
	#jobs不开启店铺首页

	When bill访问jobs的webapp:ui
	When bill浏览jobs的webapp的'分类2'商品列表页:ui
	Then bill获得webapp商品列表:ui
		|   name   |
		|  商品1   |
	Given jobs登录系统
	When jobs-永久删除商品'商品1'
	When bill访问jobs的webapp:ui
	Then bill获得webapp商品列表'404页面':ui
	When bill-返回首页
	Then bill获得jobs的webapp'商品列表页':ui

