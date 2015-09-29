#author：师帅
Feature: 编辑自定义模块

Background:
	Given jobs登录系统
	And jobs已添加商品
	"""
		[{
			"name": "商品1可单行显示",
			"shelve_type":"上架",
			"price": 1.0
		},{
			"name": "商品2可两行显示",
			"product_picture_id":"2",
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示......",
			"shelve_type":"上架",
			"price": 3.0
		},{
			"name": "商品4",
			"shelve_type":"下架",
			"price": 10.0
		}
		}]	
		"""
	Then jobs获取'在售'商品选择列表

Scenario: 添加模块
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			}, 
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"	
		}]
	"""

	When jobs编辑微页面'微页面标题'
	And jobs添加商品模块
	"""
	[{
		"products":{
			"items": [{
			"product_name":"商品2可两行显示",
			"price":"2.0"
		},{
			"product_name":"商品1可单行显示",
			"price":"1.0"
		},{
			"product_name":"商品3不可两行显示......",
			"price":"3.0"
		}],
		"list_style1":"大图",
		"list_style2":"卡片样式",
		"show_product_name":"ture",
		"show_price":"true"
		}
	}]	
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": "微页面标题"
		}, 
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		"products": {
			"items": [{
				"product_name":"商品2可两行显示",
				"price":"2.0"
				},{
				"product_name":"商品1可单行显示",
				"price":"1.0"
				},{
				"product_name":"商品3不可两行显示...",
				"price":"3.0"
				}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
			}
	}]
	"""

	When jobs编辑微页面'微页面标题'
	And jobs添加图片信息
	"""
		[{
			"picture_navigation": {
				"items": [{
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
			}
		}]

	"""

	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": "微页面列表"
		},
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		"products": {
			"items": [{
				"product_name":"商品2可两行显示",
				"price":"2.0"
				}, {
				"product_name":"商品1可单行显示",
				"price":"1.0"
				}, {
				"product_name":"商品3不可两行显示...",
				"price":"3.0"
				}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		},
		"picture_navigation": {
				"items": [{
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
			}
		}]
	"""

#拖拽调整模块顺序
	When jobs编辑微页面'微页面标题'
	Then jobs能获取'微页面标题'
	"""
	[{
		"title": {
			"name": "微页面列表"
		},
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		"products": {
			"items": [{
				"product_name":"商品2可两行显示",
				"price":"2.0"
				}, {
				"product_name":"商品1可单行显示",
				"price":"1.0"
				}, {
				"product_name":"商品3不可两行显示...",
				"price":"3.0"
			}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		},
		"picture_navigation": {
				"items": [{
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
			}
		}]
	"""

#删除后不留空白区，下一个模块自动顶替被删除的模块
	When jobs编辑微页面'微页面标题'
	And jobs删除'富文本'
	Then jobs能获取'微页面标题'
	"""
	[{
		"title":{
			"name": "微页面标题"
		},
		"picture_navigation": {
				"items": [{
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
			},
		"products": {
			"items": [{
				"product_name":"商品2可两行显示",
				"price":"2.0"
				}, {
				"product_name":"商品1可单行显示",
				"price":"1.0"
				}, {
				"product_name":"商品3不可两行显示...",
				"price":"3.0",
			}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		}
	}]
	"""

	When jobs编辑微页面'微页面标题'
	And jobs添加'富文本'
	"""
		[{
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title":{
			"name": "微页面标题"
		},
		"picture_navigation": {
				"items": [{
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
			},
		"products": {
			"items": [{
				"product_name":"商品2可两行显示",
				"price":"2.0"
				}, {
				"product_name":"商品1可单行显示",
				"price":"1.0"
				}, {
				"product_name":"商品3不可两行显示...",
				"price":"3.0"
			}],
			"list_style1":"大图",
			"list_style2":"卡片样式",
			"show_product_name":"ture",
			"show_price":"true"
		},
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
	}]
	"""

	When jobs编辑微页面'微页面标题'
	And jobs删除'商品'
	Then jobs能获取'微页面标题'
	"""
	[{
		"title":{
			"name": "微页面标题"
		},
		"picture_navigation": {
				"items": [{
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
			},
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
	}]
	"""

	When jobs编辑微页面'微页面标题'
	And jobs修改'标题4'
	"""
		[{
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
	[{
		"title":{
			"name": "微页面标题"
		},
		"picture_navigation": {
				"items": [{
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
			},
		"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
	}]
	"""

