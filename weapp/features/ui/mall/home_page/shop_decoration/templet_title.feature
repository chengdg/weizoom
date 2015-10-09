#_author_:师帅

Feature:自定义模块——【基础模块】标题-页面

<<<<<<< Updated upstream
=======

Scenario: 1编辑标题
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"templet_title":{
				"title": "标题",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"background_color": "#0000ff"
			}
		}]
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"templet_title":{
				"title": "标题",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"background_color": "#0000ff"
			}
		}
	"""
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"templet_title":{
				"title": "标题1111",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"background_color": "#ff0000"
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"templet_title":{
				"title": "标题1111",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"background_color": "#ff0000"
			}
		}
	"""
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
	"""
@ui
Scenario:(1)标题模块,编辑、删除、字数和控制校验
>>>>>>> Stashed changes

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
