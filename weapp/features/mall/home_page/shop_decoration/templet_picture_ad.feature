#author：师帅
Feature: 自定义模块-图片广告

@termite2
Scenario: 1 创建微页面
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}
	"""

@termite2
Scenario: （2）验证删除，添加
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}
	"""
#删除'标题2
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}
	"""
#添加一个图片广告
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题3",
					"link": "会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题4",
					"link": "会员主页"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题3",
					"link": "会员主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题4",
					"link": "会员主页"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
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

@termite2
Scenario: （3）编辑图片广告信息
	#编辑图片广告信息
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}]
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "会员主页"
				}]
			}
		}
	"""
#修改'标题3'
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题3",
					"link": "店铺主页"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "轮播图",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题3",
					"link": "店铺主页"
				}]
			}
		}
	"""
#将轮播图修改为分开显示
	When jobs编辑微页面'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "分开显示",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "店铺主页"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题1'
	"""
		{
			"title": {
				"name": "微页面标题1"
			},
			"picture_ads":{
				"display_mode": "分开显示",
				"values":[{
					"path": "/standard_static/test_resource_img/hangzhou1.jpg",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"path": "/standard_static/test_resource_img/hangzhou2.jpg",
					"title": "标题2",
					"link": "我的订单"
				},{
					"path": "/standard_static/test_resource_img/hangzhou3.jpg",
					"title": "标题3",
					"link": "店铺主页"
				}]
			}
		}
	"""
