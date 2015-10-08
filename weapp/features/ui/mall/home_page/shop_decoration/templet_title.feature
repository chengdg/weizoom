#_author_:师帅

Feature:自定义模块——【基础模块】标题-页面


Scenario:1 新建微页面
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"templet_title":{
				"title": "标题",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"color": "blue"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			},
			"templet_title":{
				"title": "标题",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"color": "blue"
			}
		}
	"""

Scenario: 2验证，删除
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"templet_title":{
				"title": "",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"color": "blue"
			}
		}]
	"""
	Then jobs提示'标题名不能为空'
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"templet_title":{
				"title": "标题",
				"subtitle": "",
				"time": "",
				"color": "blue"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			},
			"templet_title":{
				"title": "标题",
				"subtitle": "",
				"time": "",
				"color": "blue"
			}
		}
	"""
	When jobs删除'标题'
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""