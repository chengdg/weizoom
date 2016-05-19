# watcher: fengxuejing@weizoom.com,benchi@weizoom.com
# __author__ : "冯雪静"

Feature: 自营平台创建团购活动
	"""
	自营平台创建团购活动-使用同步商品创建完团购活动后
		1.商户更新商品后，自营平台“更新”已参加团购活动进行中的商品提示：“该商品正在进行团购活动”
		2.商户更新商品后，自营平台“更新”已参加团购活动未开启的商品提示：“该商品正在进行团购活动”
		3.商户下架商品后，自营平台的团购活动自动结束
		4.商户删除商品后，自营平台的团购活动自动结束
		5.商户修改商品为多规格后，自营平台的团购活动自动结束
	"""

#特殊说明：jobs表示自营平台,bill表示商家
Background:
	#商家bill的商品信息
	Given 添加bill店铺名称为'bill商家'
	Given bill登录系统
	When bill已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And bill添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And bill选择'顺丰'运费配置
	And bill已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And bill已添加商品
		"""
		[{
			"name": "bill无规格商品1",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": 2.00
		},{
			"name": "bill无规格商品2",
			"created_at": "2015-07-03 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 22.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": "顺丰"
		},{
			"name": "bill无规格商品3",
			"created_at": "2015-07-04 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 33.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			}
		},{
			"name": "bill多规格商品4",
			"created_at": "2015-07-05 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 44.12,
						"user_code":"4412",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			}
		}]
		"""
	#自营平台jobs登录
	Given 设置jobs为自营平台账号
	Given jobs登录系统
	When jobs添加微信证书
	When jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	And jobs选择'顺丰'运费配置
	And jobs将商品池商品批量放入待售于'2015-08-02 12:30'
		"""
		[
			"bill多规格商品4",
			"bill无规格商品3",
			"bill无规格商品2",
			"bill无规格商品1"
		]
		"""
	When jobs更新商品'bill多规格商品4'
		"""
		{
			"name": "bill多规格商品4",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"model": {
				"models": {
					"standard": {
						"price": 444.12,
						"user_code":"4412",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			},
			"postage":10.00
		}
		"""
	When jobs更新商品'bill无规格商品3'
		"""
		{
			"name": "bill无规格商品3",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"model": {
				"models": {
					"standard": {
						"price": 333.12,
						"user_code":"3312",
						"weight":1.0,
						"stock_type": "有限",
						"stocks":100
					}
				}
			}
		}
		"""
	When jobs更新商品'bill无规格商品2'
		"""
		{
			"name": "bill无规格商品2",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"model": {
				"models": {
					"standard": {
						"price": 222.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": 10.00
		}
		"""
	When jobs更新商品'bill无规格商品1'
		"""
		{
			"name": "bill无规格商品1",
			"supplier":"bill商家",
			"purchase_price": 9.00,
			"model": {
				"models": {
					"standard": {
						"price": 122.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": "顺丰"
		}
		"""
	When jobs批量上架商品
		"""
		[
			"bill多规格商品4",
			"bill无规格商品3",
			"bill无规格商品2",
			"bill无规格商品1"
		]
		"""
	When jobs新建团购活动
		"""
		[{
			"group_name":"团购活动1",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"bill无规格商品1",
			"group_dict":
				[{
					"group_type":5,
					"group_days":1,
					"group_price":10.00
				}],
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动1分享描述"
		},{
			"group_name":"团购活动2",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"bill无规格商品2",
			"group_dict":
				[{
					"group_type":5,
					"group_days":1,
					"group_price":20.00
				},{
					"group_type":10,
					"group_days":2,
					"group_price":21.00
				}],
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动2分享描述"
		},{
			"group_name":"团购活动3",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"bill无规格商品3",
			"group_dict":
				[{
					"group_type":5,
					"group_days":1,
					"group_price":30.00
				}],
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动3分享描述"
		},{
			"group_name":"团购活动4",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"bill多规格商品4",
			"group_dict":
				[{
					"group_type":5,
					"group_days":1,
					"group_price":40.00
				},{
					"group_type":10,
					"group_days":2,
					"group_price":41.00
				}],
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动4分享描述"
		}]
		"""
	When jobs开启团购活动'团购活动1'
	When jobs开启团购活动'团购活动3'
	When jobs开启团购活动'团购活动4'

@eugene @product_pool
Scenario:1 对团购活动中的(同步商品)进行更新商品操作
	商户更新已在自营平台创建团购活动的商品
	1.自营平台的商品池显示“待更新”
	2.自营平台点击“更新”提示：“该商品正在进行团购活动”

	Given bill登录系统
	#商户修改商品，商品池显示更新
	When bill更新商品'bill无规格商品1'
		"""
		{
			"name": "bill商品1",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 111.12,
						"user_code":"1112",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": 2.00
		}
		"""
	When bill更新商品'bill无规格商品2'
		"""
		{
			"name": "bill商品2",
			"created_at": "2015-07-03 10:20",
			"model": {
				"models": {
					"standard": {
						"price": 22.12,
						"user_code":"2212",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			},
			"postage": "顺丰"
		}
		"""
	#自营平台jobs登录
	Given jobs登录系统
	When jobs更新商品池商品'bill商品1'于'2015-08-03 10:30'
	Then jobs获得提示信息'该商品正在进行团购活动'
	When jobs更新商品池商品'bill商品2'于'2015-08-03 10:30'
	Then jobs获得提示信息'该商品正在进行团购活动'

@eugene @product_pool
Scenario:2 商户对自营平台团购活动中的(同步商品)进行下架和删除商品操作
	商户下架已在自营平台创建团购活动的商品
	1.自营平台团购活动自动结束

	Given bill登录系统
	#商户下架商品
	When bill'下架'商品'bill无规格商品2'

	#自营平台jobs登录
	Given jobs登录系统
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动4",
			"status":"进行中"
		},{
			"name":"团购活动3",
			"status":"进行中"
		},{
			"name":"团购活动1",
			"status":"进行中"
		},{
			"name":"团购活动2",
			"status":"已结束"
		}]
		"""
	Given bill登录系统
	#商户删除商品
	When bill'永久删除'商品'bill无规格商品3'

	#自营平台jobs登录
	Given jobs登录系统
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动4",
			"status":"进行中"
		},{
			"name":"团购活动1",
			"status":"进行中"
		},{
			"name":"团购活动3",
			"status":"已结束"
		},{
			"name":"团购活动2",
			"status":"已结束"
		}]
		"""

@eugeneTMP
Scenario:3 商户对自营平台团购活动中的(同步商品)进行修改成多规格商品
	商户修改已在自营平台创建团购活动的商品为多规格
	1.自营平台团购活动自动结束

	Given bill登录系统
	#商户修改商品为多规格
	When bill更新商品'bill多规格商品4'
		"""
		{
			"name": "bill多规格商品4",
			"created_at": "2015-07-05 10:20",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"M": {
						"price": 30.00,
						"weight": 1,
						"stock_type": "有限",
						"stocks": 100
					},
					"S": {
						"price": 30.00,
						"weight": 2,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	#自营平台jobs登录
	Given jobs登录系统
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动3",
			"status":"进行中"
		},{
			"name":"团购活动1",
			"status":"进行中"
		},{
			"name":"团购活动2",
			"status":"未开启"
		},{
			"name":"团购活动4",
			"status":"已结束"
		}]
		"""




