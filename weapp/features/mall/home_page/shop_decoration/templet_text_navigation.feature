#_author_:王丽
#_edit_:新新

Feature:自定义模块——【基础模块】文本导航-页面
	1、文本导航模块新建时，默认有一个文本导航
	2、‘导航名称’和‘链接到’都是必填的
	3、文本导航的‘导航名称’字数不能超过30字
	4、文本导航的‘导航名称’，自适应，可单行显示的单行显示，不可单行显示的用‘...’的方式单行显示
	5、新添加的文本导航，默认在最后一个，可以无限添加文本导航
	6、文本导航可以删除，最后必须保留一个，当只有一个文本导航的时候，该文本导航不能删除
	7、文本导航的链接，“从微站选择”当选择的链接的名称过长时用省略号截取显示，保证链接名称、修改、图标在同一行，不折行

Scenario:1添加文本导航
	Given jobs登录系统
	When jobs创建微页面
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
		{
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
		}
	"""

Scenario: 2编辑文本导航
	Given jobs登录系统
	When jobs创建微页面
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
		{
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
		}
	"""
	When jobs编辑微页面'微页面标题'
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
					"navigation_name": "文本导航2",
					"navigation_link": "店铺主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航",
					"navigation_link": "会员中心"
				},{
					"navigation_name": "文本导航2",
					"navigation_link": "微页面"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航2",
					"navigation_link": "微页面"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"navigation":{
				"values":[{
					"navigation_name": "文本导航2",
					"navigation_link": "微页面"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			}
		}
	"""

