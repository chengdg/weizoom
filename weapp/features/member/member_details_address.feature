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
	When bill已添加收货地址
		"""
		[{
			"address":"北京市 北京市 海淀区 详细地址1",
			"ship_name":"收货人1",
			"ship_tel":"15933556587"
		},{
			"ship_name":"收货人2",
			"ship_tel":"15933556586",
			"ship_area":"天津市 天津市 河西区"，
			"ship_address":"详细地址2"
		}]
		"""

Scenario:1 会员详情获得收货地址列表

	Given jobs登录系统

	Then jobs获得"bill"的收货信息
		"""
		[{
			"address":"北京市 北京市 海淀区 详细地址1",
			"ship_name":"收货人1",
			"ship_tel":"15933556587"
		},{
			"address":"天津市 天津市 河西区 详细地址2",
			"ship_name":"收货人2",
			"ship_tel":"15933556586"
		}]
		"""

Scenario:2 编辑收货地址

	When bill访问jobs的webapp
	When bill编辑收货地址
		"""
		[{
			"ship_name":"收货人1修改",
			"ship_tel":"15933556587",
			"ship_area":"北京市 北京市 西城区"，
			"ship_address":"详细地址1修改"
		}]
		"""

	Given jobs登录系统

	Then jobs获得"bill"的收货信息
		"""
		[{
			"address":"北京市 北京市 西城区 详细地址1修改",
			"ship_name":"收货人1修改",
			"ship_tel":"15933556587"
		}]
		"""

Scenario:3 删除收货地址

	When bill访问jobs的webapp
	When bill删除收货地址
		"""
		[{
			"ship_name":"收货人1",
			"ship_tel":"15933556587",
			"ship_area":"北京市 北京市 海淀区"，
			"ship_address":"详细地址1"
		}]
		"""

	Given jobs登录系统

	Then jobs获得"bill"的收货信息
		"""
		[]
		"""
