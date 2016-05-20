# watcher: benchi@weizoom.com, zhangsanxiang@weizoom.com
#_author_:张三香 2016.05.20

Feature:新建福利卡券
	"""
		1、虚拟商品和其他实物商品一样，可以参与促销活动（会员价、限时、买赠、积分抵扣、多商品券及团购）
		2、新建福利卡券页面信息:
			'商品信息'：
				a.选择商品时，可按照'商品名称'和'商品条码'进行查询
				b.不设置查询条件，点击【查询】后弹窗中显示所有在售商品列表，商品只能单选
				c.选择商品后，显示商品信息（名称、图片、条码）、商品价格、库存、操作（【删除】）
				d.同一商品只能存在一个福利卡券活动中
			'活动名称':输入福利卡券活动的名称
			'卡券有效期':开始和结束时间
			上传码库文件：
				a.以上传csv格式方式添加码库；csv文件中需要显示卡号与密码字段，如果无密码，则为空
				b.如果某csv文件已经被使用，再次上传时，保存活动时进行校验提示“该文件内卡券已经在使用中，请确认后再操作”
				c.csv文件上传完后，显示码库的数量
				d.csv文件中如果有未激活或已过期状态的卡号，则应校验提示上传失败
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
			"is_virtual_product":"true",
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
			"is_virtual_product":"true",
			"supplier": "微众",
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
			"detail": "微众虚拟商品2的详情",
			"status": "在售"
		},{
			"name": "稻香村虚拟商品3",
			"product_type":"虚拟",
			"is_virtual_product":"true",
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
			"status":"在售"
		}]
		"""
	#创建csv文件中需要的卡信息
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
				"status":"未激活",
				"price":10.00
			}]
		}
		"""

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
			"creat_time":"今天"
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
			"card_stocks":2,
			"card_sales":0,
			"create_time":"今天",
			"actions":["发放详情","编辑","结束"]
		}]
		"""

Scenario:2 新建福利卡活动，csv中包含非有效卡信息时，则上传不成功
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
				},{
					"id":"0000003",
					"password":"3234567"
				}],
			"creat_time":"今天"
		}]
		"""
	Then jobs获得提示信息'上传失败'

Scenario:3 新建福利卡活动，csv中包含正在使用的卡信息时，则上传不成功
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
			"creat_time":"今天"
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
				}],
			"creat_time":"今天"
		}]
		"""
	Then jobs获得提示信息'该文件内卡券已经在使用中，请确认后再操作'