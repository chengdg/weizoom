#author：师帅
Feature: 自定义模块-图片广告

Background:
	Given jobs登录系统
	And jobs已添加模块
		"""
		[	
			{"model_name": "富文本"},
			{"model_name": "商品"},
			{"model_name": "商品列表"},
			{"model_name": "图片广告"},
			{"model_name": "公告"},
			{"model_name": "标题"},
			{"model_name": "文本导航"},
			{"model_name": "图片导航"},
			{"model_name": "辅助空白"},
			{"model_name": "橱窗"}
		]
		"""

Scenario: （1）编辑-轮播图
	When jobs选择轮播图
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
		}]
	"""

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

Scenario: （4）验证删除后在添加
	#验证删除后再添加图片信息，排序按照正序排列
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
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "用户反馈"
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
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "用户反馈"
		}]
	"""
	When jobs删除'2'
	Then jobs展示区显示'图片广告'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "用户反馈"
		}]
	"""
	When jobs添加图片信息
	"""
		[{
			"picture_id": "5",
			"title": "标题5",
			"link": "会员中心"
		}]
	"""
	Then jobs展示区显示'图片广告'
	"""
		[{
			"picture_id": "1",
			"title": "标题1",
			"link": "店铺主页"
		}, {
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "用户反馈"
		}, {
			"picture_id": "5",
			"title": "标题5",
			"link": "会员中心"
		}]
	"""

Scenario: （5）编辑图片广告信息
	#编辑图片广告信息
	When jobs编辑'图片广告-4'
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
			"picture_id": "3",
			"title": "标题3",
			"link": "个人中心"
		}, {
			"picture_id": "4",
			"title": "标题4",
			"link": "问卷调查"
		}, {
			"picture_id": "5",
			"title": "标题5",
			"link": "会员中心"
		}]
	"""

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
