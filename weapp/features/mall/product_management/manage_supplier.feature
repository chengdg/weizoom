# __author__ : "冯雪静"

Feature: 管理供货商
	jobs通过管理系统管理供货商
	"""
	1.添加供货商
	2.删除供货商
	3.修改供货商
	4.导出供货商,查询供货商,根据查询条件导出,模糊查询和精确查询
	"""


@supplier @add_supplier @mall2
Scenario: 1 添加供货商
	jobs添加供货商后
	1.按时间倒序排列

	#名称，负责人，电话，地址为必填项，备注选填
	#土小宝1有备注，丹江湖2没有备注
	Given jobs登录系统
	When jobs添加供货商
		"""
		[{
			"name": "土小宝1",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	Then jobs能获取供货商'土小宝1'
		"""
		{
			"name": "土小宝1",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}
		"""
	And jobs能获取供货商'丹江湖2'
		"""
		{
			"name": "丹江湖2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}
		"""
	And jobs能获取供货商列表
		"""
		[{
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""


@supplier @del_supplier @mall2
Scenario: 2 删除供货商
	jobs添加供货商后
	1.可进行删除

	#添加三个供货商，删除一个，获取供货商列表
	Given jobs登录系统
	When jobs添加供货商
		"""
		[{
			"name": "土小宝1",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}, {
			"name": "波尼亚",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	Then jobs能获取供货商列表
		"""
		[{
			"name": "波尼亚",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""
	When jobs删除供货商'波尼亚'
	Then jobs能获取供货商列表
		"""
		[{
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""


@supplier @mod_supplier @mall2
Scenario: 3 修改供货商
	jobs添加供货商后
	1.可进行修改

	Given jobs登录系统
	When jobs添加供货商
		"""
		[{
			"name": "土小宝1",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}, {
			"name": "波尼亚",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	Then jobs能获取供货商列表
		"""
		[{
			"name": "波尼亚",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""
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
	Then jobs能获取供货商'土小宝1'
		"""
		{}
		"""
	Then jobs能获取供货商'土小宝'
		"""
		{
			"name": "土小宝",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}
		"""
	When jobs修改供货商'丹江湖2'
		"""
		{
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13812345678",
			"supplier_address": "泰兴大厦",
			"remark": "卖鸭蛋"
		}
		"""
	Then jobs能获取供货商'丹江湖'
		"""
		{
			"name": "丹江湖",
			"responsible_person": "陌陌",
			"supplier_tel": "13812345678",
			"supplier_address": "泰兴大厦",
			"remark": "卖鸭蛋"
		}
		"""
	And jobs能获取供货商列表
		"""
		[{
			"name": "波尼亚",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "丹江湖",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": "卖鸭蛋"
		}, {
			"name": "土小宝",
			"create_at": "今天",
			"responsible_person": "宝宝",
			"remark": "备注卖花生油"
		}]
		"""


@supplier @mall2 @ex_supplier
Scenario: 4 导出供货商
	jobs添加供货商后
	1.导出全部供货商
	2.根据查询条件导出

	Given jobs登录系统
	When jobs添加供货商
		"""
		[{
			"name": "土小宝1",
			"responsible_person": "负责人",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "丹江湖2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}, {
			"name": "波尼亚1",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	Then jobs能获取供货商列表
		"""
		[{
			"name": "波尼亚1",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""
	When jobs导出'供货商'
	Then jobs能获取导出供货商信息
		|  name   | responsible_person | supplier_tel |   supplier_address   |    remark    |
		| 波尼亚1 |       陌陌         | 13811223344  | 北京市海淀区泰兴大厦 |              |
		| 丹江湖2 |       陌陌         | 13811223344  | 北京市海淀区泰兴大厦 |              |
		| 土小宝1 |       负责人       | 13811223344  | 北京市海淀区泰兴大厦 | 备注卖花生油 |

	#查询供货商可以模糊查询
	When jobs查询供货商
		"""
		{
			"name": "1"
		}
		"""
	Then jobs能获取供货商列表
		"""
		[{
			"name": "波尼亚1",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}, {
			"name": "土小宝1",
			"create_at": "今天",
			"responsible_person": "负责人",
			"remark": "备注卖花生油"
		}]
		"""
	When jobs导出'供货商'
	Then jobs能获取导出供货商信息
		|  name   | responsible_person | supplier_tel |   supplier_address   |    remark    |
		| 波尼亚1 |       陌陌         | 13811223344  | 北京市海淀区泰兴大厦 |              |
		| 土小宝1 |       负责人       | 13811223344  | 北京市海淀区泰兴大厦 | 备注卖花生油 |

	#查询供货商精确查询
	When jobs查询供货商
		"""
		{
			"name": "丹江湖2"
		}
		"""
	Then jobs能获取供货商列表
		"""
		[{
			"name": "丹江湖2",
			"create_at": "今天",
			"responsible_person": "陌陌",
			"remark": ""
		}]
		"""
	When jobs导出'供货商'
	Then jobs能获取导出供货商信息
		|  name   | responsible_person | supplier_tel |   supplier_address   |    remark    |
		| 丹江湖2 |       陌陌         | 13811223344  | 北京市海淀区泰兴大厦 |              |











