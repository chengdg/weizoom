# __author__ : "崔帅帅"
Feature: Real time message
	Jobs能通过管理系统对实时消息收藏

Background:
	Given jobs已有的会话消息
		"""
		[{
			"nickname":"bill",
			"news": [{
				      "content":"bbbbbb",
			          "time":"2014-9-23"
			        },{
			           "content":"cccccc",
			           "time":"2014-9-18"
			        }]
		}]	
		"""	
    And jobs登录系统

@ignore
 Scenario: 收藏单个会话消息
    Jobs在实时消息中收藏单个的会话消息后,能获取收藏的单个会话消息
    
    When jobs收藏'bill'2014-9-18的会话消息
	Then jobs能获取收藏列表
		"""
		{
			"nickname":"bill",
			"content":"cccccc",
			"time":"2014-9-18"
		}
		"""

@ignore
Scenario: 收藏多个会话消息
    Jobs在实时消息中收藏单个的会话消息后,能获取收藏的单个会话消息
    
    When jobs收藏'bill'的所有会话消息
	Then jobs能获取收藏列表
		"""
		[{
			"nickname":"bill",
			"content" : "bbbbbb",
			"time":"2014-9-23"
		},{
		     "nickname":"bill",
			 "content":"cccccc",
			 "time":"2014-9-18"
		}]
		"""

@ignore
Scenario: 取消收藏
    Jobs在实时消息中取消收藏会话消息后,获取不到收藏的会话消息
    
    When jobs取消收藏'bill'2014-9-23的会话消息
	Then jobs能获取收藏列表
		"""
		{
		     "nickname":"bill",
			 "content":"cccccc",
			 "time":"2014-9-18"
		}
		"""
