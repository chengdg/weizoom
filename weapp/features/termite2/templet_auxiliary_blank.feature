#author：师帅
Feature: 自定义模块-辅助空白

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

#默认每次调节辅助线最小为1px
Scenario: 辅助空白
	When jobs将辅助线调到最低的30px
	Then jobs展示区显示30px的空白高度
	When jobs将辅助线调到最高的100px
	Then jobs展示区显示100px的空白高度
	When jobs每次调整辅助线1px
	Then jobs展示区相应空白高度变化1px
	