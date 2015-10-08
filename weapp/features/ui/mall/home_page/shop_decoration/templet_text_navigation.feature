#_author_:师帅
Feature:自定义模块——【基础模块】文本导航-页面


Scenario:1添加文本导航
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": "会员中心"
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": "会员中心"
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""


Scenario: 2文本导航模块，编辑、删除、字数校验
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "",
					"navigation_link": "会员中心"
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""
	Then jobs提示'导航名称不能为空'
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": ""
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""
	Then jobs提示'链接地址不能为空'
	When jobs删除'文本导航'
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}
	"""

Scenario: 3删除模块
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": ""
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": ""
				},{
					"navigation_name": "文本导航1",
					"navigation_link": "店铺主页"
				}]
			}
		}
	"""
	When jobs删除'文本导航'
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""

