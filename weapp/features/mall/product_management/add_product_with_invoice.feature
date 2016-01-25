#_author_:张三香 2016.01.20


Feature:添加新商品
	"""
	1.在添加新商品页面，添加字段：商品发票，默认是勾选状态
	2.字段位置：运费及支付中【配送时间】的下面
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	When jobs已添加支付方式
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

@product @addProduct @mall2
Scenario:1 添加无规格新商品,支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"status": "待售",
			"invoice":true,
			"model": {
					"models": {
						"standard": {
							"price": 12.0,
							"weight": 5.5,
							"stock_type": "有限",
							"stocks": 3
						}
					}
				}
		}]
		"""
	Then jobs能获取商品'支持开票商品'
		"""
		{
			"name": "支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"invoice":true,
			"is_use_custom_model": "否",
			"model": {
					"models": {
						"standard": {
							"price": 12.0,
							"weight": 5.5,
							"stock_type": "有限",
							"stocks": 3
						}
					}
				}
		}
		"""

@product @addProduct @mall2
Scenario:2 添加多规格新商品,支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "多规格支持开票",
			"is_enable_model": "启用规格",
			"invoice":true,
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'多规格支持开票'
		"""
		{
			"is_enable_model": "启用规格",
			"invoice":true,
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 S": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""

@product @addProduct @mall2
Scenario:3 添加新商品,不支持开票
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "不支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"status": "待售",
			"invoice":false,
			"model": {
					"models": {
						"standard": {
							"price": 12.0,
							"weight": 5.5,
							"stock_type": "有限",
							"stocks": 3
						}
					}
				}
		}]
		"""
	Then jobs能获取商品'不支持开票商品'
		"""
		{
			"name": "不支持开票商品",
			"category": "",
			"detail": "商品的详情",
			"invoice":false,
			"is_use_custom_model": "否",
			"model": {
					"models": {
						"standard": {
							"price": 12.0,
							"weight": 5.5,
							"stock_type": "有限",
							"stocks": 3
						}
					}
				}
		}
		"""