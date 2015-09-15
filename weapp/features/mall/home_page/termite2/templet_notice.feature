#_author_:王丽
#_edit_:benchi
#_edit_:新新

Feature:自定义模块——【基础模块】公告-页面

Background:
	Given jobs登录系统
	And jobs已添加模块
		"""
		[	
			{"modle_name": "富文本"},
			{"modle_name": "商品"},
			{"modle_name": "商品列表"},
			{"modle_name": "图片广告"},
			{"modle_name": "公告"},
			{"modle_name": "标题"},
			{"modle_name": "文本导航"},
			{"modle_name": "图片导航"},
			{"modle_name": "辅助空白"},
			{"modle_name": "橱窗"}
		]
	
		"""
	
#单屏可以显示公告
Scenario:添加公告
	When jobs添加公告'单屏可显示'
	"""
	[{
		"notice_text": "自定义模块公告单屏可显示"
	}]
	"""
	Then jobs展示区'不滚动'显示'公告'
	"""
	[{
		"notice_text": "自定义模块公告单屏可显示"
	}]
	"""
	And jobs背景色'黄色'

#单屏不能显示公告
	When jobs修改公告'单屏不可显示'
	"""
	[{
		"notice_text":"自定义模块公告单屏不可显示"
	}]
	"""
	Then jobs展示区'滚动'显示'公告'
	"""
	[{
		"notice_text":"自定义模块公告单屏不可显示"
	}]
	"""

#公告为空
	When jobs修改公告'空'
	"""
	[{
		"notice_text":""
	}]
	"""
	Then jobs展示区'不滚动'显示'公告'
	"""
	[{
		"notice_text":"默认显示公告，请填写内容，如果过长，将会在手机上滚动显示"
	}]
	"""

#删除公告

	When jobs删除公告'单屏可显示'
	Then jobs展示区弹出提示信息
	And jobs展示区当前公告删除,焦点消失
	And  jobs编辑区对应的编辑窗体关闭