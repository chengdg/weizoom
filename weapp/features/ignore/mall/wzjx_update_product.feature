# __author__ : "冯雪静"
#微众精选：修改商品的供货商
Feature: 更新商品的供货商
	Jobs能通过管理系统更新"商品的供货商"
	"""
	1.更新商品的供货商
	"""

Background:
	Given jobs登录系统
	And jobs已添加供货商
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
			"name": "东坡肘子"
		}, {
			"supplier": "丹江湖1",
			"name": "叫花鸡"
		}, {
			"supplier": "土小宝1",
			"name": "红烧肉"
		}]
		"""


Scenario: 1 更新商品的供货商
	jobs更新商品的供货商
	1.jobs获取商品

	Given jobs登录系统
	#更新商品的供货商
	When jobs更新商品'东坡肘子'
		"""
		{
			"supplier": "丹江湖1",
			"name": "东坡肘子"
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"supplier": "丹江湖1",
			"name": "东坡肘子"
		}
		"""
	#更新商品名字和供货商
	When jobs更新商品'叫花鸡'
		"""
		{
			"supplier": "土小宝1",
			"name": "花生油"
		}
		"""
	Then jobs能获取商品'叫花鸡'
		"""
		[]
		"""
	And jobs能获取商品'花生油'
		"""
		{
			"supplier": "土小宝1",
			"name": "花生油"
		}
		"""

