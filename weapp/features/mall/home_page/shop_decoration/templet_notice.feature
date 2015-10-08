#_author_:王丽
#_edit_:benchi
#_edit_:新新
#_edit_:师帅
Feature:自定义模块——【基础模块】公告-页面


Scenario:添加公告
	Given jobs登录系统
	When jobs创建微页面
	"""
	[{
		"title": {
			"name": "微页面标题"
		},
		"notice_text": "自定义模块公告单屏可显示"
	}]
	"""
	Then jobs能获取'微页面标题'
	"""
	{
		"title": {
			"name": "微页面标题"
		},
		"notice_text": "自定义模块公告单屏可显示"
	}
	"""


#公告为空
	When jobs编辑微页面'微页面标题'
	"""
	[{
		"title": {
			"name": "微页面标题"
		},
		"notice_text":""
	}]
	"""
	Then jobs能获取'微页面标题'
	"""
	{
		"title": {
			"name": "微页面标题"
		},
		"notice_text":"默认显示公告，请填写内容，如果过长，将会在手机上滚动显示"
	}
	"""
#删除公告
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"notice_text":""
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""