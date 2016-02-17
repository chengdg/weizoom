#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2015.12.08

Feature:权限管理-员工管理-新建员工
	"""
		1、新建员工页面：
			【新建员工】
				账户名称：必填字段，
					输入框后有红字提示信息-注：账户名一旦注册不能更改，4-20位字符，可使用汉字、字母或数字的组合，不建议使用纯数字。
				密码:必填字段，输入框后有红字提示信息-注：6-20位字符，可使用字母、数字或符号的组合，不建议使用单一类型。
				确认密码：必填字段
				员工姓名：必填字段
				部门：必填字段，下拉框列表形式显示，默认显示‘选择部门’，按照部门的创建时间正序显示

			【角色】：复选框形式显示角色信息，按照角色创建时间正序显示

			【权限】：默认显示"此员工未设置权限"，【角色】区域若勾选了某个角色，则显示该角色的权限设置信息

		2、保存成功后，返回到列表页面，左侧默认选中该员工所属的部门，右侧列表按照员工的创建时间正序显示，每页显示10条数据

		3、员工列表字段：
			账户名称:显示该员工的账户名称
			姓名：显示员工姓名
			部门：显示员工所属部门
			角色：显示员工具有的角色，当有多个角色时显示xx及其他
			状态：默认为"启用"
			操作：不同状态对应的操作列信息不同
				'启用'状态下显示【停用】|【员工信息】
				'停用'状态下显示【启用】|【删除】|【员工信息】
		4、每次点击'员工管理'进入其页面时：
			分页显示所有部门的所有员工信息，
			左侧部门列表不选中任何一个部门，
			右侧员工列表按照创建时间正序显示
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
	When jobs给角色'角色3'添加权限
		"""
		[{
			"name":"角色3",
			"roles_permission":
				[{
					"module_name":"首页",
					"values":
					[{
						"value":"统计概况"
					},{
						"value":"积分规则"
					}]
				},{
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

@authority @employee
Scenario:1 新建员工,角色为空
	Given jobs登录系统
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

@authority @employee
Scenario:2 新建员工,单个角色,角色权限为空
	Given jobs登录系统
	When jobs新建员工
		"""
		[{
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
		}]
		"""
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

@authority @employee
Scenario:3 新建员工,单个角色,角色权限非空
	Given jobs登录系统
	When jobs新建员工
		"""
		[{
			"info":
				[{
					"account_name":"ceshi03",
					"password":"123456a",
					"confirm_password":"123456a",
					"employee_name":"张03",
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
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi03",
			"employee_name":"张03",
			"department_name":"部门2"
			"roles":"角色2",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""

@authority @employee
Scenario:4 新建员工,多个角色
	Given jobs登录系统
	When jobs新建员工
		"""
		[{
			"info":
				[{
					"account_name":"ceshi04",
					"password":"123456a",
					"confirm_password":"123456a",
					"employee_name":"张04",
					"department_name":"部门2"
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
			"permissions":[{
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
	Then jobs获得员工管理列表
		"""
		[{
			"account_name":"ceshi04",
			"employee_name":"张04",
			"department_name":"部门2"
			"roles":"角色1及其他",
			"status":"启用",
			"actions":["停用","员工信息"]
		}]
		"""