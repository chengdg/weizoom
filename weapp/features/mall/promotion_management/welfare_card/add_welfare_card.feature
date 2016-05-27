# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:新建福利卡券
	"""
		1、虚拟商品和其他实物商品一样，可以参与促销活动（会员价、限时、买赠、积分抵扣、多商品券及团购）
		2、新建福利卡券页面信息:
			'商品信息'：
				a.选择商品时，可按照'商品名称'和'商品条码'进行查询
				b.不设置查询条件，点击【查询】后弹窗中显示所有在售虚拟商品列表，商品只能单选
				c.选择商品后，显示商品信息（名称、图片、条码）、商品价格、库存、操作（【删除】）
				d.同一商品只能存在一个福利卡券活动中
			'活动名称':输入福利卡券活动的名称
			'卡券有效期':开始和结束时间
			上传码库文件的校验：
				a.以上传xls/xlsx格式方式添加码库；码库文件要严格按照格式进行填写（卡号、密码）
				b.上传码库文件时会对以下情况均会进行校验：
					卡号为空，密码非空
					卡号非空，密码为空
					卡号相同，密码不同/相同
					卡号在其他福利卡券中有上传
					编辑福利卡券时，包含创建时已经上传的卡号（只识别新补充的卡号信息，不更改已经上传的卡号信息）
					卡号状态为未激活、已过期、已失效
		3、新建福利卡券活动时，商品弹窗信息
			a.弹窗名称：在售虚拟商品
			b.弹窗中列表显示以下信息:
				【商品条码】、【商品名称】、【商品价格】、【商品库存】【创建时间】、【操作】
		4、上传码库后，自动更新商品的库存
	"""

Background:
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		},{
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
			"stocks": 0,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
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
			"name": "微众虚拟商品2",
			"product_type":"微众卡",
			"supplier": "微众",
			"purchase_price": 19.00,
			"promotion_title": "虚拟商品2",
			"categories": "",
			"bar_code":"212233",
			"price": 20.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 0,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				}],
			"detail": "微众虚拟商品2的详情",
			"status": "在售"
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
			"stocks": 0,
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
			"status":"在售"
		}]
		"""
	#创建码库文件中需要的卡信息
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
				"price":10.00
			},{
				"id":"0000004",
				"password":"4234567",
				"status":"未使用",
				"price":10.00
			}]
		}
		"""

@welfare_card @weshop
Scenario:1 新建福利卡券活动
	Given jobs登录系统
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
			"card_start_date":"今天",
			"card_end_date":"30天后",
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				}],
			"create_time":"今天"
		}]
		"""
	Then jobs获得福利卡券活动列表
		"""
		[{
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
			"create_time":"今天",
			"actions":["码库详情","增加库存","结束"]
		}]
		"""
	#上传码库后，自动更新商品库存
	And jobs能获取商品'微众虚拟商品1'
		"""
		{
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
			"stocks": 2,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				},{
					"type": "货到付款"
				}],
			"detail":"微众虚拟商品1的详情"
		}
		"""

@welfare_card @weshop
Scenario:2 新建福利卡券活动，码库文件中包含非有效卡信息时，则上传不成功
	Given jobs登录系统
	#码库文件中有重复卡号
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
				"card_start_date":"今天",
				"card_end_date":"30天后",
				"cards":
					[{
						"id":"0000001",
						"password":"1234567"
					},{
						"id":"0000002",
						"password":"2234567"
					},{
						"id":"0000002",
						"password":"2234567"
					}],
				"create_time":"今天"
			}]
			"""
		Then jobs获得提示信息'第3行卡号与前面重复，请核查!'
	#码库文件中卡号或密码为空
		#卡密码为空
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
				"card_start_date":"今天",
				"card_end_date":"30天后",
				"cards":
					[{
						"id":"0000001",
						"password":"1234567"
					},{
						"id":"0000002",
						"password":""
					}],
				"create_time":"今天"
			}]
			"""
		Then jobs获得提示信息'第2行数据有误，请核查!'
		#卡号为空
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
				"card_start_date":"今天",
				"card_end_date":"30天后",
				"cards":
					[{
						"id":"0000001",
						"password":"1234567"
					},{
						"id":"",
						"password":"2234567"
					}],
				"create_time":"今天"
			}]
			"""
		Then jobs获得提示信息'第2行数据有误，请核查!'
		#卡号和密码均为空
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
				"card_start_date":"今天",
				"card_end_date":"30天后",
				"cards":
					[{
						"id":"",
						"password":""
					},{
						"id":"0000001",
						"password":"1234567"
					}],
				"create_time":"今天"
			}]
			"""
		Then jobs获得提示信息'第1行数据有误，请核查!'

@welfare_card @weshop
Scenario:3 新建福利卡券活动，码库文件中包含正在使用的卡信息时，只读取可用的卡信息
	Given jobs登录系统
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
			"card_start_date":"今天",
			"card_end_date":"30天后",
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				}],
			"create_time":"今天"
		}]
		"""

	When jobs新建福利卡券活动
		"""
		[{
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
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000003",
					"password":"3234567"
				}],
			"create_time":"今天"
		}]
		"""
	Then jobs获得福利卡券活动列表
		"""
		[{
			"activity_name":"20元通用卡",
			"product":{
				"name":"微众虚拟商品2",
				"bar_code":"212233"
			},
			"total_stocks":1,
			"remain_stocks":1,
			"sale_cards":0,
			"expired_cards":0,
			"invalid_cards":0,
			"create_time":"今天",
			"actions":["码库详情","增加库存","结束"]
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
			"create_time":"今天",
			"actions":["码库详情","增加库存","结束"]
		}]
		"""

@welfare_card @weshop
Scenario:4 新建福利卡券活动，商品弹窗的校验
	Given jobs登录系统
	Given jobs已添加商品
		"""
		[{
			"name": "微众虚拟商品4",
			"product_type":"微众卡",
			"supplier": "微众",
			"purchase_price": 9.00,
			"promotion_title": "40元通用卡",
			"categories": "分类1,分类2",
			"bar_code":"412233",
			"min_limit":2,
			"is_member_product":"on",
			"price": 40.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 0,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
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
			"status":"待售"
		},{
			"name": "微众普通商品5",
			"product_type":"普通商品",
			"supplier": "微众",
			"purchase_price": 49.00,
			"promotion_title": "普通商品5",
			"categories": "",
			"bar_code":"512233",
			"price": 50.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 5,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"postage":0.00,
			"pay_interfaces":
				[{
					"type": "在线支付"
				}],
			"detail": "微众普通商品5的详情",
			"status": "在售"
		}]
		"""
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":"",
			"bar_code":""
		}
		"""
	Then jobs新建福利卡券活动时能获得在售虚拟商品列表
		| bar_code  | name             | price | stocks | create_time    | actions |
		| 312233    | 稻香村虚拟商品3  | 30.00 | 0      | 今天           |  选取   |
		| 212233    | 微众虚拟商品2    | 20.00 | 0      | 今天           |  选取   |
		| 112233    | 微众虚拟商品1    | 10.00 | 0      | 今天           |  选取   |

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
			"card_start_date":"今天",
			"card_end_date":"30天后",
			"cards":
				[{
					"id":"0000001",
					"password":"1234567"
				},{
					"id":"0000002",
					"password":"2234567"
				}],
			"create_time":"今天"
		}]
		"""
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":"",
			"bar_code":""
		}
		"""
	Then jobs新建福利卡券活动时能获得在售虚拟商品列表
		| bar_code  | name             | price | stocks | create_time    | actions |
		| 312233    | 稻香村虚拟商品3  | 30.00 | 0      | 今天           |  选取   |
		| 212233    | 微众虚拟商品2    | 20.00 | 0      | 今天           |  选取   |
		| 112233    | 微众虚拟商品1    | 10.00 | 2      | 今天           |  已使用 |