#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

Feature: 微页面-个性模块1

#默认有两个模块
Background:
	Given jobs登录系统
	And jobs已添加模块信息
	"""
		[{
			"name": "1",
			"link": "link1"
		}, {
			"name": "2",
			"link": "link2"
		}]
	"""

#最多只能添加四个模块
Scenario:1添加商城模块
#jobs进来后在展示区显示已添加好的信息
	When jobs添加背景图片
	"""
		[{
			"background_picture": "picture"
		}]
	"""
	And jobs已添加模块信息
	"""
		[{
			"name": "3",
			"link": "link3"
		}, {
			"name4": "4",
			"link": "link4"
		}]
	"""
	Then jobs展示区显示
	"""
	[{
			"background_picture": "picture",
			"modles": [{
							"name": "1",
							"link": "link1"
						}, {
							"name": "2",
							"link": "link2"
						}, {
							"name": "3",
							"link": "link3"
						}, {
							"name4": "4",
							"link": "link4"
						}]
		}]
	"""
Scenario:2对模块进行验证，删除
When jobs添加背景图片
	"""
		[{
			"background_picture": "picture"
		}]
	"""
	And jobs已添加模块信息
	"""
		[{
			"name": "3",
			"link": "link3"
		}, {
			"name4": "4",
			"link": "link4"
		}]
	"""
	Then jobs展示区显示
	"""
	[{
			"background_picture": "picture",
			"modles": [{
							"name": "1",
							"link": "link1"
						}, {
							"name": "2",
							"link": "link2"
						}, {
							"name": "3",
							"link": "link3"
						}, {
							"name4": "4",
							"link": "link4"
						}]
		}]
	"""
#修改导航名称,图片
	When jobs修改导航名称'4'
	"""
		[{
			"name": "456"
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
			"modles":[{
						"name": "1",
						"link": "link1"
					}, {
						"name": "2",
						"link": "link2"
					}, {
						"name": "3",
						"link": "link3"
					}, {
						"name": "456",
						"link": "link4"
					}]
		}]
		
	"""
#对导航名称字数限制
	When jobs修改导航名称'456'
	"""
		[{
			"name": "ABCDEF"
		}]
	"""
	Then jobs编辑区提示错误信息'最多可输入5个字'
	And jobs展示区显示
	"""
		[{
			"background_picture": "picture",
			"modles":[{
						"name": "1",
						"link": "link1"
					}, {
						"name": "2",
						"link": "link2"
					}, {
						"name": "3",
						"link": "link3"
					}, {
						"name": "ABCDE",
						"link": "link4"
					}]
		}]
		
	"""
#删除操作
	When jobs删除商城模块'3'
	Then jobs展示区显示
	"""
		[{
			"background_picture": "picture",
			"modles": [{
						"name": "1",
						"link": "link1"
					}, {
						"name": "2",
						"link": "link2"
					}, {
						"name": "ABCDE",
						"link": "link4"
					}]
		}]
		
	"""




