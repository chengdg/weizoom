# __author__ : "benchi"
Feature: jobs能看到 实时消息的详情，分为能回复，与不能回复（消息仅在48小时内回复有效）

Background:
	Given jobs登录系统
	And bill关注jobs的公众号
	And jobs已获取"bill"的基本资料
	"""
		[{
			"remark_name": "billb",
			"gender": "男",
	   		"location": "中国  北京  海淀",
	   		"member_level": "普通会员",
	   		"integral": 100,
	   		"fans_group": "分组一",
	   		"binding_tel": 15686896236,
	   		"attention_time": "2014-12-30 20:06:43"
		}]
	"""
	And tom关注jobs的公众号
	And jobs已获取"tom"的基本资料
	"""
		[{
			"remark_name": "tomb",
			"gender": "男",
	   		"location": "中国  北京  西城",
	   		"member_level": "普通会员",
	   		"integral": 50,
	   		"fans_group": "分组二",
	   		"binding_tel": 15686896237,
	   		"attention_time": "2014-11-30 20:06:43"
		}]
	"""

@new_weixin.message
Scenario: 1 jobs可以看到消息详情
	Given jobs登录系统
	And jobs已获取"bill"粉丝信息列表
	"""
		[{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容1",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    },{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容2",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    },{
			"fans_name": "tom",
	   		"inf_content": "tom信息内容",
	    	"last_message_time": "48小时前",
	    	"remark": ""
	    }]
	"""
	And jobs已回复"bill"
		"""
		[{
			"replied_content": "jobs回复bill信息内容"
	     }]
	"""

	Then jobs成功获取"bill"消息详情列表
	"""
		{
			"messages": [{
				"replied_content": "jobs回复bill信息内容"
			},{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容1",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    },{
			"fans_name": "bill",
	   		"inf_content": "bill信息内容2",
	    	"last_message_time": "48小时内",
	    	"remark": ""
	    }],
	    "member_information": [{
				"remark_name": "billb",
				"gender": "男",
		   		"location": "中国  北京  海淀",
		   		"member_level": "普通会员",
		   		"integral": 100,
		   		"fans_group": "分组一",
		   		"binding_tel": 15686896236,
		   		"attention_time": "2014-12-30 20:06:43"
		}],
			"can_reply":true
		}
	"""

	Then jobs成功获取"tom"消息详情列表
	"""
		{
			"messages": [{
				"fans_name": "tom",
		   		"inf_content": "tom信息内容",
		    	"last_message_time": "48小时前",
	    		"remark": ""
		   		 }],
	   		 "member_information": [{
				"remark_name": "tomb",
				"gender": "男",
		   		"location": "中国  北京  西城",
		   		"member_level": "普通会员",
		   		"integral": 50,
		   		"fans_group": "分组二",
		   		"binding_tel": 15686896237,
		   		"attention_time": "2014-11-30 20:06:43"
			}],
			"can_reply":false
		}
	"""
	