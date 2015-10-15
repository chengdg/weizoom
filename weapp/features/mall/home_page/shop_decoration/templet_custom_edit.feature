#author：师帅
Feature: 编辑自定义模块-编辑

@termite21
Scenario:1编辑自定义模块
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
			"picture_ids":[{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg",
				"title": "标题1",
				"link": "店铺主页"
			}, {
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
		}]
		"""

	#拖拽调整模块顺序
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
			}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"	
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
			}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"	
		}
		"""
	#修改标题4
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				"title": "标题4321",
				"link": "我的订单"
			}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				"title": "标题4321",
				"link": "我的订单"
			}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}
		"""

@termite2
Scenario:2 编辑自定义模块-删除
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
		},{
			"name": "商品4",
			"shelve_type":"下架",
			"price": 4.0
		}]
		"""
	When jobs创建微页面
		"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
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
				}],
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
			}
		}]
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",
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
				}],
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
			}
		}
		"""

#删除后不留空白区，下一个模块自动顶替被删除的模块
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				}],
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
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				}],
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
			}
		}
		"""
	#删除后再添加富文本
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ids":{
				"index": 1,
				"items": [{
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
			},
			"products": {
				"index": 2,
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
			"multy_text_content": {
				"index": 3
				"text": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
			}
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ids":{
				"index": 1,
				"items": [{
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
			},
			"products": {
				"index": 2,
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
			"multy_text_content": {
				"index": 3,
				"text": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
			}
		}
		"""
	#删除商品模块
	When jobs编辑微页面'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}
		"""
	Then jobs能获取'微页面标题1'
		"""
		{
			"title": {
				"name": "微页面标题1"
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
				}],
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格"
		}
		"""	

@termite2
Scenario: 添加模块
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


