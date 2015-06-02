# __author__ : "崔帅帅"
Feature: Real time news search
	Jobs能通过管理系统对实时消息搜索

Background:
	Given jobs已有的会话消息
		"""
		[{
			"nickname":"bill",
			"content":"你好，嗨嗨嗨嗨",
			"time":"2014-9-23"
		}, {
			"nickname":"tom",
			"content":"我我我你你,啦啦嗨嗨",
			"time":"2014-8-23"
		}, {
			"nickname":"nokia",
			"content":"我我我你你,嗨我在这",
			"time":"2014-9-22"
		}]	
		"""	
	And jobs登录系统

@ignore
Scenario: 按昵称搜索
    Jobs在实时消息中按昵称搜索会话消息后
    
    1. 能获取对应昵称的会话消息
    2. 没有时间限制可以搜索任意时间的会话
    When jobs搜索昵称是'bill'的会话消息
		"""
		[{
			"search_content":"bill"
		}]	
		"""
	Then jobs能获取'bill'的会话消息
		"""
		{
			"nickname":"bill",
			"content":"你好，嗨嗨嗨嗨",
			"time":"2014-9-23"
		}
		"""
    When jobs搜索昵称是'tom'的会话消息
		"""
		[{
			"search_content" :"tom"
		}]	
		"""
	Then jobs能获取'tom'的会话消息
		"""
		{
			"nickname" :"tom",
			"content" :"我我我你你",
			"time"：:"2014-8-23"
		}
		"""

@ignore
Scenario: 按昵称搜索
    Jobs在实时消息中按关键词搜索会话消息后
    1. 能获取对应有该关键词的会话消息
    2. 按关键词搜索会话消息只能是近两天的
    When jobs搜索关键词是'嗨'的会话消息
		"""
		[{
			"search_content":"嗨"
		}]	
		"""
	Then jobs能获取关键词是'嗨'的会话消息
		"""
		[{
			"nickname":"bill",
			"content":"你好,嗨嗨嗨嗨",
			"time":"2014-9-23"
		},{
            "nickname":"nokia",
			"content":"我我我你你,嗨我在这",
			"time":"2014-9-22"
		}]
		"""
    