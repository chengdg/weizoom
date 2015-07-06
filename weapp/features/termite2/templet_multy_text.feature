
#_author_：师帅
#_edit_：benchi
# 利用现有控件，在编辑区内编辑什么样的内容，相应的，在展示区内显示对应的富文本内容（富文本可包括，文件，图片，表格等等,富文本中有默认信息，字数控制在10000字）
Feature: 自定义模块-富文本

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
Scenario: 添加，编辑富文本
	When jobs添加富文本
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	When jobs编辑富文本
	"""
		[{
			"multy_text_content": "富文本标题文字加粗有下划线，换行显示内容描述，换行显示图片，换行显示6行6列的表格"
		}]
	"""
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字加粗有下划线，换行显示内容描述，换行显示图片，换行显示6行6列的表格"
		}]
	"""

