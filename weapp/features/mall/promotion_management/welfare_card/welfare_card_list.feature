# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:福利卡券活动列表
	"""
		1、福利券列表查询条件：
			商品名称：支持模糊查询
			商品条码：精确查询
			创建时间：查询时开始时间必须小于等于结束时间
		2、福利卡券列表字段
			活动名称：显示创建时的活动名称
			商品名称：显示创建时选择的商品名称、条码
			总库存：福利卡券的总库存数
			可用库存:福利卡券可用的库存数
			已售出：已经售出的福利卡券的数量
			已过期:已过期的卡券数量
			已失效：已失效的卡券数量
			创建时间：福利卡券的创建时间，精确到秒，显示格式为：xxxx-xx-xx xx:xx:xx
			操作：【卡券详情】、【编辑】、【结束】/【已结束】
		3、点击操作【编辑】，进入编辑福利卡券页面，进入后可修改'有效期'、'码库文件'，活动名称和商品均不可编辑
		4、点击操作【结束】，弹出提示"是否确认结束该活动！"，确认后则【结束】变为【已结束】
		5、福利卡券结束后，若有未发放完的卡券，则剩余的卡券将使失效
	"""

Background:
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}]
		"""
	And jobs已添加供货商
		"""
		[{
			"name": "微众",
			"responsible_person": "张大众",
			"supplier_tel": "15211223344",
			"supplier_address": "北京市海淀区海淀科技大厦",
			"remark": "备注"
		}, {
			"name": "稻香村",
			"responsible_person": "许稻香",
			"supplier_tel": "15311223344",
			"supplier_address": "北京市朝阳区稻香大厦",
			"remark": ""
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given jobs已添加商品
		"""
		[{
			"name": "微众虚拟商品1",
			"product_type":"微众卡",
			"supplier": "微众",
			"purchase_price": 9.00,
			"promotion_title": "10元通用卡",
			"categories": "分类1,分类2",
			"bar_code":"112233",
			"min_limit":2,
			"is_member_product":"on",
			"price": 10.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 100,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail":"微众虚拟商品1的详情",
			"status":"在售"
		},{
			"name":"微众虚拟商品2",
			"product_type":"微众卡",
			"supplier":"微众",
			"purchase_price": 19.00,
			"promotion_title": "虚拟商品2",
			"categories": "",
			"bar_code":"212233",
			"price": 20.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 200,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				}],
			"detail":"微众虚拟商品2的详情",
			"status":"在售"
		},{
			"name": "稻香村虚拟商品3",
			"product_type":"虚拟商品",
			"supplier": "稻香村",
			"purchase_price": 30.00,
			"promotion_title": "稻香村代金券",
			"categories": "分类2",
			"bar_code":"312233",
			"min_limit":1,
			"is_member_product":"off",
			"price": 30.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 2,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail":"稻香村虚拟商品3的详情",
			"status""在售"
		}]
		"""
	And jobs已创建微众卡
		"""
		{
			"cards":[{
				"id":"0000001",
				"password":"1234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000002",
				"password":"2234567",
				"status":"未使用",
				"price":10.00
			},{
				"id":"0000003",
				"password":"3234567",
				"status":"未使用",
				"price":20.00
			},{
				"id":"0000004",
				"password":"4234567",
				"status":"未使用",
				"price":20.00
			},{
				"id":"0000005",
				"password":"5234567",
				"status":"未使用",
				"price":10.00
			}]
		}
		"""
	#创建福利卡券活动
	When jobs新建福利卡券活动
		"""
		[{
			"product":
				{
					"name":"微众虚拟商品1",
					"bar_code":"112233",
					"price":10.00
				},
			"activity_name":"10元通用卡",
			"card_start_date":"2天前",
			"card_end_date":"30天后",
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				}],
			"create_time":"2天前"
		},{
			"product":
				{
					"name":"微众虚拟商品2",
					"bar_code":"212233",
					"price":20.00
				},
			"activity_name":"20元通用卡",
			"card_start_date":"今天",
			"card_end_date":"30天后",
			"cards":
				[{
					"id":"0000003",
					"password":"3234567"
				},{
					"id":"0000004",
					"password":"4234567"
				}],
			"create_time":"今天"
		}]
		"""

@welfare_card @weshop
Scenario:1 编辑福利卡券活动
	Given jobs登录系统
	When jobs编辑福利卡券活动
		"""
		{
			"product":
				{
					"name":"微众虚拟商品1",
					"bar_code":"112233",
					"price":10.00
				},
			"activity_name":"10元通用卡修改",
			"card_start_date":"今天",
			"card_end_date":"36天后",
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				},{
					"id":"0000005",
					"password":"5234567"
				}],
			"create_time":"2天前"
		}
		"""
	Then jobs获得福利卡券活动列表
		"""
		[{
			"activity_name":"20元通用卡",
			"product":{
				"name":"微众虚拟商品2",
				"bar_code":"212233"
				},
			"total_stocks":2,
			"remain_stocks":2,
			"sale_cards":0,
			"expired_cards":0,
			"invalid_cards":0,
			"create_time":"今天",
			"actions":["卡券详情","编辑","结束"]
		},{
			"activity_name":"10元通用卡修改",
			"product":{
				"name":"微众虚拟商品1",
				"bar_code":"112233"
			},
			"total_stocks":3,
			"remain_stocks":3,
			"sale_cards":0,
			"expired_cards":0,
			"invalid_cards":0,
			"create_time":"2天前",
			"actions":["卡券详情","编辑","结束"]
		}]
		"""

@welfare_card @weshop
Scenario:2 结束福利卡券活动
	Given jobs登录系统
	When jobs'结束'福利卡券活动'20元通用卡'
	#Then jobs获得提示信息'是否确认结束?'
	Then jobs获得福利卡券活动列表
		"""
		[{
			"activity_name":"20元通用卡",
			"product":{
				"name":"微众虚拟商品2",
				"bar_code":"212233"
				},
			"total_stocks":2,
			"remain_stocks":2,
			"sale_cards":0,
			"expired_cards":0,
			"invalid_cards":0,
			"create_time":"今天",
			"actions":["卡券详情","编辑","已结束"]
		},{
			"activity_name":"10元通用卡",
			"product":{
				"name":"微众虚拟商品1",
				"bar_code":"112233"
			},
			"total_stocks":2,
			"remain_stocks":2,
			"sale_cards":0,
			"expired_cards":0,
			"invalid_cards":0,
			"create_time":"2天前",
			"actions":["卡券详情","编辑","结束"]
		}]
		"""
	And jobs获得福利卡券活动'20元通用卡'的卡券详情列表
		| card_id | create_time | start_date | end_date | status | get_time | member | order_no |
		| 0000003 |   今天      |    今天    | 30天后   | 已失效 |          |        |          |
		| 0000004 |   今天      |    今天    | 30天后   | 已失效 |          |        |          |

@welfare_card @weshop
Scenario:3 福利卡券活动列表的查询
	Given jobs登录系统
	#按照'商品名称'查询
		#模糊查询
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"微众",
					"product_bar_code":"",
					"create_start_time":"",
					"create_end_time":""
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[{
					"activity_name":"20元通用卡",
					"product":{
						"name":"微众虚拟商品2",
						"bar_code":"212233"
						}
				},{
					"activity_name":"10元通用卡",
					"product":{
						"name":"微众虚拟商品1",
						"bar_code":"112233"
						}
				}]
				"""
		#精确查询
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"微众虚拟商品2",
					"product_bar_code":"",
					"create_start_time":"",
					"create_end_time":""
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[{
					"activity_name":"20元通用卡",
					"product":{
						"name":"微众虚拟商品2",
						"bar_code":"212233"
						}
				}]
				"""

	#按照'商品条码'查询
		#查询结果为空
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"",
					"product_bar_code":"1234",
					"create_start_time":"",
					"create_end_time":""
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[]
				"""
		#精确查询
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"",
					"product_bar_code":"212233",
					"create_start_time":"",
					"create_end_time":""
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[{
					"activity_name":"20元通用卡",
					"product":{
						"name":"微众虚拟商品2",
						"bar_code":"212233"
						}
				}]
				"""

	#按照'创建时间'进行查询
		#开始时间和结束时间相等
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"",
					"product_bar_code":"",
					"create_start_time":"2天前",
					"create_end_time":"2天前"
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[{
					"activity_name":"10元通用卡",
					"product":{
						"name":"微众虚拟商品1",
						"bar_code":"112233"
						},
					"create_time":"2天前"
				}]
				"""
		#开始时间和结束时间不等
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"",
					"product_bar_code":"",
					"create_start_time":"3天前",
					"create_end_time":"2天后"
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[{
					"activity_name":"20元通用卡",
					"product":{
						"name":"微众虚拟商品2",
						"bar_code":"212233"
						},
					"create_time":"今天"
				},{
					"activity_name":"10元通用卡",
					"product":{
						"name":"微众虚拟商品1",
						"bar_code":"112233"
						},
					"create_time":"2天前"
				}]
				"""
		#查询结果为空
			When jobs设置福利卡券活动列表查询条件
				"""
				{
					"product_name":"",
					"product_bar_code":"",
					"create_start_time":"明天",
					"create_end_time":"2天后"
				}
				"""
			Then jobs获得福利卡券活动列表
				"""
				[]
				"""

	#组合查询
		When jobs设置福利卡券活动列表查询条件
			"""
			{
				"product_name":"微众",
				"product_bar_code":"212233",
				"create_start_time":"2天前",
				"create_end_time":"明天"
			}
			"""
		Then jobs获得福利卡券活动列表
			"""
			[{
				"activity_name":"20元通用卡",
				"product":{
					"name":"微众虚拟商品2",
					"bar_code":"212233"
					},
				"create_time":"今天"
			}]
			"""