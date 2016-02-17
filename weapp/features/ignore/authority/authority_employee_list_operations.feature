#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2015.12.08

Feature:权限管理-员工管理-列表操作
	"""
		不同状态对应的操作列信息不同
			'启用'状态下显示【停用】|【员工信息】
			'停用'状态下显示【启用】|【删除】|【员工信息】
		员工列表：按照员工创建时间正序排列，每页最多显示10条数据
	"""

Background:
	Given jobs登录系统
	When jobs新建角色
		"""
		[{
			"name":"角色1"
		},{
			"name":"角色2"
		},{
			"name":"角色3"
		}]
		"""
	When jobs新建部门
		"""
		[{
			"name":"部门1"
		},{
			"name":"部门2"
		}]
		"""
	When jobs新建员工
		"""
		[{
			"info":
				[{
					"account_name":"ceshi01",
					"password":"123456a",
					"confirm_password":"123456a",
					"employee_name":"张01",
					"department_name":"部门1"
				}],
			"roles":
				[{
					"role_name":"角色1",
					"is_selected":"N"
				},{
					"role_name":"角色2",
					"is_selected":"N"
				},{
					"role_name":"角色3",
					"is_selected":"N"
				}],
			"permissions":""
		},{
			"info":
				[{
					"account_name":"ceshi02",
					"password":"123456a",
					"confirm_password":"123456a",
					"employee_name":"张02",
					"department_name":"部门2"
				}],
			"roles":
				[{
					"role_name":"角色1",
					"is_selected":"Y"
				},{
					"role_name":"角色2",
					"is_selected":"N"
				},{
					"role_name":"角色3",
					"is_selected":"N"
				}],
			"permissions":""
		},{
			"info":
				[{
					"account_name":"ceshi03",
					"password":"123456a",
					"confirm_password":"123456a",
					"employee_name":"张03",
					"department_name":"部门1"
				}],
			"roles":
				[{
					"role_name":"角色1",
					"is_selected":"Y"
				},{
					"role_name":"角色2",
					"is_selected":"Y"
				},{
					"role_name":"角色3",
					"is_selected":"N"
				}],
			"permissions":""
		}]
		"""

@authority @employee
Scenario:1 停用子账号
	Given jobs登录系统
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门1"
			"roles":"角色1及其他",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"department_name":"部门2"
			"roles":"角色1",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"department_name":"部门1"
			"roles":"",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""
	When jobs停用账户'ceshi03'
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"status":"停用",
			"actions":["启用","删除","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

@authority @employee
Scenario:2 启用子账号
	Given jobs登录系统
	When jobs停用账户'ceshi03'
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"status":"停用",
			"actions":["启用","删除","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""
	When jobs启用账户'ceshi03'
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

@authority @employee
Scenario:3 删除子账号
	Given jobs登录系统
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门1"
			"roles":"角色1及其他",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"department_name":"部门2"
			"roles":"角色1",
			"status":"启用",
			"actions":["停用","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"department_name":"部门1"
			"roles":"",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""
	When jobs停用账户'ceshi03'
	When jobs停用账户'ceshi02'
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门1"
			"roles":"角色1及其他",
			"status":"停用",
			"actions":["启用","删除","员工信息"]
		},{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"department_name":"部门2"
			"roles":"角色1",
			"status":"停用",
			"actions":["启用","删除","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"department_name":"部门1"
			"roles":"",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""
	When jobs删除账户'ceshi02'
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门1"
			"roles":"角色1及其他",
			"status":"停用",
			"actions":["启用","删除","员工信息"]
		},{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"department_name":"部门1"
			"roles":"",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

@authority @employee
Scenario:4 员工管理列表的分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	#Then jobs获得员工管理列表共'3'页
	#When jobs访问员工管理列表第'1'页
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门1"
			"roles":"角色1及其他",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

	When jobs访问员工管理列表下一页
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"department_name":"部门2"
			"roles":"角色1",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

	When jobs访问员工管理列表第'3'页
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi01",
			"employee_name":"张01",
			"department_name":"部门1"
			"roles":"",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

	When jobs访问员工管理列表上一页
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi02",
			"employee_name":"张02",
			"department_name":"部门2"
			"roles":"角色1",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""