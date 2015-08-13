#_author_:王丽

Feature:自定义模块——【基础模块】预览-页面
	1、不用保存，直接预览当前的编辑页面的内容
	2、预览是重新创建一个新页面
	3、预览区显示对应的模块,模块必填文本显示'请添加XXX',显示对应的图片，必填图片区如果没有自定义的图片，用系统图片代替
	4、预览页，手机模拟器不要滚动条

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

Scenario:预览
	When jobs预览当前
	Then jobs在新建页面,预览区显示对应的模块,模块必填文本显示'请添加XXX',显示对应的图片，必填图片区如果没有自定义的图片，用系统图片代替
	Then jobs扫码区'预览二维码'显示
	When jobs完成扫码
	Then jobs在手机端看到预览效果
