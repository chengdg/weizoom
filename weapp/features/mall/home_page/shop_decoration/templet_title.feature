#_author_:王丽
#_edit_:benchi
#_edit_:新新

Feature:自定义模块——【基础模块】标题-页面
        显示位置：居左、居中、居右，
        根据字数不同，副标题与时间的显示位置也不同

@wepage
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
