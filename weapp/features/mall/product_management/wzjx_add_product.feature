# __author__ : "冯雪静"
#微众精选：添加商品
Feature: 添加商品
	Jobs能通过管理系统在商城中添加"商品"
	"""
	微众精选去掉商品规格，添加商品时，不需要考虑规格
	新添加了：供货商和采购价
	1.添加商品
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
	And jobs已添加供货商
		"""
		[{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"is_active": "启用"
		}]
		"""


@mall2 @addProduct
Scenario: 1 添加商品
	Jobs添加商品后，能获取他添加的商品

	Given jobs登录系统
	And jobs已添加商品
		#东坡肘子(供货商：土小宝，有分类，上架，无限库存，多轮播图), 叫花鸡(供货商：丹江湖，无分类，下架，有限库存，单轮播图),红烧肉(供货商：土小宝，免运费)
		"""
		[{
			"supplier": "土小宝",
			"name": "东坡肘子",
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"price": 10.00,
			"purchase_price": 9.00,
			"weight": 5.0,
			"stock_type": "无限"
		}, {
			"supplier": "丹江湖",
			"name": "叫花鸡",
			"category": "",
			"detail": "叫花鸡的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"price": 12.00,
			"purchase_price": 9.90,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"supplier": "土小宝",
			"name": "红烧肉",
			"category": "",
			"detail": "红烧肉的详情",
			"status": "在售",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"price": 12.0,
			"purchase_price": 9.99,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3,
			"postage": 0.0
		}]
		"""
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	#When jobs选择'顺丰'运费配置
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "土小宝",
			"name": "东坡肘子",
			"promotion_title": "促销的东坡肘子",
			"category": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"price": 10.00,
			"purchase_price": 9.00,
			"weight": 5.0,
			"stock_type": "无限"
		}
		"""
	And jobs能获取商品'叫花鸡'
		"""
		{
			"supplier": "丹江湖",
			"name": "叫花鸡",
			"category": "",
			"detail": "叫花鸡的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"price": 12.00,
			"purchase_price": 9.90,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3,
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}]
		}
		"""
	And jobs能获取商品'红烧肉'
		"""
		{
			"supplier": "土小宝",
			"name": "红烧肉",
			"category": "",
			"detail": "红烧肉的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"price": 12.0,
			"purchase_price": 9.99,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3,
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": 0.0
		}
		"""
	Given bill登录系统
	Then bill能获取商品列表
		"""
		[]
		"""
