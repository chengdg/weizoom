#_author_:王丽

Feature:自定义模块——【基础模块】橱窗-页面
	1、	标题名：最多可输入15个字
   		内容区标题：最多可输入15个字
   		内容区说明：最多输入50个字
   	2、链接，“从微站选择”当选择的链接的名称过长时用省略号截取显示，保证链接名称、修改、图标在同一行，不折行

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

Scenario:(1)橱窗，编辑、删除、字数和控制校验
	#编辑橱窗
		#橱窗的空值校验 jobs设置橱窗标题'空',显示方式'默认',内容标题'空',内容说明'空'
		When jobs添加橱窗
		"""
			[{
				"display_window_title":"",
				"content_title":"",
				"content_explain":""
			}]
		"""
		Then jobs展示区显示默认添加的图片，以'默认'方式展示
		And jobs展示区标题'空',内容标题'空',内容说明'空'

	#橱窗的字数校验  标题'大于15',显示方式'默认',内容标题'大于15',内容说明'大于50'
		When jobs修改橱窗
		"""
			[{
				"display_window_title":"橱窗标题名大于15",
				"display_mode":"默认",
				"content_title":"内容标题大于15",
				"content_explain":"内容说明大于50"

			}]
		"""
		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs编辑区提示错误信息'橱窗标题名不能多于15字'
		And jobs编辑区提示错误信息'内容标题不能多于15字'
		And jobs编辑区提示错误信息'内容说明不能多于50字'

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片，无链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"默认",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50"
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''默认样式''默认图片'显示

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片,有链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"默认",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50"
			"pictrue_link_modle":[{
				"pictrue_link1":"图片链接1"
				}]
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''默认样式''默认图片'显示

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片,链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"3列",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50",
			"value":[{
				"pictrue1":"图片1",
				"pictrue_link1":"图片链接1"
			},{
				"pictrue2":"图片2",
				"pictrue_link2":"图片链接2"
			},{
				"pictrue2":"图片3",
				"pictrue_link2":"图片链接3"
				}]
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''3列''设置图片'显示

	#删除橱窗模块,弹出删除确认提示窗体
		When jobs删除橱窗模块
		Then jobs展示区橱窗模块删除
		And  jobs编辑区对应的编辑窗体关闭

Scenario:橱窗编辑 添加一个图片，其他图片为默认图片
	#编辑橱窗
		When jobs添加橱窗
		"""
			[{
				"display_window_title":"",
				"content_title":"",
				"display_mode":"默认",
				"content_explain":"",
				"value":[{
				"pictrue1":"图片1",
				"pictrue_link1":"图片链接1"
				}
			}]
		"""
		Then jobs展示区显示默认添加的图片，以'默认'方式展示
		"""
			[{
				"value":[{
				"pictrue1":"图片1",
				"pictrue_link1":"图片链接1"
				}
			},{
				"value":[{
				"pictrue1":"默认图片",
				"pictrue_link1":""
				}
			},{
				"value":[{
				"pictrue1":"默认图片",
				"pictrue_link1":""
				}
			}]
		"""

		And jobs展示区标题'空',内容标题'空',内容说明'空'