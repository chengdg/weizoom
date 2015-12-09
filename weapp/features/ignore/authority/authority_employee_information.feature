#_author_:张三香 2015.12.09

Feature:权限管理-员工管理-员工信息
	"""
	点击操作列的【员工信息】，进入员工信息页面：
		1、可以对员工姓名、部门、角色进行修改
		2、点击【修改密码】，可以进行密码修改
		3、点击【补充权限】，可以对权限信息进行修改
		4、【补充权限】：可为账号赋予超出已选角色范围以外的权限；补充权限时不可删减该员工已经获得角色涵盖的权限；当角色和补充权限存在交集时，只添加一次相应的权限。
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
	When jobs给角色'角色2'添加权限
		"""
		[{
			"name":"角色2",
			"roles_permission":
				[{
					"module_name":"微信",
					"values":
					[{
						"value":"统计概况"
					},{
						"value":"积分规则"
					}]
				}]
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
		}]
		"""

@authority @employee
Scenario:1 查看员工信息
	Given jobs登录系统
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
	#When jobs查看账户'ceshi01'的员工信息
	Then jobs获得账户'ceshi01'的员工信息
		"""
		[{
			"info":
				[{
					"account_name":"ceshi01",
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

@authority @employee
Scenario:2 修改员工信息
	Given jobs登录系统
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
	#When jobs查看账户'ceshi01'的员工信息
	When jobs修改账户'ceshi01'的员工信息
		"""
		[{
			"info":
				[{
					"account_name":"ceshi01",
					"employee_name":"张001",
					"department_name":"部门2"
				}],
			"roles":
				[{
					"role_name":"角色1",
					"is_selected":"N"
				},{
					"role_name":"角色2",
					"is_selected":"Y"
				},{
					"role_name":"角色3",
					"is_selected":"N"
				}],
			"add_permission":[{
					"module_name":"订单",
					"values":
					[{
						"value":"所有订单"
					},{
						"value":"订单设置"
					}]
				}]
		}]
		"""
	Then jobs获得账户'ceshi01'的员工信息
		"""
		[{
			"info":
				[{
					"account_name":"ceshi01",
					"employee_name":"张001",
					"department_name":"部门2"
				}],
			"roles":
				[{
					"role_name":"角色1",
					"is_selected":"N"
				},{
					"role_name":"角色2",
					"is_selected":"Y"
				},{
					"role_name":"角色3",
					"is_selected":"N"
				}],
			"permissions":[{
				"roles_permission":
					[{
						"module_name":"微信",
						"values":
						[{
							"value":"统计概况"
						},{
							"value":"积分规则"
						}]
					}],
				"add_permission":
					[{
						"module_name":"订单",
						"values":
						[{
							"value":"所有订单"
						},{
							"value":"订单设置"
						}]
					}]
				}]
		}]
		"""
	And jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi01",
			"employee_name":"张001",
			"department_name":"部门2"
			"roles":"角色2",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

