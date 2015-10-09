#author：师帅

Feature: 自定义模块-图片广告

<<<<<<< Updated upstream
Scenario:1 新建微页面
	When jobs登录系统
	And jobs创建微页面
=======
Background:
	Given jobs登录系统
	And jobs已创建微页面
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
	"""
		{
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
		}
	"""

Scenario: 2验证信息
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
=======
	"""
		{
>>>>>>> Stashed changes
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
<<<<<<< Updated upstream
				"display_mode": "轮播图"
				"values":[{
					"picture_id": "",
=======
				"values":[{
					"picture_id": "1",
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
		}]
	"""
	Then jobs提示'请添加一张图片'
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"picture_ads":{
				"display_mode": "轮播图"
				"values":[{
					"picture_id": "1",
					"title": "",
					"link": "店铺主页"
				},{
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
				},{
=======
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
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
				"display_mode": "轮播图"
				"values":[{
					"picture_id": "1",
					"title": "",
					"link": "店铺主页"
				},{
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
=======
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
>>>>>>> Stashed changes
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
<<<<<<< Updated upstream
=======
				},{
					"picture_id": "4",
					"title": "标题4",
					"link": "会员中心"
>>>>>>> Stashed changes
				}]
			}
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
<<<<<<< Updated upstream
			"picture_ads":{
				"display_mode": "轮播图"
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": ""
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
	Then jobs提示'链接地址不能为空'


Scenario: 3删除
	When jobs登录系统
	And jobs创建微页面
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
=======
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
>>>>>>> Stashed changes
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
<<<<<<< Updated upstream
				"display_mode": "轮播图"
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
					"link": "个人中心"
=======
					"link": "问卷调查"
>>>>>>> Stashed changes
				}]
			}
		}
	"""
<<<<<<< Updated upstream
	When jobs删除'标题1'
=======
>>>>>>> Stashed changes
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			},
			"picture_ads":{
<<<<<<< Updated upstream
				"display_mode": "轮播图"
				"values":[{
=======
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
>>>>>>> Stashed changes
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
				},{
					"picture_id": "3",
					"title": "标题3",
<<<<<<< Updated upstream
					"link": "个人中心"
=======
					"link": "问卷调查"
>>>>>>> Stashed changes
				}]
			}
		}
	"""
<<<<<<< Updated upstream
	When jobs删除'图片广告'
	Then jobs能获取'微页面标题'
	"""
		{
			"title": {
				"name": "微页面标题"
			}
		}
	"""
=======
>>>>>>> Stashed changes


@ui
Scenario: （6）添加图片
	#验证之前用过的图片，在'用过的图片中显示'便于选择图片使用
	When jobs添加新图片
	"""
		[{
			"picture_id": "1"
		}, {
			"picture_id": "2"
		}, {
			"picture_id": "3"
		}, {
			"picture_id": "4"
		}]
	"""
	Then jobs展示区显示'图片广告'
	"""
		[{
			"picture_id": "1"
		}, {
			"picture_id": "2"
		}, {
			"picture_id": "3"
		}, {
			"picture_id": "4"
		}]
	"""
	Then jobs在用过的图片中显示
	"""
		[{
			"picture_id": "1"
		}, {
			"picture_id": "2"
		}, {
			"picture_id": "3"
		}, {
			"picture_id": "4"
		}]
	"""