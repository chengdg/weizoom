#_author_:王丽
#_edit_:benchi
#_edit_:新新

Feature:自定义模块——【基础模块】标题-页面
        显示位置：居左、居中、居右，
        根据字数不同，副标题与时间的显示位置也不同



Scenario: 1编辑标题
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title": {
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
			"title": {
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
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"templet_title":{
				"title": "标题1111",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"color": "red"
			}
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"templet_title":{
				"title": "标题1111",
				"subtitle": "副标题",
				"time": "2015-5-13 10:13",
				"color": "red"
			}
		}
	"""
