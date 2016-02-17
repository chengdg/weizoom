#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
#author：师帅

Feature: 自定义模块-图片导航

@ui
Scenario: 验证信息
	When jobs添加图片信息
	"""
		[{
			"picture_id": "1",
			"title": "描述语最多可输入5个字",
			"link": "推广扫码"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": ""
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "描述语最多可输入5个字",
			"link": "会员中心"
		}]
	"""
	Then jobs编辑区提示错误信息'描述语最多可输入5个字'
	And jobs展示区显示'图片导航'
	"""
		[{
			"picture_id": "1",
			"title": "描述语显示5个字",
			"link": "推广扫码"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": ""
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "描述语显示5个字",
			"link": "会员中心"
		}]
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