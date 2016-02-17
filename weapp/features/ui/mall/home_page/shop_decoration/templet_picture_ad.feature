#watcher:fengxuejing@weizoom.com,benchi@weizoom.com


Feature: 自定义模块-图片广告

@ui
Scenario: （2）编辑-分开显示
	When jobs选择分开显示
	And jobs添加图片信息
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}]
	"""

	Then jobs展示区显示'图片广告'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": "推广扫码"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}]
	"""

@ui
Scenario:（3） 验证信息
	When jobs选择分开显示
	And jobs添加图片信息
	"""
		[{
			"picture_id": "1",
			"title": "标题内容超过20个字符",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": ""
		}]
	"""
	Then jobs编辑区提示错误信息'图片标题最多可输入20个字'
	And jobs展示区显示'图片广告'
	"""
		[{
			"picture_id": "1",
			"title": "标题内容超过20个字符",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": ""
		}]
	"""

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