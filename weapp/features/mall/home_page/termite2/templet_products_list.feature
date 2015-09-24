#_author_:王丽
#_edit_:新新

Feature:自定义模块——【基础模块】商品列表-页面
        设置一个列表样式的商品展示区，选择商品分组，将分组中上架的商品到商品展示区
        1、选择商品分组
        （1）可以选择所有的商品分组
        （2）选择分组单选
        （3）商品分组按照创建时间倒序显示
        （4）分组名称过长显示不全的"..."方式显示
        （5）商品分组列表分页显示
        （6）"分组管理"，打开新页面，进入"分组管理"，新添加的分组，刷新之后在当前选择分组窗体可以选择到
        2、选择分组中的商品，按照创建时间倒序依次添加到商品展示区
        3、所选择商品分组中的上架的商品不足'显示个数'的，直接只显示分组中的现有商品，小图和一大两小的不够一组的直接空白
        #关于商品状态和分组状态改变，商品列表的处理
        4、重新选择分组，删除之前分组添加的所有商品，重新添加现在分组的所有商品
        5、修改分组中的商品的个数和商品，商品列表模块和使用商品列表的地方同步修改
        6、修改分组中的商品详细信息，商品列表模块和使用商品列表的地方同步修改
        7、商品列表只展示所选择的分组中的“在售”的商品。
        8、自定义页面中选择的商品分组中的商品被下架、删除，自定义页面刷新后自动删除该商品
        9、自定义页面中选择的商品分组被删除，自定义页面删除此‘商品列表’基础模块
        10、商品列表’商品来源的’商品分组‘名称应该和商品管理下的’商品分组‘名称同步 ，修改商品分组名称，商品列表中的商品来源的商品分组名称也应该同步修改
        11、商品如果参加了促销活动显示促销价格

Background:
	Given jobs登录系统
	And jobs已添加分组
		"""
		[{
			"name": "分组1",
			"create_time":"2015-05-09 9:00"
		},{
			"name": "分组2",
			"create_time":"2015-05-08 9:00"
		},{
			"name": "分组3",
			"create_time":"2015-05-07 9:00"
		},{
			"name": "分组4",
			"create_time":"2015-05-09 8:00"
		},{
			"name": "分类5",
			"create_time":"2015-05-05 8:00"
		},{
			"name": "分类6",
			"create_time":"2015-05-04 8:00"
		},{
			"name": "分类7",
			"create_time":"2015-05-03 8:00"
		},{
			"name": "分类8",
			"create_time":"2015-05-02 8:00"
		},{
			"name": "分类9",
			"create_time":"2015-05-01 8:00"
		}]	
		"""
	#商品1,商品2,商品3,商品4,商品5,商品6,商品7,商品8,商品9,商品10（上架状态）,商品11,商品12,商品13（下架状态）
	#分类1:商品1,商品2,商品3,商品4,商品5,商品6,商品7,商品11
	#分类2:商品1,商品2,商品3,商品4,商品5,商品6,商品7,商品11,商品12,商品13
	#分类3:商品1,商品2,商品3,商品4,商品5,商品6,商品7,商品8,商品9,商品10,商品11,商品12,商品13
	#分类4:商品11,商品12,商品13
	And jobs已添加商品
		"""
		[{
			"name": "商品1可单行显示",
			"product_picture_id":"1",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-12 9:00",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"product_picture_id":"2",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-13 9:00",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示......",
			"product_picture_id":"3",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-11 9:00",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"product_picture_id":"4",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-10 9:00",
			"shelve_type":"上架",
			"price": 4.0
		},{
			"name": "商品5",
			"product_picture_id":"5",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-09 9:00",
			"shelve_type":"上架",
			"price": 5.0
		},{
			"name": "商品6",
			"product_picture_id":"6",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-08 9:00",
			"shelve_type":"上架",
			"price": 6.0
		},{
			"name": "商品7",
			"product_picture_id":"7",
			"category": "分类1,分类2,分类3",
			"create_time":"2015-05-07 9:00",
			"shelve_type":"上架",
			"price": 7.0
		},{
			"name": "商品8",
			"product_picture_id":"8",
			"category": "分类1,分类3",
			"create_time":"2015-05-06 9:00",
			"shelve_type":"上架",
			"price": 8.0
		},{
			"name": "商品9",
			"product_picture_id":"9",
			"create_time":"2015-05-05 9:00",
			"category": "分类3",
			"shelve_type":"上架",
			"price": 9.0
		},{
			"name": "商品10",
			"product_picture_id":"10",
			"category": "分类3",
			"create_time":"2015-05-04 9:00",
			"shelve_type":"上架",
			"price": 10.0
		},{
			"name": "商品11",
			"product_picture_id":"11",
			"category": "分类1,分类3,分类4",
			"create_time":"2015-05-03 9:00",
			"shelve_type":"下架",
			"price": 11.0
		},{
			"name": "商品12",
			"product_picture_id":"12",
			"category": "分类3,分类4",
			"create_time":"2015-05-02 9:00",
			"price": 12.0
		},{
			"name": "商品13",
			"product_picture_id":"13",
			"category": "分类3,分类4",
			"create_time":"2015-05-01 9:00",
			"price": 13.0
		}]	
		"""

Scenario:选择商品分组窗体：商品分组列表搜索、添加新商品分组
	Given job获得商品分类列表
		"""
		[{
			"name": "分组1",
			"create_time":"2015-05-09 9:00"
		},{
			"name": "分组4",
			"create_time":"2015-05-09 8:00"
		},{
			"name": "分组2",
			"create_time":"2015-05-08 9:00"
		},{
			"name": "分组3",
			"create_time":"2015-05-07 9:00"
		},{
			"name": "分类5",
			"create_time":"2015-05-05 8:00"
		},{
			"name": "分类6",
			"create_time":"2015-05-04 8:00"
		},{
			"name": "分类7",
			"create_time":"2015-05-03 8:00"
		},{
			"name": "分类8",
			"create_time":"2015-05-02 8:00"
		},{
			"name": "分类9",
			"create_time":"2015-05-01 8:00"
		}]
		"""
	#选择商品分组名称的搜索
		#模糊匹配
			When jobs按商品分组名称搜索
			"""
			[{
				"search":"分类"
			}]
			"""

			Then jobs获得商品分组列表
			"""
			[{
				"name": "分类5",
				"create_time":"2015-05-05 8:00"
			},{
				"name": "分类6",
				"create_time":"2015-05-04 8:00"
			},{
				"name": "分类7",
				"create_time":"2015-05-03 8:00"
			},{
				"name": "分类8",
				"create_time":"2015-05-02 8:00"
			},{
				"name": "分类9",
				"create_time":"2015-05-01 8:00"
			}]
			"""
		#完全匹配
			When jobs按商品分组名称搜索
			"""
			[{
				"search":"分类6"
			}]
			"""
			Then jobs获得商品分组列表
			"""
			[{
				"name": "分类6",
				"create_time":"2015-05-04 8:00"
			}]
			"""
		#空搜索
			When jobs按商品分组名称搜索
			"""
			[{
				"search":""
			}]
			"""
			Then jobs获得商品分组列表
			"""
			[{
				"name": "分组1",
				"create_time":"2015-05-09 9:00"
			},{
				"name": "分组4",
				"create_time":"2015-05-09 8:00"
			},{
				"name": "分组2",
				"create_time":"2015-05-08 9:00"
			},{
				"name": "分组3",
				"create_time":"2015-05-07 9:00"
			},{
				"name": "分类5",
				"create_time":"2015-05-05 8:00"
			},{
				"name": "分类6",
				"create_time":"2015-05-04 8:00"
			},{
				"name": "分类7",
				"create_time":"2015-05-03 8:00"
			},{
				"name": "分类8",
				"create_time":"2015-05-02 8:00"
			},{
				"name": "分类9",
				"create_time":"2015-05-01 8:00"
			}]
			"""
		#添加新分组
			When jobs添加分组
			"""
			[{
				"name":"新分组",
				"create_time":"2015-05-15 9:00"
			}]
			"""
			Then jobs获得商品分组列表
			"""
			[{
				"name": "新分组",
				"create_time":"2015-05-15 9:00"
			},{
				"name": "分组1",
				"create_time":"2015-05-09 9:00"
			},{
				"name": "分组4",
				"create_time":"2015-05-09 8:00"
			},{
				"name": "分组2",
				"create_time":"2015-05-08 9:00"
			},{
				"name": "分组3",
				"create_time":"2015-05-07 9:00"
			},{
				"name": "分类5",
				"create_time":"2015-05-05 8:00"
			},{
				"name": "分类6",
				"create_time":"2015-05-04 8:00"
			},{
				"name": "分类7",
				"create_time":"2015-05-03 8:00"
			},{
				"name": "分类8",
				"create_time":"2015-05-02 8:00"
			},{
				"name": "分类9",
				"create_time":"2015-05-01 8:00"
			}]
			"""

Scenario:1 商品分组选择列表分页
	When jobs获取商品分组选择列表
	"""
	[{
		"name": "分组1",
		"create_time":"2015-05-09 9:00"
	},{
		"name": "分组4",
		"create_time":"2015-05-09 8:00"
	},{
		"name": "分组2",
		"create_time":"2015-05-08 9:00"
	},{
		"name": "分组3",
		"create_time":"2015-05-07 9:00"
	},{
		"name": "分类5",
		"create_time":"2015-05-05 8:00"
	},{
		"name": "分类6",
		"create_time":"2015-05-04 8:00"
	},{
		"name": "分类7",
		"create_time":"2015-05-03 8:00"
	},{
		"name": "分类8",
		"create_time":"2015-05-02 8:00"
	},{
		"name": "分类9",
		"create_time":"2015-05-01 8:00"
	}]
	"""
	When jobs已设置分页条件
	"""
	{
		"page_count":8
	}
	"""

	Then jobs获取商品列表模块商品分组选择列表显示共2页
	When jobs浏览第1页
	Then jobs获取商品分组选择列表
	"""
	[{
		"name": "分组1",
		"create_time":"2015-05-09 9:00"
	},{
		"name": "分组4",
		"create_time":"2015-05-09 8:00"
	},{
		"name": "分组2",
		"create_time":"2015-05-08 9:00"
	},{
		"name": "分组3",
		"create_time":"2015-05-07 9:00"
	},{
		"name": "分类5",
		"create_time":"2015-05-05 8:00"
	},{
		"name": "分类6",
		"create_time":"2015-05-04 8:00"
	},{
		"name": "分类7",
		"create_time":"2015-05-03 8:00"
	},{
		"name": "分类8",
		"create_time":"2015-05-02 8:00"
	}]
	"""
	When jobs浏览'第2页'
	Then jobs获取商品分组选择列表
	"""
	[{
		"name": "分类9",
		"create_time":"2015-05-01 8:00"
	}]
	"""
	When jobs浏览'上一页'
	Then jobs获取商品分组列表
	"""
	[{
		"name": "分组1",
		"create_time":"2015-05-09 9:00"
	},{
		"name": "分组4",
		"create_time":"2015-05-09 8:00"
	},{
		"name": "分组2",
		"create_time":"2015-05-08 9:00"
	},{
		"name": "分组3",
		"create_time":"2015-05-07 9:00"
	},{
		"name": "分类5",
		"create_time":"2015-05-05 8:00"
	},{
		"name": "分类6",
		"create_time":"2015-05-04 8:00"
	},{
		"name": "分类7",
		"create_time":"2015-05-03 8:00"
	},{
		"name": "分类8",
		"create_time":"2015-05-02 8:00"
	}]
	"""

Scenario:2 商品管理'下架'、'删除'、'添加'、'修改'分组中的商品

	#商品列表模块显示个数'6','详细列表'样式,'默认样式'
		When jobs添加商品列表
		"""
		[{	"title": "微页面标题",
			"products_source":"分组1",
			"display_count":"6",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"price_show":"true"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品2可两行显示",
			"product_picture_id":"2",
			"price":"2.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品1可单行显示",
			"product_picture_id":"1",
			"price":"1.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""

	#下架商品'1'
		When jobs商品下架
		"""
		[{
			"product_picture_id":"1"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品2可两行显示",
			"product_picture_id":"2",
			"price":"2.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品7",
			"product_picture_id":"7",
			"price":"7.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""
	#删除商品'2'
		When jobs商品删除
		"""
		[{
			"product_picture_id":"1"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品7",
			"product_picture_id":"7",
			"price":"7.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品8",
			"product_picture_id":"8",
			"price":"8.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""
	#分组添加商品'10'
		When jobs商品模块添加商品
		"""
		[{
			"product_picture_id":"10"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品7",
			"product_picture_id":"7",
			"price":"7.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品8",
			"product_picture_id":"8",
			"price":"8.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品10",
			"product_picture_id":"10",
			"price":"10.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""
	#修改分组中商品'3'的详细信息
		When jobs修改商品
		"""
		[{
			"product_picture_id":"3",
			"name":"修改后商品3不可两行显示...",
			"price":"30.0"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"修改后商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"30.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品7",
			"product_picture_id":"7",
			"price":"7.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品8",
			"product_picture_id":"8",
			"price":"8.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品10",
			"product_picture_id":"10",
			"price":"10.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""

Scenario:3 商品管理，删除商品分组
	#商品列表模块显示个数'6','详细列表'样式,'默认样式'
		When jobs添加商品列表
		"""
		[{	"title": "微页面标题",
			"products_source":"分组1",
			"display_count":"6",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"price_show":"true"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品2可两行显示",
			"product_picture_id":"2",
			"price":"2.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品1可单行显示",
			"product_picture_id":"1",
			"price":"1.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""
	#删除商品分组
		When jobs删除分组'分组1'
		Then jobs能获取'微页面标题'
		"""
			[{
				"title": "微页面标题"
			}]
		"""

Scenario:4 分组管理修改商品名，商品列表中使用该分组的商品来源，也应该同步修改

	#商品列表模块显示个数'6','详细列表'样式,'默认样式'
		When jobs添加商品列表
		"""
		[{	"title": "微页面标题",
			"products_source":"分组1",
			"display_count":"6",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"price_show":"true"
		}]
		"""
		Then jobs能获取'微页面标题'
		"""
		[{
			"title": "微页面标题"
		},{
			"name":"商品2可两行显示",
			"product_picture_id":"2",
			"price":"2.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品1可单行显示",
			"product_picture_id":"1",
			"price":"1.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品3不可两行显示...",
			"product_picture_id":"3",
			"price":"3.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品4",
			"product_picture_id":"4",
			"price":"4.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"product_picture_id":"5",
			"price":"5.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"product_picture_id":"6",
			"price":"6.0",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
		"""

	#修改商品分组名称
		When jobs修改'分组1'的分组名称
		"""
		[{
			"grouping_name":"分组1——修改"
		}]
		"""
		Then jobs获取商品列表
		"""
		[{	"title": "微页面标题"
			"products_source":"分组1——修改",
			"display_count":"6",
			"list_style1":"详细列表",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"price_show":"true"
		}]
		"""




