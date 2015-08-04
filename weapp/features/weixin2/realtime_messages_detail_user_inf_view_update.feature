# __author__ : "benchi"
Feature: jobs浏览，修改 用户的的基本资料

Background:
	Given jobs登录系统
	And bill关注jobs的公众号
	And jobs已获取"bill"的基本资料
	"""
		[{
			"remark_name": "billb",
			"gender": "未知",
	   		"location": "中国  北京  海淀",
	   		"member_level": "普通会员",
	   		"integral": 100,
	   		"fans_group": "分组一",
	   		"binding_tel": 15686896236,
	   		"attention_time": "2014-12-30 20:06:43",
	   		"last_buy_time": "2014-12-30 21:06:43",
	   		"buy_count": 1,
	   		"product_price": 50,
	   		"the_sum": 50
		}]
	"""
@new_weixin.message
Scenario: 1 jobs编辑修改 用户的的基本资料
			修改完单独的信息后即可保存，例如对 备注姓名，修改完后，即完成保存工作

	Given jobs登录系统
	And jobs已获取"bill"粉丝信息列表
	"""
		[{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容1",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    }]
	"""
	Then jobs成功获取"bill"消息详情列表
	"""
		{
			"messages": [{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容1",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    }],
	    "member_information": [{
				"remark_name": "billb",
				"gender": "未知",
		   		"location": "中国  北京  海淀",
		   		"member_level": "普通会员",
		   		"integral": 100,
		   		"fans_group": "分组一",
		   		"binding_tel": 15686896236,
		   		"attention_time": "2014-12-30 20:06:43",
		   		"last_buy_time": "2014-12-30 21:06:43",
		   		"buy_count": 1,
		   		"product_price": 50,
		   		"the_sum": 50
		}],
			"can_reply":true
		}
	"""

	When jobs修改"bill"基本资料"备注姓名"
	"""
		[{
			"remark_name": "billbb"
			}]
	"""
	And jobs修改"bill"基本资料"性别"
	"""
		[{
			"gender": "男"
	   		}]
	"""
	And jobs修改"bill"基本资料"粉丝等级"
	"""
		[{
			"member_level": "钻石会员"
	   		}]
	"""
	And jobs修改"bill"基本资料"本店积分"
	"""
		[{
			"integral": 200
	   		}]
	"""

	And jobs修改"bill"基本资料"粉丝分组"
	"""
		[{
			"integral": "分组二"
	   		}]
	"""

	Then jobs成功获取"bill"消息详情列表
	"""
		{
			"messages": [{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容1",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    }],
	    "member_information": [{
				"remark_name": "billbb",
				"gender": "男",
		   		"location": "中国  北京  海淀",
		   		"member_level": "钻石会员",
		   		"integral": 200,
		   		"fans_group": "分组二",
		   		"binding_tel": 15686896236,
		   		"attention_time": "2014-12-30 20:06:43",
		   		"last_buy_time": "2014-12-30 21:06:43",
		   		"buy_count": 1,
		   		"product_price": 50,
		   		"the_sum": 50
		}],
			"can_reply":true
		}
	"""