#_author_:王丽
#_edit_:新新

Feature:自定义模块——【基础模块】商品-页面
        设置一个列表样式的商品展示区，只能选择到上架的商品设置商品列表展示区
        1、选择商品窗体规则
        	（1）可以选择'在售'的所有商品
        	（2）'在售'的所有商品按照'创建时间'倒序排列
        	（3）商品名称过长显示不全的"..."方式显示
        	（4）可以多选商品
        	（5）一个商品可以重复选择
        	（6）搜索模糊匹配'商品名称'
        	 (7) 在售商品列表分页显示，每页8个
        	（8）'新增商品'功能，打开新页面,进入'添加新商品'页，添加新商品，刷新之后在当前选择窗体中出现
        2、小图、一大两小的模式，当商品数量不够整组的时候，空缺的商品位置，空缺显示
        3、删除中间的商品后，后面的自动补齐
          （例如：一大两小，删除大图后，左下小图补到上方大图，右下小图补到左下小图）
        4、商品下架、删除之后,使用此商品的商品模板和使用商品模板的地方同步删除此商品，后面的商品依次补齐
        5、修改商品信息后，对应使用此商品的商品模板和使用商品模板的地方对应修改
        6、商品如果参加了促销活动显示促销价格

Background:
	Given jobs登录系统
	And jobs已添加商品
		#商品1,商品2,商品3（上架状态）,商品4（下架状态）
		"""
		[{
			"name": "商品1可单行显示",
			"product_picture_id":"1",
			"create_time":"2015-05-02 9:00",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"product_picture_id":"2",
			"create_time":"2015-05-01 9:00",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示......",
			"product_picture_id":"3",
			"create_time":"2015-05-03 9:00",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"product_picture_id":"4",
			"create_time":"2015-05-04 9:00",
			"shelve_type":"下架",
			"price": 4.0
		}]	
		"""
	Then jobs获取'在售'商品选择列表
	"""
	[{
		"name":"商品3不可两行显示...",
		"create_time":"2015-05-03 9:00"
	},{
		"name":"商品1可单行显示",
		"create_time":"2015-05-02 9:00"
	},{
		"name":"商品2可两行显示",
		"create_time":"2015-05-01 9:00"
	}]
	"""

Scenario:1 选择在售商品窗体：在售商品列表、搜索、添加新商品
	
	#搜索功能,按商品名称搜索
		#模糊匹配搜索
			When jobs按商品名称搜索
			"""
			[{
				"search":"两行"
			}]
			"""
			Then jobs获取'在售'商品选择列表
			"""
			[{
				"name":"商品3不可两行显示......",
				"create_time":"2015-05-03 9:00"
			},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}]
			"""
		#完全匹配搜索
			When jobs按商品名称搜索
			"""
			[{
				"search":"商品2可两行显示"
			}]
			"""
			Then jobs获取'在售'商品选择列表
			"""
			[{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}]
			"""
		#空搜索
			When jobs按商品名称搜索
			"""
			[{
				"search":""
			}]
			"""
			Then jobs获取'在售'商品选择列表
			"""
			[{
				"name":"商品3不可两行显示...",
				"create_time":"2015-05-03 9:00"
			},{
				"name":"商品1可单行显示",
				"create_time":"2015-05-02 9:00"
			},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}]
			"""
		#添加新商品
		Given jobs已添加商品
		"""
		[{
			"name": "商品5",
			"product_picture_id":"5",
			"create_time":"2015-05-05 9:00",
			"shelve_type":"上架",
			"price": 5.0
		}]
		"""
		Then jobs获取'在售'商品选择列表
		"""
		[{
			"name":"商品5",
			"create_time":"2015-05-05 9:00"
		},{
			"name":"商品3不可两行显示......",
			"create_time":"2015-05-03 9:00"
		},{
			"name":"商品1可单行显示",
			"create_time":"2015-05-02 9:00"
		},{
			"name":"商品2可两行显示",
			"create_time":"2015-05-01 9:00"
		}]
		"""

Scenario:2 商品选择列表分页,每页显示8个商品
	Given jobs已添加商品
	"""
	[{
		"name": "商品5",
		"product_picture_id":"5",
		"create_time":"2015-05-05 9:00",
		"shelve_type":"上架",
		"price": 5.0
	},{
		"name": "商品6",
		"product_picture_id":"6",
		"create_time":"2015-05-06 9:00",
		"shelve_type":"上架",
		"price": 6.0
	},{
		"name": "商品7",
		"product_picture_id":"7",
		"create_time":"2015-05-07 9:00",
		"shelve_type":"上架",
		"price": 7.0
	},{
		"name": "商品8",
		"product_picture_id":"8",
		"create_time":"2015-05-08 9:00",
		"shelve_type":"上架",
		"price": 8.0
	},{
		"name": "商品9",
		"product_picture_id":"9",
		"create_time":"2015-05-10 9:00",
		"shelve_type":"上架",
		"price": 9.0
	},{
		"name": "商品10",
		"product_picture_id":"10",
		"create_time":"2015-05-9 9:00",
		"shelve_type":"上架",
		"price": 10.0
	}]
	"""
	Then jobs商品模块商品选择列表显示2页
	When jobs访问商品选择列表第1页
	Then jobs获取'在售'商品选择列表
	"""
	[{
		"name": "商品9",
		"create_time":"2015-05-10 9:00"
	},{
		"name": "商品10",
		"create_time":"2015-05-09 9:00"
	},{
		"name": "商品8",
		"create_time":"2015-05-08 9:00"
	},{
		"name": "商品7",
		"create_time":"2015-05-07 9:00"
	},{
		"name": "商品6",
		"create_time":"2015-05-06 9:00"
	},{
		"name": "商品5",
		"create_time":"2015-05-05 9:00"
	},{
		"name":"商品3不可两行显示......",
		"create_time":"2015-05-03 9:00"
	},{
		"name":"商品1可单行显示",
		"create_time":"2015-05-02 9:00"
	}]
	"""
	When jobs浏览'下一页'
	Then jobs获取'在售'商品选择列表
	"""
	[{
		"name":"商品2可两行显示",
		"create_time":"2015-05-01 9:00"
	}]
	"""
	When jobs浏览'上一页'
	Then jobs获取'在售'商品选择列表
	"""
	[{
		"name": "商品9",
		"create_time":"2015-05-10 9:00"
	},{
		"name": "商品10",
		"create_time":"2015-05-09 9:00"
	},{
		"name": "商品8",
		"create_time":"2015-05-08 9:00"
	},{
		"name": "商品7",
		"create_time":"2015-05-07 9:00"
	},{
		"name": "商品6",
		"create_time":"2015-05-06 9:00"
	},{
		"name": "商品5",
		"create_time":"2015-05-05 9:00"
	},{
		"name":"商品3不可两行显示......",
		"create_time":"2015-05-03 9:00"
	},{
		"name":"商品1可单行显示",
		"create_time":"2015-05-02 9:00"
	}]
	"""

Scenario:3 一个商品可以被重复选择
	When jobs创建微页面
	"""
	[{	"title": 
		{
			"name": 微页面标题"
		},
		"products":
		{
			"items": [{
			"name":"商品3不可两行显示......",
			"create_time":"2015-05-03 9:00"
			},{
			"name":"商品1可单行显示",
			"create_time":"2015-05-02 9:00"
			},{
			"name":"商品2可两行显示",
			"create_time":"2015-05-01 9:00"
			}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
		
	}]
	"""
	Then jobs能获取'微页面标题'
	"""
	[{"title": 
		{
			"name": 微页面标题"
		}, 
		"products": {
			"items"[{
				"name":"商品3不可两行显示...",
				"price":"3.0"
			},{
				"name":"商品1可单行显示",
				"price":"1.0"
			},{
				"name":"商品2可两行显示",
				"price":"2.0"
				}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
	}]
	"""
	When jobs编辑微页面'微页面标题'
	"""
	[{
		"products":{
			"items"{
				[{
				"name":"商品1可单行显示",
				"create_time":"2015-05-02 9:00"
				},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
				}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
				}
		}	
	}]
	"""

	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items" [{
				"name":"商品3不可两行显示...",
				"price":"3.0"
			},{
				"name":"商品1可单行显示",
				"price":"1.0"
			},{
				"name":"商品2可两行显示",
				"price":"2.0"
			},{
				"name":"商品1可单行显示",
				"price":"1.0"
			},{
				"name":"商品2可两行显示",
				"price":"2.0"
			}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""

Scenario:4 商品管理'下架'、'删除'商品
	When jobs创建微页面
	"""
	[{
		"title": {
			"name": 微页面标题"
		},
		"products": {
			"items":[{
				"name":"商品3不可两行显示......",
				"create_time":"2015-05-03 9:00"
				},{
				"name":"商品1可单行显示",
				"create_time":"2015-05-02 9:00"
				},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
				}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items" [{
				"name":"商品3不可两行显示...",
				"price":"3.0"
				},{
				"name":"商品1可单行显示",
				"price":"1.0"
				},{
				"name":"商品2可两行显示",
				"price":"2.0"
				}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""
	When jobs下架商品'商品3不可两行显示...'
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items": [{
				"name":"商品1可单行显示",
				"price":"1.0"
				},{
				"name":"商品2可两行显示",
				"price":"2.0"
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""

	When jobs删除商品'商品2可两行显示'
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items": [{
				"name":"商品1可单行显示",
				"price":"1.0"
				}],
				"list_style1":"大图",
		"list_style2":"默认样式",
		"show_product_name":"ture",
		"show_price":"true"
			}
	}]
	"""

Scenario:5 商品管理'修改'商品
	When jobs创建微页面
	"""
	[{	"title": {
			"name": 微页面标题"
		}
		"products": {
			"items" [{
			"name":"商品3不可两行显示......",
			"create_time":"2015-05-03 9:00"
			},{
			"name":"商品1可单行显示",
			"create_time":"2015-05-02 9:00"
			},{
			"name":"商品2可两行显示",
			"create_time":"2015-05-01 9:00"
		}],
		"list_style1":"大图",
		"list_style2":"默认样式",
		"show_product_name":"ture",
		"show_price":"true"
		}
	}]	
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items": [{
				"name":"商品3不可两行显示...",
				"price":"3.0"
				},{
				"name":"商品1可单行显示",
				"price":"1.0"
				},{
				"name":"商品2可两行显示",
				"price":"2.0"
				}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""
	#修改商品价格和名称
	When jobs修改商品'商品2可两行显示'
	"""
	[{
		"name":"修改后——商品2可两行显示",
		"price":"20.0"
	}]
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": 微页面标题"
		}, 
		"products": {
			"items": [{
				"name":"商品3不可两行显示...",
				"price":"3.0"
				},{
				"name":"商品1可单行显示",
				"price":"1.0"
				},{
				"name":"修改后——商品2可两行显示",
				"price":"20.0"
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
	}]
	"""

Scenario:6 商品修改，删除
	When jobs创建微页面
	"""
		[{	
			"title": {
				"name": 微页面标题"
			},
			"products": {
				"items" [{
				"name":"商品3不可两行显示......",
				"create_time":"2015-05-03 9:00"
				},{
				"name":"商品1可单行显示",
				"create_time":"2015-05-02 9:00"
				},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
		}]	
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": 微页面标题"
			}, 
			"products": {
				"items": [{
					"name":"商品3不可两行显示...",
					"price":"3.0"
					},{
					"name":"商品1可单行显示",
					"price":"1.0"
					},{
					"name":"商品2可两行显示",
					"price":"2.0"
					}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"ture",
				"show_price":"true"
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{	
			"title": {
				"name": 微页面标题"
			},
			"products": {
				"items" [{
				"name":"商品3不可两行显示......",
				"create_time":"2015-05-03 9:00"
				},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{	
			"title": {
				"name": 微页面标题"
			},
			"products": {
				"items" [{
				"name":"商品3不可两行显示......",
				"create_time":"2015-05-03 9:00"
				},{
				"name":"商品2可两行显示",
				"create_time":"2015-05-01 9:00"
			}],
			"list_style1":"大图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{	
			"title": {
				"name": 微页面标题"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{	
			"title": {
				"name": 微页面标题"
			}
		}
	"""
	
