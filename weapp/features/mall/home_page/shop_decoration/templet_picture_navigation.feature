#author：师帅
Feature: 自定义模块-图片导航

Scenario: 1添加图片导航
	Given jobs登录系统
	When jobs创建微页面
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
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
		{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
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
	"""
	When jobs编辑微页面'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				},{
					"picture_id": "4",
					"title": "标题4",
					"link": "我的订单"
				}]
			}
	"""

	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				},{
					"picture_id": "4",
					"title": "标题44",
					"link": "我的订单"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""



