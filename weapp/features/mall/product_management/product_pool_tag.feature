#_author_:田丰敏 2016.09.21


Feature:自营平台查看商品池标签
	"""
		说明：需要先实现panda系统商品分类、标签、同步商品等step，该feature现只做数据参考
		1、商品二级分类配置标签，同步商品到自营平台；商品配置标签，同步商品到自营平台
		2、商品同步到自营平台后，在panda系统修改商品分类（/商品分类标签/商品标签），标签的变化可实时同步到自营平台；
		   商品同步到自营平台后，在panda系统删除已使用的标签，标签的变化可实时同步到自营平台
		3、在商品池根据商品标签进行筛选

		备注：商品标签以商品为主，如果该商品修改了标签后，则不再根据分类标签的变化而变化
	"""

Background:
	Given 重置'weizoom_card'的bdd环境
	Given 重置'apiserver'的bdd环境
	Given yunying登录系统::panda

	When yunying添加分类::panda
		"""
		{
			"head_classify":"无",
			"classify_name":"电子数码",
			"comments":"1"
		}
		"""
	When yunying添加分类::panda
		"""
		{
			"head_classify":"无",
			"classify_name":"生活用品",
			"comments":"1"
		}
		"""
	When yunying添加分类::panda
		"""
		{
			"head_classify":"电子数码",
			"classify_name":"手机",
			"comments":""
		}
		"""
	When yunying添加分类::panda
		"""
		{
			"head_classify":"电子数码",
			"classify_name":"平板电脑",
			"comments":""
		}
		"""
	When yunying添加分类::panda
		"""
		{
			"head_classify":"生活用品",
			"classify_name":"零食",
			"comments":""
		}
		"""
	When yunying添加分类::panda
		"""
		{
			"head_classify":"生活用品",
			"classify_name":"肥皂",
			"comments":""
		}
		"""

	When yunying新增标签
		"""
		{
			"tag_group":"国家",
			"tag":["美国","法国","中国","德国","意大利","澳大利亚"]
		}
		"""
	When yunying新增标签
		"""
		{
			"tag_group":"省市",
			"tag":["江苏","黑龙江","广东","浙江","北京","江西"]
		}
		"""
	When yunying新增标签
		"""
		{
			"tag_group":"基本信息",
			"tag":["男","女","新生儿","9-13岁","14-18岁","成年"]
		}
		"""
	When yunying新增标签
		"""
		{
			"tag_group":"地区",
			"tag":["亚洲","欧洲"]
		}
		"""
	#创建供货商、设置商家运费、同步商品到自营平台
	#创建供货商
	Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name":"商家1",
			"first_classify":["电子数码","生活用品"]
		}
		"""
	Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name":"商家2",
			"first_classify":["电子数码","生活用品"]
		}
		"""
	Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name":"商家3",
			"first_classify":["电子数码","生活用品"]
		}
		"""

	When yunying给商品分类配置标签::panda
		"""
		{
			"product_style":[{
						"first_classify":"生活用品",
						"second_classify":"零食",
						"label":[{
							"tag_group":"国家",
							"tag":["美国","法国"]
						},{
							"tag_group":"省市",
							"tag":["江苏","北京"]
						},{
							"tag_group":"基本信息",
							"tag":["新生儿"]
						}]
					},{
						"first_classify":"电子数码",
						"second_classify":"平板电脑",
						"label":[{
							"tag_group":"基本信息",
							"tag":["男","女","新生儿"]
						}]
					},{
						"first_classify":"电子数码",
						"second_classify":"手机",
						"label":[{
							"tag_group":"地区",
							"tag":["亚洲","欧洲"]
						}]
					}]
		}
		"""
	When '商家1'新增商品
		"""
		{
			"name": "商品1a",
			"promotion_title": "商品1a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1a描述信息",
			"first_classify":"生活用品",
			"second_classify":"零食"
		}
		"""

	When '商家1'新增商品
		"""
		{
			"name": "商品1b",
			"promotion_title": "商品1b促销",
			"purchase_price": 8.00,
			"price": 9.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1b描述信息",
			"first_classify":"生活用品",
			"second_classify":"肥皂"
		}
		"""
	When '商家2'新增商品
		"""
		{
			"name": "商品2a",
			"promotion_title": "商品2a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品2a描述信息",
			"first_classify":"电子数码",
			"second_classify":"平板电脑"
		}
		"""

	When '商家3'新增商品
		"""
		{
			"name": "商品3a",
			"promotion_title": "商品3a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品3a描述信息",
			"first_classify":"电子数码",
			"second_classify":"手机"
		}
		"""
	Given yunying登录系统::panda
	When yunying给商品'商品1b'配置标签::panda
		"""
		{
			"label":[{
				"tag_group":"省市",
				"tag":["北京","江西"]
			},{
				"tag_group":"基本信息",
				"tag":["成年"]
			}]
		}
		"""


	#同步商品到自营平台

	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"商家3",
			"name": "商品3a",
			"promotion_title": "商品3a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品3a描述信息",
			"first_classify":"电子数码",
			"second_classify":"手机",
			"tag":["亚洲","欧洲"]
		}
		"""

	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"商家2",
			"name": "商品2a",
			"promotion_title": "商品2a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品2a描述信息",
			"first_classify":"电子数码",
			"second_classify":"平板电脑",
			"tag":["男","女","新生儿"]
		}
		"""

	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"商家1",
			"name": "商品1b",
			"promotion_title": "商品1b促销",
			"purchase_price": 8.00,
			"price": 9.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1b描述信息",
			"first_classify":"生活用品",
			"second_classify":"肥皂",
			"tag":["北京","江西","成年"]
		}
		"""

	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"商家1",
			"name": "商品1a",
			"promotion_title": "商品1a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1a描述信息",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"tag":["美国","法国","江苏","北京","新生儿"]
		}
		"""

Scenario:1 自营平台查看商品池商品标签
	Given zy1登录系统
	Then zy1获得商品池商品列表
		"""
		[{
			"name": "商品1a",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"supplier":"商家1",
			"price": 10.00,
			"stocks":100,
			"tag":["美国","法国","江苏","北京","新生儿"],
			"actions": ["上架"]
		},{
			"name": "商品1b",
			"first_classify":"生活用品",
			"second_classify":"肥皂",
			"supplier":"商家1",
			"price": 9.00,
			"stocks":100,
			"tag":["北京","江西","成年"],
			"actions": ["上架"]
		},{
			"name": "商品2a",
			"first_classify":"电子数码",
			"second_classify":"平板电脑",
			"supplier":"商家2",
			"price": 10.00,
			"stocks":100,
			"tag":["男","女","新生儿"],
			"actions": ["上架"]
		},{
			"name": "商品3a",
			"first_classify":"电子数码",
			"second_classify":"手机",
			"supplier":"商家3",
			"price": 10.00,
			"stocks": 100,
			"tag":["亚洲","欧洲"],
			"actions": ["上架"]
		}]
		"""
Scenario:2 商品管理系统修改商品分类（分类标签，商品标签），查看商品池商品标签
	Given yunying登录系统::panda

	When yunying给商品分类配置标签::panda
		"""
		{
			"product_style":[{
						"first_classify":"生活用品",
						"second_classify":"零食",
						"label":[{
							"tag_group":"国家",
							"tag":["美国","法国"]
						},{
							"tag_group":"省市",
							"tag":["江苏","北京"]
						}]
					},{
						"first_classify":"电子数码",
						"second_classify":"平板电脑",
						"label":[{
							"tag_group":"省市",
							"tag":["江苏","北京"]
						}]
					}]
		}
		"""
	When yunying删除标签
	"""
	{
		"tag_group":"地区"
	}
	"""
	When 商家'商家1'编辑商品'商品1a'
		"""
		{
			"name": "商品1a",
			"promotion_title": "商品1a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1a描述信息",
			"first_classify":"生活用品",
			"second_classify":"肥皂"
		}
		"""


	When yunying给商品'商品1b'配置标签::panda
		"""
		{
			"label":[{
				"tag_group":"基本信息",
				"tag":["成年"]
			}]
		}
		"""

	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"商家1",
			"name": "商品1a",
			"promotion_title": "商品1a促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1a描述信息",
			"first_classify":"生活用品",
			"second_classify":"肥皂"
		}
		"""

	Given zy1登录系统
	Then zy1获得商品池商品列表
		"""
		[{
			"name": "商品1a",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"supplier":"商家1",
			"price": 10.00,
			"stocks":100,
			"tag":"",
			"actions": ["上架"]
		},{
			"name": "商品1b",
			"first_classify":"生活用品",
			"second_classify":"肥皂",
			"supplier":"商家1",
			"price": 9.00,
			"stocks":100,
			"tag":["成年"]
			"actions": ["上架"]
		},{
			"name": "商品2a",
			"first_classify":"电子数码",
			"second_classify":"平板电脑",
			"supplier":"商家2",
			"price": 10.00,
			"stocks":100,
			"tag":["江苏","北京"]
			"actions": ["上架"]
		},{
			"name": "商品3a",
			"first_classify":"电子数码",
			"second_classify":"手机",
			"supplier":"商家3",
			"price": 10.00,
			"stocks": 100,
			"actions": ["上架"]
		}]
		"""

Scenario:3 在商品池根据标签进行筛选

	Given zy1登录系统
	When jobs设置商品池列表查询条件
		"""
		{
			"tag":""
		}
		"""
	Then zy1获得商品池商品列表
		"""
		[{
			"name": "商品1a",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"supplier":"商家1",
			"price": 10.00,
			"stocks":100,
			"tag":["美国","法国","江苏","北京","新生儿"],
			"actions": ["上架"]
		},{
			"name": "商品1b",
			"first_classify":"生活用品",
			"second_classify":"肥皂",
			"supplier":"商家1",
			"price": 9.00,
			"stocks":100,
			"tag":["北京","江西","成年"],
			"actions": ["上架"]
		},{
			"name": "商品2a",
			"first_classify":"电子数码",
			"second_classify":"平板电脑",
			"supplier":"商家2",
			"price": 10.00,
			"stocks":100,
			"tag":["男","女","新生儿"],
			"actions": ["上架"]
		},{
			"name": "商品3a",
			"first_classify":"电子数码",
			"second_classify":"手机",
			"supplier":"商家3",
			"price": 10.00,
			"stocks": 100,
			"tag":["亚洲","欧洲"],
			"actions": ["上架"]
		}]
		"""
	When jobs设置商品池列表查询条件
		"""
		{
			"tag":["北京"]
		}
		"""
	Then zy1获得商品池商品列表
		"""
		[{
			"name": "商品1a",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"supplier":"商家1",
			"price": 10.00,
			"stocks":100,
			"tag":["美国","法国","江苏","北京","新生儿"],
			"actions": ["上架"]
		},{
			"name": "商品1b",
			"first_classify":"生活用品",
			"second_classify":"肥皂",
			"supplier":"商家1",
			"price": 9.00,
			"stocks":100,
			"tag":["北京","江西","成年"],
			"actions": ["上架"]
		}]
		"""
	When jobs设置商品池列表查询条件
		"""
		{
			"supplier":"商家1",
			"tag":["新生儿"]
		}
		"""
	Then zy1获得商品池商品列表
		"""
		[{
			"name": "商品1a",
			"first_classify":"生活用品",
			"second_classify":"零食",
			"supplier":"商家1",
			"price": 10.00,
			"stocks":100,
			"tag":["美国","法国","江苏","北京","新生儿"],
			"actions": ["上架"]
		}]
		"""