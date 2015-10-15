#_author_:师帅
#editor 新新 2015.10.13
Feature:自定义模块——【基础模块】橱窗-页面
	"""
	1、	标题名：最多可输入15个字
   		内容区标题：最多可输入15个字
   		内容区说明：最多输入50个字
   	2、链接，“从微站选择”当选择的链接的名称过长时用省略号截取显示，保证链接名称、修改、图标在同一行，不折行
   	"""

@mall2 @termite2 
Scenario:1 新建橱窗微页面
	Given jobs登录系统
	When jobs创建微页面
		"""
		[{
			"title":{
				"name": "微页面标题1"
			},
			"display_window":{
				"index": 1,
				"items": {
				"display_window_title":"",
				"content_title":"",
				"display_mode":"默认",
				"content_explain":"",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"picture_link":"店铺主页"
				}]
			}
		}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"display_window":{
				"index": 1,
				"items": {
				"display_window_title":"",
				"content_title":"",
				"display_mode":"默认",
				"content_explain":"",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"picture_link":"店铺主页"
				}]
			}
		}
		}
		"""
	#将会员主页修改为我的订单
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"display_window":{
				"index": 1,
				"items": {
				"display_window_title":"",
				"content_title":"",
				"display_mode":"3列",
				"content_explain":"",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"picture_link":"我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"picture_link":"店铺主页"
				}]
			}
		}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			},
			"display_window":{
				"index": 1,
				"items": {
				"display_window_title":"",
				"content_title":"",
				"display_mode":"3列",
				"content_explain":"",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"picture_link":"我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"picture_link":"会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"picture_link":"店铺主页"
				}]
			}
		}
		}
		"""
	#删除橱窗
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title":{
				"name": "微页面标题1"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}
		}
		"""