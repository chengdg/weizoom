#author：师帅
Feature: 编辑自定义模块-添加

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
			"shelve_type":"上架",
			"price": 2.0
		},{
			"name": "商品3不可两行显示",
			"shelve_type":"上架",
			"price": 3.0
		}]
		"""

@termite21
Scenario: 添加模块
	When jobs创建微页面
		"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"	
		}
		"""

	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
			"products": {
				"items": [{
					"name":"商品2可两行显示",
					"price":"2.0"
				}, {
					"name":"商品1可单行显示",
					"price":"1.0"
				}, {
					"name":"商品3不可两行显示",
					"price":"3.0"
				}],
				"list_style1": "大图",
				"list_style2": "默认样式",
				"show_product_name": "true",
				"show_price": "true"
			}
		}
		"""

	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			}, 
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
			"products": {
				"items": [{
					"name":"商品2可两行显示",
					"price":"2.0"
				}, {
					"name":"商品1可单行显示",
					"price":"1.0"
				}, {
					"name":"商品3不可两行显示",
					"price":"3.0"
				}],
				"list_style1": "大图",
				"list_style2": "默认样式",
				"show_product_name": "true",
				"show_price": "true"
			}
		}
		"""

	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
			"products": {
				"items": [{
					"name":"商品2可两行显示",
					"price":"2.0"
				}, {
					"name":"商品1可单行显示",
					"price":"1.0"
				}, {
					"name":"商品3不可两行显示",
					"price":"3.0"
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			},
			"picture_ids":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				}, {
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}, {
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题4",
					"link": "会员主页"
			}]
		}
		"""

	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
			"products": {
				"items": [{
					"name":"商品2可两行显示",
					"price":"2.0"
				}, {
					"name":"商品1可单行显示",
					"price":"1.0"
				}, {
					"name":"商品3不可两行显示",
					"price":"3.0"
				}],
				"list_style1":"大图",
				"list_style2":"默认样式",
				"show_product_name":"true",
				"show_price":"true"
			},
			"picture_ids":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				}, {
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}, {
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题4",
					"link": "会员主页"
			}]
		}
		"""
