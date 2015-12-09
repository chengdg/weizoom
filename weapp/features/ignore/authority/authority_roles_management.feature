#_author_:张三香 2015.12.08

Feature:权限管理-角色管理
	1.点击“+新建”创建角色，下方新增可编辑文本框，里面文字为“新角色”
	2.角色新建成功后，权限设置默认为空，按钮显示【添加权限】
	3.角色的权限设置为空时，按钮显示【添加权限】，权限设置非空时，按钮显示【修改权限】
	4.角色名称不能为空
	5.角色名称不允许重复
	6.角色上限数为30

@authority @role
Scenario:1 新建角色
	Given jobs登录系统
	When jobs新建角色
		"""
		[{
			"name":"角色1"
		}]
		"""
	Then jobs能获得角色'角色1'
		"""
		[{
			"name":"角色1",
			"roles_permission":""
		}]
		"""
	And jobs获得角色列表
		"""
		[{
			"name":"角色1"
		}]
		"""

@authority @role
Scenario:2 重命名角色
	Given jobs登录系统
	When jobs新建角色
		"""
		[{
			"name":"角色2"
		}]
		"""
	Then jobs获得角色列表
		"""
		[{
			"name":"角色2"
		}]
		"""
	When jobs重命名角色'角色2'
		"""
		{
			"name":"角色02"
		}
		"""
	Then jobs获得角色列表
		"""
		[{
			"name":"角色02"
		}]
		"""

@authority @role
Scenario:3 角色的权限设置
	Given jobs登录系统
	When jobs新建角色
		"""
		[{
			"name":"角色3"
		}]
		"""
	#给角色"添加权限"
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
		Then jobs能获得角色'角色3'
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

	#给角色"修改权限"-使角色权限非空
		When jobs给角色'角色3'修改权限
			"""
			[{
				"name":"角色3",
				"roles_permission":
				[{
					"module_name":"首页",
					"values":
					[{
						"value":"统计概况"
					}]
				},{
					"module_name":"商品",
					"values":
					[{
						"value":"在售商品管理"
					},{
						"value":"添加新商品"
					}]
				}]
			}]
			"""
		Then jobs能获得角色'角色3'
			"""
			[{
				"name":"角色3",
				"roles_permission":
				[{
					"module_name":"首页",
					"values":
					[{
						"value":"统计概况"
					}]
				},{
					"module_name":"商品",
					"values":
					[{
						"value":"在售商品管理"
					},{
						"value":"添加新商品"
					}]
				}]
			}]
			"""

	#给角色"修改权限"-使角色权限为空
		When jobs给角色'角色3'修改权限
			"""
			[{
				"name":"角色3",
				"roles_permission":""
			}]
			"""
		Then jobs能获得角色'角色3'
			"""
			[{
				"name":"角色3",
				"roles_permission":""
			}]
			"""

@authority @role
Scenario:4 删除角色
	Given jobs登录系统
	When jobs新建角色
		"""
		[{
			"name":"角色01"
		},{
			"name":"角色02"
		},{
			"name":"角色03"
		}]
		"""
	Then jobs获得角色列表
		"""
		[{
			"name":"角色03"
		},{
			"name":"角色02"
		},{
			"name":"角色01"
		}]
		"""
	When jobs给角色'角色02'添加权限
		"""
		[{
			"name":"角色02",
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

	#删除权限设置为空的角色
		When jobs删除角色'角色03'
		Then jobs获得角色列表
			"""
			[{
				"name":"角色02"
			},{
				"name":"角色01"
			}]
			"""
	#删除权限设置非空的角色
		When jobs删除角色'角色02'
		Then jobs获得角色列表
			"""
			[{
				"name":"角色01"
			}]
			"""
