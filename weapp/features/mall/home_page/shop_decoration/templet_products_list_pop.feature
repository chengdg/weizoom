#_author_:师帅 15/10/12
#editor 新新 2015.10.14


Feature:自定义模块——【基础模块】商品列表-页面

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分组1"
		},{
			"name": "分组2"
		},{
			"name": "分组3"
		},{
			"name": "分组4"
		},{
			"name": "分类5"
		},{
			"name": "分类6"
		},{
			"name": "分类7"
		},{
			"name": "分类8"
		},{
			"name": "分类9"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1可单行显示",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 4.0
		},{
			"name": "商品5",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 5.0
		},{
			"name": "商品6",
			"category": "分组1,分组2,分组3",
			"status":"上架",
			"price": 6.0
		},{
			"name": "商品7",
			"category": "分组1,分组2,分组3",
			"status":"下架",
			"price": 7.0
		}]
		"""

Scenario:1选择商品分类窗体：商品分类列表搜索、添加新商品分类
	#选择商品分类名称的搜索
	#模糊匹配
	When jobs按商品分类名称搜索
		"""
		[{
			"search":"分类"
		}]
		"""
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		}]
		"""
	#完全匹配
	When jobs按商品分类名称搜索
		"""
		[{
			"search": "分类6"
		}]
		"""
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "分类6"
		}]
		"""
	#空搜索
	When jobs按商品分类名称搜索
		"""
		[{
			"search": ""
		}]
		"""
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		},{
			"name": "分组2"
		}]
		"""
	#添加新分类
	When jobs添加商品分类
		"""
		[{
			"name":"新分组"
		}]
		"""
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "新分组"
		},{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		}]
		"""

Scenario:2 商品分类选择列表分页
	When jobs获取商品分类选择列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		},{
			"name": "分组2"
		}]
		"""
	Then jobs获取商品列表模块商品分类选择列表显示共2页
	When jobs访问商品分类列表第1页
	Then jobs获取商品分类选择列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		},{
			"name": "分组2"
		}]
		"""
	When jobs在微页面浏览'下一页'商品分类
	Then jobs获取商品分类选择列表
		"""
		[{
			"name": "分组1"
		}]
		"""
	When jobs在微页面浏览'上一页'商品分类
	Then jobs获取商品分类列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		},{
			"name": "分组2"
		}]
		"""

Scenario:3 分类管理修改商品名，商品列表中使用该分类的商品来源，也应该同步修改

	#商品列表模块显示个数'9','详细列表'样式,'默认样式'
	When jobs创建微页面
		"""
		[{	"title":{
				"name": "微页面标题1"
			},
			"products_source": {
				"items":[{
					"products_source_name":"分组2"
				}],
				"display_count":"9",
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"items":[{
					"name":"商品1可单行显示",
					"price": 1.0
					},{
					"name":"商品2可两行显示",
					"price": 2.0
					},{
					"name":"商品3不可两行显示",
					"price": 3.0
					},{
					"name":"商品4",
					"price": 4.0
					},{
					"name":"商品5",
					"price": 5.0
					},{
					"name":"商品6",
					"price": 6.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""

	#修改商品分类名称
	When jobs更新商品分类'分组2'为
		"""
		{
			"name":"分组2——修改"
		}
		"""
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组3"
		},{
			"name": "分组2——修改"
		}]
		"""
	When jobs删除商品分类'分组3'
	Then jobs在微页面获得商品分类列表
		"""
		[{
			"name": "分类9"
		},{
			"name": "分类8"
		},{
			"name": "分类7"
		},{
			"name": "分类6"
		},{
			"name": "分类5"
		},{
			"name": "分组4"
		},{
			"name": "分组2——修改"
		},{
			"name": "分组1"
		}]
		"""
