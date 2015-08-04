#author：师帅
Feature: 自定义模块-图片导航

Background:
	Given jobs登录系统
	And jobs已添加模块
		"""
		[	
			{"modle_name": "富文本"},
			{"modle_name": "商品"},
			{"modle_name": "商品列表"},
			{"modle_name": "图片广告"},
			{"modle_name": "公告"},
			{"modle_name": "标题"},
			{"modle_name": "文本导航"},
			{"modle_name": "图片导航"},
			{"modle_name": "辅助空白"},
			{"modle_name": "橱窗"}
		]
		"""

Scenario: 数据完整时图片导航
	When jobs添加图片信息
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
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}] 
	"""

	Then jobs展示区显示'图片导航'
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
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "会员中心"
		}]
	"""

Scenario: 图片没有添加4张时，其他图片用默认图片代替
	When jobs添加图片信息
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "2",
			"title": "标题2",
			"link": "推广扫码"
		}] 
	"""

	Then jobs展示区显示'图片导航'
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
			"picture_id": "默认图片1",
			"title": "",
			"link": ""
		}, {
			"picture_id": "默认图片2",
			"title": "",
			"link": ""
		}]
	"""

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

#编辑图片导航信息
Scenario: 编辑图片导航信息
	When jobs编辑'图片导航-4'
	"""
		[{
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}]
	"""
	Then jobs展示区显示'图片导航'
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
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}]
	"""


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

