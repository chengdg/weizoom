# __author__ : "王丽"

Feature: 会员详情-收货信息
"""
	会员设置的收回地址
	1、【收货人】：收货人的姓名
	2、【手机号码】：手机号码校验，必须是11位的手机号
	3、【选择地区】：选择省份、城市、地区
	4、【详细地址】：详细地址，手工填写
"""

Background:
	Given jobs登录系统

	And bill关注jobs的公众号

	When bill访问jobs的webapp
	When bill添加收货地址
		"""
		[{
			"name":"收货人1",
			"phone":"15933556587",
			"area":"选择的城市地区1"，
			"detailed_address":"详细地址1"
		}]
		"""

Scenario:1 添加收货地址

	Given jobs登录系统
	
	And bill关注jobs的公众号

	Then jobs获得"bill"的收货信息
		"""
		[{
			"address":"选择的城市地区1详细地址1",
			"name":"收货人1",
			"phone":"15933556587"
		}]
		"""

	When bill访问jobs的webapp
	When bill添加收货地址
		"""
		[{
			"name":"收货人2",
			"phone":"15933556586",
			"area":"选择的城市地区2"，
			"detailed_address":"详细地址2"
		}]
		"""

	Given jobs登录系统

	Then jobs获得"bill"的收货信息
		"""
		[{
			"address":"选择的城市地区1详细地址1",
			"name":"收货人1",
			"phone":"15933556587"
		},{
			"address":"选择的城市地区2详细地址2",
			"name":"收货人2",
			"phone":"15933556586"
		}]
		"""

Scenario:2 编辑收货地址

	When bill访问jobs的webapp
	When bill编辑收货地址
		"""
		[{
			"name":"收货人1修改",
			"phone":"15933556587",
			"area":"选择的城市地区1修改"，
			"detailed_address":"详细地址1修改"
		}]
		"""

	Given jobs登录系统

	Then jobs获得"bill"的收货信息
		"""
		[{
			"address":"选择的城市地区1修改详细地址1修改",
			"name":"收货人1修改",
			"phone":"15933556587"
		}]
		"""

Scenario:3 删除收货地址

	When bill访问jobs的webapp
	When bill删除收货地址
		"""
		[{
			"name":"收货人1",
			"phone":"15933556587",
			"area":"选择的城市地区1"，
			"detailed_address":"详细地址1"
		}]
		"""

	Given jobs登录系统
	
	Then jobs获得"bill"的收货信息
		"""
		[]
		"""
		