#author：师帅
Feature: 微页面-新建微页面

Background:
	Given jobs登录系统
	And jobs已添加模块
		"""
		[	
			{"model_name": "富文本"},
			{"model_name": "商品"},
			{"model_name": "商品列表"},
			{"model_name": "图片广告"},
			{"model_name": "公告"},
			{"model_name": "标题"},
			{"model_name": "文本导航"},
			{"model_name": "图片导航"},
			{"model_name": "辅助空白"},
			{"model_name": "橱窗"}
		]
		"""

Scenario:1新建微页面
	When jobs登录系统
	And jobs新建微页面
	Then jobs进入编辑页面
	And jobs编辑区显示模块
	"""
		[	
			{"model_name": "富文本"},
			{"model_name": "商品"},
			{"model_name": "商品列表"},
			{"model_name": "图片广告"},
			{"model_name": "公告"},
			{"model_name": "标题"},
			{"model_name": "文本导航"},
			{"model_name": "图片导航"},
			{"model_name": "辅助空白"},
			{"model_name": "橱窗"}
		]
		"""
