#author：师帅
Feature: 微页面-个性模板2

#默认为3个模块
Background:
	Given jobs登录系统
	And jobs已添加模块信息
	"""
		[{
			"name": "1",
			"link": "link1",
			"icon": "icon1"
		}, {
			"name": "2",
			"link": "link2",
			"icon": "icon2"
		}, {
			"name": "3",
			"link": "link3",
			"icon": "icon3"
		}]
	"""
	And jobs已添加背景图片
	"""
		[{
			"background_picture": "picture1"
		}]
	"""

#最多为7个模块
Scenario:1添加个性模板
#jobs进来后在展示区显示已添加好的信息
	When jobs已添加模块信息
	"""
		[{
			"name": "4",
			"link": "link4",
			"icon": "icon4"
		}, {
			"name": "5",
			"link": "link5",
			"icon": "icon5"
		}, {
			"name": "6",
			"link": "link6",
			"icon": "icon6"
		}, {
			"name": "7",
			"link": "link7",
			"icon": "icon7"
		}]
	"""

	Then jobs展示区显示
	"""
		[{
			"background_picture": "picture1",
			"modles": [{
					"name": "1",
					"link": "link1",
					"icon": "icon1"
				}, {
					"name": "2",
					"link": "link2",
					"icon": "icon2"
				}, {
					"name": "3",
					"link": "link3",
					"icon": "icon3"
				}, {
					"name": "4",
					"link": "link4",
					"icon": "icon4"
				}, {
					"name": "5",
					"link": "link5",
					"icon": "icon5"
				}, {
					"name": "6",
					"link": "link6",
					"icon": "icon6"
				}, {
					"name": "7",
					"link": "link7",
					"icon": "icon7"
				}]
		}]
		
	"""
#对模块进行验证，删除
Scenario:2对模块进行验证，删除
	When jobs已添加模块信息
	"""
		[{
			"name": "4",
			"link": "link4",
			"icon": "icon4"
		}, {
			"name": "5",
			"link": "link5",
			"icon": "icon5"
		}, {
			"name": "6",
			"link": "link6",
			"icon": "icon6"
		}, {
			"name": "7",
			"link": "link7",
			"icon": "icon7"
		}]
	"""

	Then jobs展示区显示
	"""
		[{
			"background_picture": "picture1",
			"modles": [{
					"name": "1",
					"link": "link1",
					"icon": "icon1"
				}, {
					"name": "2",
					"link": "link2",
					"icon": "icon2"
				}, {
					"name": "3",
					"link": "link3",
					"icon": "icon3"
				}, {
					"name": "4",
					"link": "link4",
					"icon": "icon4"
				}, {
					"name": "5",
					"link": "link5",
					"icon": "icon5"
				}, {
					"name": "6",
					"link": "link6",
					"icon": "icon6"
				}, {
					"name": "7",
					"link": "link7",
					"icon": "icon7"
				}]
		}]
		
	"""
	When jobs修改个性模块'3'
	"""
		[{
			"name": "333",
			"link": "link3",
			"icon": "icon333"
		}]
	"""
	And jobs修改背景图片
	"""
		[{
			"background_picture": "picture2"
		}]
	"""
	Then jobs展示区显示
	"""
		[{
			"background_picture": "picture2",
			"modles": [{
						"name": "1",
						"link": "link1",
						"icon": "icon1"
					}, {
						"name": "2",
						"link": "link2",
						"icon": "icon2"
					}, {
						"name": "3333",
						"link": "link3",
						"icon": "icon3333"
					}, {
						"name": "4",
						"link": "link4",
						"icon": "icon4"
					}, {
						"name": "5",
						"link": "link5",
						"icon": "icon5"
					}, {
						"name": "6",
						"link": "link6",
						"icon": "icon6"
					}, {
						"name": "7",
						"link": "link7",
						"icon": "icon7"
					}]
		}]
		
	"""
	When jobs修改个性模块'4'
	"""
		[{
			"name": "444444444",
			"link": "link3",
			"icon": "icon444"
		}]
	"""
	Then jobs编辑区提示错误信息'最多可输入5个字'
	And jobs展示区显示
	"""
		[{
			"background_picture": "picture2",
			"modles":[{
						"name": "1",
						"link": "link1",
						"icon": "icon1"
					}, {
						"name": "2",
						"link": "link2",
						"icon": "icon2"
					}, {
						"name": "3333",
						"link": "link3",
						"icon": "icon3333"
					}, {
						"name": "44444",
						"link": "link4",
						"icon": "icon444"
					}, {
						"name": "5",
						"link": "link5",
						"icon": "icon5"
					}, {
						"name": "6",
						"link": "link6",
						"icon": "icon6"
					}, {
						"name": "7",
						"link": "link7",
						"icon": "icon7"
					}]
		}]
		
	"""

#删除操作
	When jobs删除个性模块'5'
	Then jobs展示区显示
	"""
		[{
			"background_picture": "picture2",
			"modles":[{
						"name": "1",
						"link": "link1",
						"icon": "icon1"
					}, {
						"name": "2",
						"link": "link2",
						"icon": "icon2"
					}, {
						"name": "3333",
						"link": "link3",
						"icon": "icon3333"
					}, {
						"name": "44444",
						"link": "link4",
						"icon": "icon444"
					}, {
						"name": "6",
						"link": "link6",
						"icon": "icon6"
					}, {
						"name": "7",
						"link": "link7",
						"icon": "icon7"
					}]
		}]
		
	"""


