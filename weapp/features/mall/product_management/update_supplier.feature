# __author__ : "冯雪静"
#微众精选：修改供货商影响商品
Feature: 修改供货商影响商品
	Jobs能通过管理系统修改"供货商"
	"""
	1.修改供货商影响商品
		修改供货商名称和修改供货商内容
	2.删除供货商影响商品
		删除关联在售商品的供货商和删除关联待售商品的供货商
	"""


Background:
	Given jobs登录系统
	And jobs添加供货商
		"""
		[{
			"name": "土小宝1",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖1",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"supplier": "土小宝1",
			"name": "东坡肘子",
			"status": "在售",
			"price": 10.00,
			"purchase_price":9.00,
			"weight": 5.0,
			"stock_type": "无限"
		}, {
			"supplier": "丹江湖1",
			"name": "叫花鸡",
			"status":"待售",
			"price":12.00,
			"purchase_price":9.90,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"supplier": "土小宝1",
			"name": "红烧肉",
			"status": "在售",
			"price": 12.0,
			"purchase_price": 9.99,
			"weight": 5.5,
			"stock_type": "有限",
			"stocks": 3
		}]
		"""

@supplier @product @mall2
Scenario: 1 修改供货商影响商品
	jobs修改已被商品使用的供货商名字
	1.jobs获取商品

	#修改供货商名字影响商品，商品使用的供货商名字也会更新
	Given jobs登录系统
	When jobs修改供货商'土小宝1'
		"""
		{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "土小宝",
			"name": "东坡肘子",
			"price": 10.00,
			"purchase_price": 9.00,
			"stock_type": "无限"
		}
		"""
	And jobs能获取商品'叫花鸡'
		"""
		{
			"supplier": "丹江湖1",
			"name": "叫花鸡",
			"price": 12.00,
			"purchase_price": 9.90,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取商品'红烧肉'
		"""
		{
			"supplier": "土小宝",
			"name": "红烧肉",
			"price": 12.0,
			"purchase_price": 9.99,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	#修改供货商信息，不修改名字，不会影响商品
	When jobs修改供货商'丹江湖1'
		"""
		{
			"name": "丹江湖1",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "卖鸭蛋"
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "土小宝",
			"name": "东坡肘子",
			"price": 10.00,
			"purchase_price": 9.00,
			"stock_type": "无限"
		}
		"""
	And jobs能获取商品'叫花鸡'
		"""
		{
			"supplier": "丹江湖1",
			"name": "叫花鸡",
			"price": 12.00,
			"purchase_price": 9.90,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取商品'红烧肉'
		"""
		{
			"supplier": "土小宝",
			"name": "红烧肉",
			"price": 12.0,
			"purchase_price": 9.99,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取供货商列表
		"""
		[{
			"name": "丹江湖1"
		}, {
			"name": "土小宝"
		}]
		"""


@supplier @product @mall2
Scenario: 2 删除供货商影响商品
	jobs删除已被商品使用的供货商名字
	1.jobs获取商品

	Given jobs登录系统
	#删除供货商时，有关联的在售商品，提示错误信息，商品不受影响
	When jobs删除供货商'土小宝1'
	Then jobs提示错误信息'请先删除与该供货商有关的商品'
	And jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "土小宝1",
			"name": "东坡肘子",
			"price": 10.00,
			"purchase_price": 9.00,
			"stock_type": "无限"
		}
		"""
	And jobs能获取商品'叫花鸡'
		"""
		{
			"supplier": "丹江湖1",
			"name": "叫花鸡",
			"price": 12.00,
			"purchase_price": 9.90,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取商品'红烧肉'
		"""
		{
			"supplier": "土小宝1",
			"name": "红烧肉",
			"price": 12.0,
			"purchase_price": 9.99,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	#删除供货商时，有关联的待售商品，提示错误信息，商品不受影响
	When jobs删除供货商'丹江湖1'
	Then jobs提示错误信息'请先删除与该供货商有关的商品'
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "土小宝1",
			"name": "东坡肘子",
			"price": 10.00,
			"purchase_price": 9.00,
			"stock_type": "无限"
		}
		"""
	And jobs能获取商品'叫花鸡'
		"""
		{
			"supplier": "丹江湖1",
			"name": "叫花鸡",
			"price": 12.00,
			"purchase_price": 9.90,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取商品'红烧肉'
		"""
		{
			"supplier": "土小宝1",
			"name": "红烧肉",
			"price": 12.0,
			"purchase_price": 9.99,
			"stock_type": "有限",
			"stocks": 3
		}
		"""
	And jobs能获取供货商列表
		"""
		[{
			"name": "丹江湖1"
		}, {
			"name": "土小宝1"
		}]
		"""
