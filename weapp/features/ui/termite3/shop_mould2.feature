#author：师帅
Feature: 微页面-店铺模板1

Background:
	Given jobs登录系统
	And jobs已添加店铺头信息
	"""
		[{
			"background_pictrue": "picture1",
			"name": "店铺名称"
		}]
	"""
	And jobs已添加图片广告信息
	"""
		[{
			"display_mode": "轮播图",
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"display_mode": "轮播图",
			"picture_id": "2",
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"display_mode": "轮播图",
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}]
	"""
	And jobs已添加文本导航信息
	"""
		[{
			"navigation_name":"导航",
			"navigation_link":"导航链接"
		}]
	"""
	And jobs已添加商品信息
	"""
		[{
			"name":"商品4",
			"price":"3.0",
			"list_style1":"小图",
			"list_style2":"简洁样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"price":"1.0",
			"list_style1":"小图",
			"list_style2":"简洁样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"price":"2.0",
			"list_style1":"小图",
			"list_style2":"简洁样式",
			"show_product_name":"ture",
			"show_price":"true"
		}, {
			"name":"商品7",
			"price":"2.0",
			"list_style1":"小图",
			"list_style2":"简洁样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
	"""
	And jobs已添加文本导航信息
	"""
		[{
			"navigation_name":"导航名称",
			"navigation_link":"店铺主页"
		}]
	"""
	And jobs已添加橱窗信息
	"""
		[{
			"display_window_title":"橱窗",
			"content_title":"11",
			"display_mode":"默认",
			"content_explain":"11",
			"value":
			[{
				"pictrue1":"图片1",
				"pictrue_link1":"图片链接1"
			}, {
				"pictrue1":"图片2",
				"pictrue_link1":"图片链接2"
			}, {
				"pictrue1":"图片3",
				"pictrue_link1":"图片链接3"
			}
		}]
	"""
	And jobs已添加商品信息
	"""
		[{
			"name":"商品4",
			"price":"3.0",
			"list_style1":"小图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品5",
			"price":"1.0",
			"list_style1":"小图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		},{
			"name":"商品6",
			"price":"2.0",
			"list_style1":"小图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}, {
			"name":"商品7",
			"price":"2.0",
			"list_style1":"小图",
			"list_style2":"默认样式",
			"show_product_name":"ture",
			"show_price":"true"
		}]
	"""
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


#对模块进行添加，修改，删除操作
Scenario:1对模块进行添加，修改，删除操作
#jobs进来后在展示区显示已添加好的信息
#添加新模块
	When jobs添加新模块
	Then jobs编辑区显示
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
	When jobs在'文本导航'后添加'公告'
	"""
		[{
			"notice_text": "自定义模块公告单屏可显示"
		}]
	"""
	Then jobs在展示区按照添加顺序显示

#修改模块
	When jobs修改'文本导航'信息
	"""
		[{
			"navigation_name":"导航名称1111",
			"navigation_link":"个人中心"
		}]
	"""
	Then jobs展示区显示修改后的信息

#删除
	When jobs删除'文本导航'信息
	Then jobs弹出提示信息
	And jobs展示区显示删除'文本导航'后的信息

