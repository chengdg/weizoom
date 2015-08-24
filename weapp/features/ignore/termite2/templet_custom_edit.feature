#author：师帅
Feature: 编辑自定义模块

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
	And jobs已添加商品
	"""
		[{
			"name": "商品1可单行显示",
			"product_picture_id":"1",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"product_picture_id":"2",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示......",
			"product_picture_id":"3",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"product_picture_id":"4",
			"shelve_type":"下架",
			"price": 10.0
		}
		}]	
		"""
	Then jobs展示区显示蓝色边框添加新模块

Scenario: 添加模块
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

	When jobs添加商品模块
	"""
	[{
		"products":[
		{
			"product_name":"商品2可两行显示",
			"product_picture_id":"2",
			"price":"2.0"
		},{
			"product_name":"商品1可单行显示",
			"product_picture_id":"1",
			"price":"1.0"
		},{
			"product_name":"商品3不可两行显示......",
			"product_picture_id":"3",
			"price":"3.0"
		}],
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	}]
	"""
	Then jobs展示区大图单列显示商品
	"""
	[{
		"product_name":"商品2可两行显示",
		"product_picture_id":"2",
		"price":"2.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品1可单行显示",
		"product_picture_id":"1",
		"price":"1.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品3不可两行显示...",
		"product_picture_id":"3",
		"price":"3.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	}]
	"""

	When jobs添加图片导航模块
	And jobs添加图片信息
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}] 
	"""

	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""

#拖拽调整模块顺序
	When jobs拖拽'图片导航'模块放置'商品'模块上
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""
	Then jobs展示区大图单列显示商品
	"""
	[{
		"product_name":"商品2可两行显示",
		"product_picture_id":"2",
		"price":"2.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品1可单行显示",
		"product_picture_id":"1",
		"price":"1.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品3不可两行显示...",
		"product_picture_id":"3",
		"price":"3.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	}]
	"""

#删除后不留空白区，下一个模块自动顶替被删除的模块
	When jobs删除'富文本'
	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""
	Then jobs展示区大图单列显示商品
	"""
	[{
		"product_name":"商品2可两行显示",
		"product_picture_id":"2",
		"price":"2.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品1可单行显示",
		"product_picture_id":"1",
		"price":"1.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品3不可两行显示...",
		"product_picture_id":"3",
		"price":"3.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	}]
	"""

	When jobs添加'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""
	Then jobs展示区大图单列显示商品
	"""
	[{
		"product_name":"商品2可两行显示",
		"product_picture_id":"2",
		"price":"2.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品1可单行显示",
		"product_picture_id":"1",
		"price":"1.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	},{
		"product_name":"商品3不可两行显示...",
		"product_picture_id":"3",
		"price":"3.0",
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
	}]
	"""
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""

	When jobs删除'商品'
	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""

	When jobs编辑'图片导航-4'
	"""
		[{
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}]
	"""
	Then jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2", 
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}]
	"""
	Then jobs展示区显示'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""

