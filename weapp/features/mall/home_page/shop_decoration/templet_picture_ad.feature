#author：师帅
Feature: 自定义模块-图片广告


Background:
	Given jobs登录系统
	And jobs已创建微页面
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"display_mode": "轮播图"
				"values":[{
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
			"picture_ads":{
				"values":[{
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
				}]
			}
		}
	"""



Scenario: （4）验证删除，添加
	#验证删除后再添加图片信息，排序按照正序排列
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
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
			"picture_ads":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				},{
					"picture_id": "4",
					"title": "标题4",
					"link": "个人中心"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				},{
					"picture_id": "4",
					"title": "标题4",
					"link": "会员中心"
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"title": {
				"name": "微页面标题"
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

Scenario: （5）编辑图片广告信息
	#编辑图片广告信息
	When jobs编辑微页面'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"values":[{
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
					"link": "问卷调查"
				}]
			}
		}
	"""
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
				"values":[{
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
					"link": "问卷调查"
				}]
			}
		}
	"""


