#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2015.12.08

Feature:权限管理-员工管理

@authority @employee
Scenario:1 新建部门
	Given jobs登录系统
	When jobs新建部门
		"""
		[{
			"name":"部门1"
		}]
		"""
	Then jobs获得部门'部门1'
		"""
		[{
			"name":"部门1",
			"employees":""
		}]
		"""
	And jobs获得部门列表
		"""
		[{
			"name":"部门1"
		}]
		"""

@authority @employee
Scenario:2 重命名部门
	Given jobs登录系统
	When jobs新建部门
		"""
		[{
			"name":"部门1"
		},{
			"name":"部门2"
		}]
		"""
	Then jobs获得部门列表
		"""
		[{
			"name":"部门2"
		},{
			"name":"部门1"
		}]
		"""
	When jobs重命名部门'部门2'
		"""
		[{
			"name":"部门02"
		}]
		"""
	Then jobs获得部门列表
		"""
		[{
			"name":"部门02"
		},{
			"name":"部门1"
		}]
		"""

@authority @employee
Scenario:3 删除部门
	Given jobs登录系统
	When jobs新建部门
		"""
		[{
			"name":"部门1"
		},{
			"name":"部门2"
		}]
		"""
	Then jobs获得部门列表
		"""
		[{
			"name":"部门2"
		},{
			"name":"部门1"
		}]
		"""
	#删除员工为空的部门
		When jobs删除部门'部门2'
		Then jobs获得部门列表
			"""
			[{
				"name":"部门1"
			}]
			"""

	#删除员工非空的部门
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
			}]
			"""
		When jobs删除部门'部门1'
		Then jobs获得错误提示'请将部门内所有员工删除后再删除部门'

	#将部门内所有员工删除后，部门可以进行删除
		When jobs停用账户'ceshi01'
		When jobs删除账户'ceshi01'
		Then jobs获得员工管理列表
			"""
			[]
			"""
		When jobs删除部门'部门1'
		Then jobs获得部门列表
			"""
			[]
			"""