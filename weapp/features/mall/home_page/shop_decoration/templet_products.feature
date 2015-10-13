#_author_:师帅 15/10/12



Feature:自定义模块——【基础模块】商品-页面
	"""
	#设置一个列表样式的商品展示区，只能选择到上架的商品设置商品列表展示区
	#1、选择商品窗体规则
	#（1）可以选择'在售'的所有商品
	#（2）'在售'的所有商品按照'创建时间'倒序排列
	#（3）商品名称过长显示不全的"..."方式显示
	#（4）可以多选商品
	#（5）一个商品可以重复选择
	#（6）搜索模糊匹配'商品名称'
	#(7) 在售商品列表分页显示，每页8个
	#（8）'新增商品'功能，打开新页面,进入'添加新商品'页，添加新商品，刷新之后在当前选择窗体中出现
	#2、小图、一大两小的模式，当商品数量不够整组的时候，空缺的商品位置，空缺显示
	#3、删除中间的商品后，后面的自动补齐
	#（例如：一大两小，删除大图后，左下小图补到上方大图，右下小图补到左下小图）
	#4、商品下架、删除之后,使用此商品的商品模板和使用商品模板的地方同步删除此商品，后面的商品依次补齐
	# 5、修改商品信息后，对应使用此商品的商品模板和使用商品模板的地方对应修改
	# 6、商品如果参加了促销活动显示促销价格
	"""


Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1可单行显示",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"shelve_type":"下架",
			"price": 4.0
		}]
		"""
	Then jobs在微页面获取'在售'商品选择列表
		"""
		[{
			"name":"商品3不可两行显示"
		},{
			"name":"商品2可两行显示"
		},{
			"name":"商品1可单行显示"
		}]
		"""

@termite2
Scenario:4 商品管理'下架'、'删除'商品
	When jobs创建微页面
		"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items":[{
					"name":"商品3不可两行显示",
					"price": 3.0
					},{
					"name":"商品1可单行显示",
					"price": 1.0
					},{
					"name":"商品2可两行显示",
					"price": 2.0
					}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items" [{
					"name":"商品3不可两行显示",
					"price": 3.0
					},{
					"name":"商品1可单行显示",
					"price": 1.0
					},{
					"name":"商品2可两行显示",
					"price": 2.0
					}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品1可单行显示",
					"price": 1.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	When jobs-下架商品'商品3不可两行显示'
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品1可单行显示",
					"price": 1.0
					},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""

	When jobs-永久删除商品'商品2可两行显示'
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品1可单行显示",
					"price": 1.0
					}],
					"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
				}
		}
		"""

@termite2
Scenario:5 商品管理'修改'商品
	When jobs创建微页面
		"""
		[{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items" [{
				"name":"商品3不可两行显示",
				"price": 3.0
				},{
				"name":"商品1可单行显示",
				"price": 1.0
				},{
				"name":"商品2可两行显示",
				"price": 2.0
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"true",
			"show_price":"true"
			}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
						"name":"商品1可单行显示",
						"price": 1.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
				}
			}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品1可单行显示",
					"price": 1.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	#修改商品价格和名称
	When jobs更新商品'商品2可两行显示'
		"""
		{
			"name":"修改后——商品2可两行显示",
			"price":"20.0"
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品1可单行显示",
					"price": 1.0
				},{
					"name":"修改后——商品2可两行显示",
					"price": 20.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""

@termite2
Scenario:6 商品修改，删除
	When jobs创建微页面
		"""
		[{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品1可单行显示",
					"price": 1.0
				},{
					"name":"修改后——商品2可两行显示",
					"price": 20.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}]
		"""

Scenario:6 商品修改，删除
	When jobs创建微页面
		"""
		[{
			"title": {
				"name": "微页面标题1"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品1可单行显示",
					"price": 1.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	#删除一个商品
	When jobs编辑微页面'微页面标题1'
		"""
		{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items" [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			}
		}
		"""
	#切换样式
	When jobs编辑微页面'微页面标题1'
		"""
		{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"小图",
				"list_style2":"简洁样式",
				"show_price":"true"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{	
			"title": {
				"name": "微页面标题1"
			},
			"products": {
				"items": [{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"小图",
				"list_style2":"简洁样式",
				"show_price":"true"
			}
		}
		"""
	#删除商品模块
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}
		}
		"""
	
