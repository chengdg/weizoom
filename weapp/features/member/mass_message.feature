@memberList
# __editor__ : "新新"
Feature: 群发消息
	Jobs能通过管理系统将消息（文本,文本连接,表情,图文）发放给会员
	#除已跑路会员外
	#同个会员最多接收4条群发消息
	#选择会员后点击群发消息,可跳转到群发消息页，当选择给选中会员群发消息时显示群发会员名称（无备注的显示昵称、有备注的显示备注名称），鼠标移入会员名称时出现删除标志，点击删除标志后移除该会员，点击重新筛选则回到会员管理页面
	1.群发消息给2个会员(包含已跑路的会员)
	2 群发消息给多个会员
	3 向会员分组群发消息

Background:

	Given jobs登录系统
	And jobs已有图文
		"""
		[{
			"name": "图文1"
			
		}, {
			"name": "图文2"
		}]
		"""
	When jobs添加会员分组
		"""
		[{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}]
		"""
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "未分组"
		}, {
			"name": "分组1"
		}, {
			"name": "分组2"
		}]
		"""
	Given tom1关注jobs的公众号
	Given tom2关注jobs的公众号
	Given tom3关注jobs的公众号
	Given tom5关注jobs的公众号
	Given tom5取消关注jobs的公众号
	#tom1,tom2,tom3没有接到过该公众号的任何群发
	And jobs已有会员列表
		"""
		[{
			"name": "tom1",
			"packet": "分组1",
			"status": "已关注"
		}, {
			"name": "tom2",
			"packet": "分组2",
			"status": "已关注"
		}, {
			"name": "tom3",
			"packet": "分组2",
			"status": "已关注"
		}, {
			"name": "tom5",
			"packet": "分组2",
			"status": "已跑路"
		}]
		"""

Scenario: 1 群发消息给一个会员
	#除已跑路外
    #1.至少发送2人
    #发送文本,文本连接,表情
	When jobs添加群发
	"""
		{
			"members": ["tom1", "tom5"],
			"content":"文本,文本连接,表情"
		}
	"""
	When jobs群发
	Then jobs提示群发用户数量不能不于2人

Scenario: 2 群发消息给多个会员
	#除已跑路外
	#发送图文
	Given jobs登录系统
	When jobs添加群发
	"""
		{
			"members": ["tom1","tom2","tom3","tom5"],
			"content":"图文1"
		}
	"""
	When jobs群发
	When tom1访问jobs的webapp
	Then tom1能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	When tom2访问jobs的webapp
	Then tom2能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	When tom3访问jobs的webapp
	Then tom3能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	

Scenario: 3 向会员分组群发消息
	#除已跑路外
	Given jobs登录系统
	When jobs添加群发
	"""
		{
			"grouping":"分组2",
			"content":"图文1"
		}
	"""
	When jobs群发
	When tom2访问jobs的webapp
	Then tom2能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	When tom3访问jobs的webapp
	Then tom3能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	
