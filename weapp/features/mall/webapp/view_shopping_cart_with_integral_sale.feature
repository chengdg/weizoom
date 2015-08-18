# __edit__ : "benchi"
#积分商品在购物车中的展现形式与普通商品没有差别，故此处feathure无需重复，先留出数据接口，便于后续改动用
@func:webapp.modules.mall.views.list_products
Feature: 添加参与积分应用活动的商品到购物车中

Background:
	Given jobs登录系统
	And jobs已添加商品规格
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
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 30
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9,
						"stock_type": "无限"
					}
				}   
			}
		}, {
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"discount": 70,
			"discount_money": 70.0,
			"is_permanant_active": false
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"product_name": "商品3",
			"discount": 50,
			"discount_money": 25.0,
			"is_permanant_active": true
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号

