# __author__ : "冯雪静"

Feature:用户订单导出功能
	jobs能导出用户的订单

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "L"
			}, {
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 L": {
						"price": 100.00
				},{
					"红色 M": {
						"price": 100.00
				},{
					"红色 S": {
						"price": 100.00
				}
			}
		},{
			"name": "商品2",
			"price": 100.00,
			"is_commit": "是"
		},{
			"name": "商品3",
			"integral": 100,
		}]	
		"""
	And bill关注jobs的公众号
	And jobs已有的会员
		"""
		[{
			"name": "bill",
			"integral": "500"
		}]
		"""
	And jobs添加优惠券规则
		"""
		[{
			"name": "优惠券",
			"money": 100,
			"count": 1,
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	And jobs已有的订单
		"""
		[{
			"order_no":"0000008",
			"member":"bill",
			"order_time":"2014-10-08 12:00",
			"type":"普通订单",
			"status":"待支付",
			"sources":"本店",
			"order_price":100.00,
			"payment_price":100.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"北京市,北京市,海淀区",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品1",
				"model":"红色 L",
				"count":1,
				"price":90.00
			}]
		},{
			"order_no":"0000007",
			"member":"bill",
			"order_time":"2014-10-07 12:00",
			"type":"测试订单",
			"status":"已取消",
			"sources":"本店",
			"order_price":100.00,
			"payment_price":0.01,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"河北省,唐山市,乐亭县",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品1",
				"model":"红色 M",
				"count":1,
				"price":90.00
			}]
		},{
			"order_no":"0000006",
			"member":"bill",
			"order_time":"2014-10-06 12:00",
			"type":"普通订单",
			"status":"待发货",
			"methods_of_payment":"支付宝",
			"sources":"本店",
			"order_price":100.00,
			"payment_price":100.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"天津市,天津市,和平区",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品1",
				"model":"红色 S",
				"count":1,
				"price":90.00
			}]
		},{
			"order_no":"0000005",
			"member":"bill",
			"order_time":"2014-10-05 12:00",
			"logistics_information":{
				"logistics":"顺丰",
				"number":"123",
				"shipper":"jobs"
			},
			"type":"普通订单",
			"status":"已发货",
			"methods_of_payment":"货到付款",
			"sources":"本店",
			"order_price":100.00,
			"payment_price":100.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"山西省,太原市,小店区",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品1",
				"model":"红色 L",
				"count":1,
				"price":90.00
			}]
		},{

			"order_no":"0000004",
			"member":"bill",
			"order_time":"2014-10-04 12:00",
			"logistics_information":{
				"logistics":"顺丰",
				"number":"124",
				"shipper":"jobs"
			},
			"type":"普通订单",
			"status":"已完成",
			"methods_of_payment":"微众卡支付",
			"sources":"商户",
			"order_price":100.00,
			"payment_price":100.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"辽宁省,沈阳市,和平区",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品2",
				"count":1,
				"price":90.00
			}]
		},{
			"order_no":"0000003",
			"member":"bill",
			"order_time":"2014-10-03 12:00",
			"type":"普通订单",
			"status":"待发货",
			"methods_of_payment":"优惠抵扣",
			"sources":"商户",
			"coupon":{
				"coupon_code":"coupon1_id_1",
				"name":"优惠券",
				"price":100.00
			},
			"order_price":100.00,
			"payment_price":0.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"河南省,安阳市,汤阴县",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品2",
				"count":1,
				"price":90.00
			}]

		},{
			"order_no":"0000002",
			"member":"bill",
			"order_time":"2014-10-02 12:00",
			"logistics_information":{
				"logistics":"顺丰",
				"number":"125",
				"shipper":"jobs"
			},
			"type":"普通订单",
			"status":"已发货",
			"methods_of_payment":"优惠抵扣",
			"sources":"商户",
			"member": "bill",
			"integral":100,
			"order_price":100.00,
			"payment_price":0.00,
			"freight":10.00,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"河南省,安阳市,汤阴县",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品2",
				"count":1,
				"price":90.00
			}]
		},{

			"order_no":"0000001",
			"member":"bill",
			"order_time":"2014-10-01 12:00",
			"logistics_information":{
				"logistics":"顺丰",
				"number":"126",
				"shipper":"jobs|发货一箱"
			},
			"type":"积分商品",
			"status":"已完成",
			"methods_of_payment":"优惠抵扣",
			"sources":"本店",
			"member": "bill",
			"integral":100,
			"order_price":100,
			"payment_price":100,
			"freight":0.0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_area":"辽宁省,沈阳市,和平区",
			"ship_address":"泰兴大厦",
			"product":[{
				"name":"商品3",
				"count":1,
				"integral":100
			}]
		}]
		"""
	

@ignore 
Scenario:导出订单
	jobs选择条件后
	1. jobs选择一个条件时,导出对应的订单
	2. jobs选择多个条件时,导出对应的订单
	3. jobs选择全部条件时,导出对应的订单
	4. jobs填写详细信息时,导出对应的订单
	5. jobs选择固定标签时,导出对应的订单

	Given jobs登录系统
	When jobs选择条件为
		"""
		{
			"order_time":"2014-10-05|2014-10-08"
		}
		""" 
	Then jobs导出订单
		"""
		[{	
			"order_time":"2014-10-8 12:00",
			"order_no":"0000008",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"",
			"payment_price":100.00,
			"status":"待支付",
			"type":"普通订单",
			"trade_name":"商品1",
			"model":"红色 L",
			"count":1,
			"sources":"本店",
			"integral":0,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"北京市",
			"ship_address":"北京市,北京市,海淀区,泰兴大厦",
			"shipper":"",
			"shipper_note":"",
			"logistics":"",
			"number":""

		},{
			"order_time":"2014-10-7 12:00",
			"order_no":"0000007",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"",
			"payment_price":0.01,
			"status":"已取消",
			"type":"测试订单",
			"trade_name":"商品1",
			"model":"红色 M",
			"count":1,
			"sources":"本店",
			"integral":0,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"河北省",
			"ship_address":"河北省,唐山市,乐亭县,泰兴大厦",
			"shipper":"",
			"shipper_note":"",
			"logistics":"",
			"number":""
		},{
			"order_time":"2014-10-6 12:00",
			"order_no":"0000006",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"支付宝",
			"payment_price":100.00,
			"status":"待发货",
			"type":"普通订单",
			"trade_name":"商品1",
			"model":"红色 S",
			"count":1,
			"sources":"本店",
			"integral":0,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"天津市",
			"ship_address":"天津市,天津市,和平区,泰兴大厦",
			"shipper":"",
			"shipper_note":"",
			"logistics":"",
			"number":""
		},{
			"order_time":"2014-10-5 12:00",
			"order_no":"0000005",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"货到付款",
			"payment_price":100.00,
			"status":"已发货",
			"type":"普通订单",
			"trade_name":"商品1",
			"model":"红色 L",
			"count":1,
			"sources":"本店",
			"integral":0,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"山西省",
			"ship_address":"山西省,太原市,小店区,泰兴大厦",
			"shipper":"jobs",
			"shipper_note":"",
			"logistics":"顺丰",
			"number":"123"
		}]
		"""

	When jobs选择条件为
		"""
		{
			"type": "积分商品",
			"order_time":"2014-10-01|2014-10-08"
		}
		""" 
	Then jobs导出订单
		"""
		{
			"order_time":"2014-10-1 12:00",
			"order_no":"0000001",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"优惠抵扣",
			"payment_price":0.00,
			"status":"已完成",
			"type":"积分商品",
			"trade_name":"商品3",
			"model":"",
			"count":1,
			"sources":"本店",
			"integral":100,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"辽宁省",
			"ship_address":"辽宁省,沈阳市,和平区,泰兴大厦",
			"shipper":"jobs",
			"shipper_note":"发货一箱",
			"logistics":"顺丰",
			"number":"126"
		}
		"""

	When jobs选择条件为
		"""
		[{
			"type": "普通订单",
			"status": "待支付",
			"source": "本店",
			"order_time":"2014-10-01|2014-10-08"
		}]
		""" 
	Then jobs导出订单
		"""
		{	
			"order_time":"2014-10-8 12:00",
			"order_no":"0000008",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"",
			"payment_price":100.00
			"status":"待支付",
			"type":"普通订单",
			"trade_name":"商品1",
			"model":"红色 L",
			"count":1,
			"sources":"本店",
			"integral":0,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"北京市",
			"ship_address":"北京市,北京市,海淀区,泰兴大厦",
			"shipper":"",
			"shipper_note":"",
			"logistics":"顺丰",
			"number":"126"
		}
		"""

	When jobs选择标签时间
		"""
		[{
			"type": "普通订单",
			"status": "已发货",
			"pay_interface_type": "优惠抵扣",
			"source": "商户"
			"order_time":"2014-10-01|2014-10-08"
		}]
		"""
	Then jobs导出订单
		"""
		{
			"order_time":"2014-10-2 12:00",
			"order_no":"0000002",
			"member":"bill",
			"order_price":100.00,
			"methods_of_payment":"优惠抵扣",
			"payment_price":0.00,
			"status":"已发货",
			"type":"普通订单",
			"trade_name":"商品2",
			"model":"",
			"count":1,
			"sources":"商户",
			"integral":100,
			"coupon_name":"",
			"coupon_amount":0,
			"ship_name":"bill",
			"ship_tel":"13013013011",
			"ship_province":"河南省",
			"ship_address":"河南省,安阳市,汤阴县,泰兴大厦",
			"shipper":"jobs",
			"shipper_note":"",
			"logistics":"顺丰",
			"number":"125"
		}
		"""

	When jobs选择标签时间
		"""
		[{
			"type":"测试订单",
			"order_time":"2014-10-01|2014-10-03"
		}]
		""" 
	Then jobs导出订单
		"""
		[]
		"""