
#_author_：师帅
#_edit_：benchi
#_edit_：新新
# 利用现有控件，在编辑区内编辑什么样的内容，相应的，在展示区内显示对应的富文本内容（富文本可包括，文件，图片，表格等等,富文本中有默认信息，字数控制在10000字）
Feature: 自定义模块-富文本


Scenario: 添加，编辑富文本
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"multy_text_content": "富文本标题文字,加粗、斜体、下划线、文字颜色、背景色、字号大小、换行显示图片,换行显示3行3列的表格"
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"multy_text_content": "富文本标题文字,加粗、斜体、下划线、文字颜色、背景色、字号大小、换行显示图片,换行显示3行3列的表格"
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"multy_text_content": "富文本标题文字加粗有下划线,换行显示内容描述,换行显示图片,换行显示6行6列的表格"
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"multy_text_content": "富文本标题文字加粗有下划线,换行显示内容描述,换行显示图片,换行显示6行6列的表格"
		}
	"""

