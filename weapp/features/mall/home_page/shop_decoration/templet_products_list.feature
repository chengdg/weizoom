#_author_:师帅 15/10/12


Feature:自定义模块——【基础模块】商品列表-页面
	"""
	#设置一个列表样式的商品展示区，选择商品分组，将分组中上架的商品到商品展示区
	#1、选择商品分组
	#（1）可以选择所有的商品分组
	#（2）选择分组单选
	#（3）商品分组按照创建时间倒序显示
	#（4）分组名称过长显示不全的"..."方式显示
	#（5）商品分组列表分页显示
	#（6）"分组管理"，打开新页面，进入"分组管理"，新添加的分组，刷新之后在当前选择分组窗体可以选择到
	#2、选择分组中的商品，按照创建时间倒序依次添加到商品展示区
	#3、所选择商品分组中的上架的商品不足'显示个数'的，直接只显示分组中的现有商品，小图和一大两小的不够一组的直接空白
	#关于商品状态和分组状态改变，商品列表的处理
	#4、重新选择分组，删除之前分组添加的所有商品，重新添加现在分组的所有商品
	#5、修改分组中的商品的个数和商品，商品列表模块和使用商品列表的地方同步修改
	#6、修改分组中的商品详细信息，商品列表模块和使用商品列表的地方同步修改
	#7、商品列表只展示所选择的分组中的“在售”的商品。
	#8、自定义页面中选择的商品分组中的商品被下架、删除，自定义页面刷新后自动删除该商品
	#9、自定义页面中选择的商品分组被删除，自定义页面删除此‘商品列表’基础模块
	#10、商品列表’商品来源的’商品分组‘名称应该和商品管理下的’商品分组‘名称同步 ，修改商品分组名称，商品列表中的商品来源的商品分组名称也应该同步修改
	#11、商品如果参加了促销活动显示促销价格
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分组1"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1可单行显示",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 4.0
		},{
			"name": "商品5",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 5.0
		},{
			"name": "商品6",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 6.0
		},{
			"name": "商品7",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 7.0
		}]
		"""


@mall2  @termite2
Scenario:1 商品管理'下架'、'删除'、'添加'、'修改'分组中的商品

	#商品列表模块显示个数'6','详细列表'样式,'默认样式'
	When jobs创建微页面
		"""
		[{
			"title":{
				"name": "微页面标题1"
			},
			"products_source": {
				"index": 1,
				"items": [{
					"products_source_name": "分组1"
				}],
				"display_count": "6",
				"list_style1": "列表",
				"list_style2": "默认样式"
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
				"index": 1,
				"items": [{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name": "商品3不可两行显示",
					"price": 3.0
				},{
					"name": "商品2可两行显示",
					"price": 2.0
				}],
				"list_style1": "列表",
				"list_style2": "默认样式"
			}
		}
		"""

	#下架商品'1'
	When jobs-下架商品'商品1可单行显示'
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"index": 1,
				"items":[{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""
	#删除商品'2'
	When jobs-永久删除商品'商品2可两行显示'
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"index": 1,
				"items":[{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"商品3不可两行显示",
					"price": 3.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""
	#分组添加商品'10'
	Given jobs已添加商品
		"""
		[{
			"name": "商品10",
			"categories": "分组1",
			"shelve_type":"上架",
			"price": 10.0
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"index": 1,
				"items":[{
					"name":"商品10",
					"price": 10.0
				},{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"商品3不可两行显示",
					"price": 3.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""
	#修改分组中商品'3'的详细信息
	When jobs更新商品'商品3不可两行显示'
		"""
		{
			"name":"修改后商品3不可两行显示",
			"categories": "分组1",
			"price":"30.0"
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"index": 1,
				"items":[{
					"name":"商品10",
					"price": 10.0
				},{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"修改后商品3不可两行显示",
					"price": 30.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""

@mall2  @termite2
Scenario:2 商品管理，删除商品分组
	#商品列表模块显示个数'6','详细列表'样式,'默认样式'
	When jobs创建微页面
		"""
		[{
			"title":{
				"name": "微页面标题1"
			},
			"products_source": {
				"index": 1,
				"items":[{
					"products_source_name": "分组1"
				}],
				"display_count": "6",
				"list_style1": "列表",
				"list_style2": "默认样式"
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
				"index": 1,
				"items":[{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""
	#删除商品分组
	When jobs删除商品分类'分组1'
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
		"""

@mall2  @termite2
Scenario: 3编辑商品列表
	When jobs创建微页面
		"""
		[{	
			"title":{
				"name": "微页面标题1"
			},
			"products_source": {
				"index": 1,
				"items":[{
					"products_source_name": "分组1"
				}],
				"display_count": "6",
				"list_style1": "列表",
				"list_style2": "默认样式"
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
				"index": 1,
				"items":[{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
					"name":"商品3不可两行显示",
					"price": 3.0
				},{
					"name":"商品2可两行显示",
					"price": 2.0
				}],
				"list_style1":"列表",
				"list_style2":"默认样式"
			}
		}
		"""
	When jobs编辑微页面'微页面标题1'
		"""
		{	
			"title":{
				"name": "微页面标题1"
			},
			"products_source": {
				"index": 1,
				"items":[{
					"products_source_name": "分组1"
				}],
				"display_count": "6",
				"list_style1": "小图",
				"list_style2": "简洁样式",
				"show_price": "true"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"products_source":{
				"index": 1,
				"items":[{
					"name":"商品7",
					"price": 7.0
				},{
					"name":"商品6",
					"price": 6.0
				},{
					"name":"商品5",
					"price": 5.0
				},{
					"name":"商品4",
					"price": 4.0
				},{
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
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
		"""




