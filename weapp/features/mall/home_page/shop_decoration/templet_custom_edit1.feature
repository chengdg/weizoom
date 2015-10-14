#author：师帅
Feature: 编辑自定义模块-编辑

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
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",				
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
			"multy_text_content": "富文本标题文字，换行显示图片，换行显示3行3列的表格",				
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