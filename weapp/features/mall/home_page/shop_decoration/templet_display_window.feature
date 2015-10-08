#_author_:王丽

Feature:自定义模块——【基础模块】橱窗-页面
	1、	标题名：最多可输入15个字
   		内容区标题：最多可输入15个字
   		内容区说明：最多输入50个字
   	2、链接，“从微站选择”当选择的链接的名称过长时用省略号截取显示，保证链接名称、修改、图标在同一行，不折行





Scenario:1 新建橱窗微页面
		When jobs登录系统
		And jobs创建微页面
		"""
			[{
				"title":{
					"name": "微页面标题"
				},
				"display_window":{
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"会员主页"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
					}
			}]
		"""
		Then jobs能获取'微页面标题'
		"""
			{
				"title": {
					"name": "微页面标题"
				},
				"display_window": {
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"会员主页"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
				}
			}
		"""

Scenario: 2编辑，删除
	When jobs登录系统
	And jobs创建微页面
		"""
			[{
				"title":{
					"name": "微页面标题"
				},
				"display_window":{
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"会员主页"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
					}
			}]
		"""
		Then jobs能获取'微页面标题'
		"""
			{
				"title": {
					"name": "微页面标题"
				},
				"display_window": {
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"会员主页"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
				}
			}
		"""
		When jobs编辑微页面'微页面标题'
		"""
			[{
				"title":{
					"name": "微页面标题"
				},
				"display_window":{
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"微页面"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
					}
			}]
		"""
		Then jobs能获取'微页面标题'
		"""
			{
				"title":{
					"name": "微页面标题"
				},
				"display_window":{
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"微页面"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
					}
			}
		"""
#删除橱窗
		When jobs编辑微页面'微页面标题'
		"""
			[{
				"title":{
					"name": "微页面标题"
				},
				"display_window":{
					"items":[{
						"display_window_title":"",
						"content_title":"",
						"display_mode":"默认",
						"content_explain":"",
						"value":[{
							"pictrue1":"图片1",
							"pictrue_link1":"微页面"
							},{
							"picture2":"图片2",
							"picture_link2":"会员主页"
							},{
							"picture3":"图片3",
							"picture_link2":"店铺主页"
							}]
						}]
					}
			}]
		"""
		Then jobs能获取'微页面标题'
		"""
			{
				"title": {
					"name": "微页面标题"
				}
			}
		"""
