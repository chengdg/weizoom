#author：师帅

Feature: 自定义模块-图片导航

<<<<<<< Updated upstream
Scenario: 1新建微页面
	When jobs登录系统
	And jobs创建微页面
=======
Scenario: 1添加图片导航
	When jobs创建微页面
>>>>>>> Stashed changes
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
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
<<<<<<< Updated upstream
		{
=======
		[{
>>>>>>> Stashed changes
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
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
<<<<<<< Updated upstream
		}
	"""

Scenario: 2验证信息
	When jobs登录系统
	And jobs创建微页面
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
					"picture_id": "",
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
	Then jobs提示'请添加一张图片'
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"picture_ids":{
				"values":[{
					"picture_id": "1",
					"title": "",
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
=======
		}]
	"""

Scenario: 2编辑图片导航信息
	When jobs创建微页面'微页面标题'
	"""
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
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
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
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
				},{
					"picture_id": "4",
					"title": "标题4",
					"link": "会员中心"
				}]
			}
		}]
	"""
	When jobs编辑微页面'微页面标题'
	And jobs修改'标题4'
	"""
		[{
			"picture_id": "4",
			"title": "标题44",
			"link": "我的订单"
>>>>>>> Stashed changes
		}]
	"""
	Then jobs能获取'微页面标题'
	"""
<<<<<<< Updated upstream
		{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
					"picture_id": "1",
					"title": "",
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
		}
	"""
	When jobs编辑微页面'微页面标题'
	"""
		[{
			"picture_ids":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": ""
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
	Then jobs提示'链接地址不能为空'


Scenario: 3删除
	When jobs登录系统
	And jobs创建微页面
	"""
=======
>>>>>>> Stashed changes
		[{
			"title":{
				"name": "微页面标题"
			},
			"picture_ids":{
				"values":[{
					"picture_id": "1",
					"title": "标题1",
					"link": "店铺主页"
				},{
					"picture_id": "2",
					"title": "标题2",
					"link": "推广扫码"
<<<<<<< Updated upstream
				}, {
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				}, {
					"picture_id": "4",
					"title": "标题4",
					"link": "会员中心"
=======
				},{
					"picture_id": "3",
					"title": "标题3",
					"link": "个人中心"
				},{
					"picture_id": "4",
					"title": "标题44",
					"link": "我的订单"
>>>>>>> Stashed changes
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
			"picture_ids":{
				"values":[{
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
		}
	"""
	When jobs删除'图片导航'
	Then jobs能获取'微页面标题'
	"""
		{
			"title":{
				"name": "微页面标题"
			}
		}
	"""



@ui
#验证之前用过的图片，在'用过的图片中显示'便于选择图片使用
Scenario: 添加图片
	When jobs添加新图片
	"""
		[{
			"picture_id": "1"
		}, {
			"picture_id": "2"
		}, {
			"picture_id": "3"
		}, {
			"picture_id": "4"；
		}]
	"""
	Then jobs展示区显示'图片导航'
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