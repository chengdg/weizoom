#_author_:张雪 2016.4.11
Feature: 微信用户提交高级投票申请
	"""
		1.微信用户可以通过报名高级投票
		【名称】：必填项，高级微信投票活动的名称；
		【分组选择】：必填项，下拉框选择其中一个分组；
		【输入编号】：必填项，最多可输入16个字符；
		【输入详情】：必填项；
	"""

Background:
	Given jobs登录系统
	When jobs新建高级微信投票活动
	"""
		[{
			"title":"微信高级投票",
			"groups":[],
			"rule": "高级投票规则",
			"desc":"高级微信投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"1.jpg"

		}]
	"""
	When jobs已添加单图文
		"""
		[{
			"title":"高级微信投票活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"微信高级投票摘要",
			"content":"微信高级投票内容",
			"jump_url":"微信高级投票"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "微信高级投票",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"高级微信投票活动1单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

@mall2 @apps @shvote @shvote_apply @yang
Scenario:1.微信用户可以进行高级投票报名
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级微信投票活动1单图文'
	When bill点击图文"高级微信投票活动1单图文"进入高级微信投票活动页面
	When bill参加高级投票报名活动
	"""
		{
			"headImg":"head.jpg",
			"name":"bill",
			"group":["初中组"],
			"number":"001",
			"details":"bill的产品好",
			"detail_pic":["pic1.jpg","pic2.jpg"]

		}
	"""
	Then jobs获得报名详情列表
	"""
		[{	"headImg":"head.jpg",
			"player":"bill",
			"votes":0,
			"number":"001",
			"start_date":"今天",
			"status":"待审核",
			"actions":["审核通过","删除","查看"]
		}]
	"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票",
			"participant_count":1,
			"vote_count":1,
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""
