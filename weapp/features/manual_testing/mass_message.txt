@memberList
# __editor__ : "新新"
Feature: 群发消息
	Jobs能通过管理系统将消息（文本,文本连接,表情,图文）发放给会员
	1、除已跑路会员外
	2、同个会员最多接收4条群发消息
	 	1）订阅号（认证用户、非认证用户）在1天只能群发1条消息（每天0点更新，次数不会累加）；

		2）服务号（认证用户、非认证用户），1个月（按自然月）内可发送4条群发消息（每月月底0点更新，次数不会累加）；

		3）上传至素材管理中的图片、语音可多次群发，没有有效期。

		4）群发图文消息的标题上限为64个字节。

		5）群发内容字数上限为1200个字符、或600个汉字。

		6）语音限制：最大5M，最长60秒，支持 mp3、 wma、 wav、 amr格式。

		7）视频限制：最大20M，支持rm, rmvb, wmv, avi, mpg, mpeg, mp4格式。
	3、选择会员后点击群发消息,可跳转到群发消息页，当选择给选中会员群发消息时显示群发会员名称，
		鼠标移入会员名称时出现删除标志，点击删除标志后移除该会员，点击重新筛选则回到会员管理页面
	4、群发消息至少给2个会员(不包含已跑路的会员)
	5、群发消息给多个会员
	6、向会员分组群发消息
	7、筛选条件下所有会员群发消息
	8、鼠标移入“群发消息”时显示群发选项（"给选中的人发消息(已跑路除外)"、"给筛选出来的所有人发消息(已跑路除外)"），移出时隐藏
	9、选择会员后点击群发消息,可跳转到群发消息页，
		1）当选择"给选中会员群发消息"时显示群发会员名称，鼠标移入会员名称时出现删除标志，点击删除标志后移除该会员，
			点击重新筛选则回到会员管理页面
		2）当选择"给筛选出来的所有人发消息(已跑路除外)"群发消息时，显示筛选条件，点击重新筛选则回到会员管理页面。


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
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
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

@memberList
# __editor__ : "新新"
Scenario:16 筛选条件下所有会员群发消息
	#除已跑路外
	#任一会员都没有满足4条群发消息
	Given jobs登录系统
	And jobs已有图文
		"""
		[{
			"name": "图文1"
		}]
		"""
	Given nokia关注jobs的公众号
	Given tom关注jobs的公众号
	Given tom2关注jobs的公众号
	Given tom3关注jobs的公众号
	Given tom5关注jobs的公众号
	When tom5取消了关注jobs的公众号
	When jobs选择条件为
		"""
		{
			"member_rank":"普通会员"
		}
		"""

	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-5-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已跑路"
		}]
		"""
	When jobs添加群发
		"""
		{
			"content":"图文1"
		}
		"""
	When jobs群发
	When nokia访问jobs的webapp
	Then nokia能收到群发
		"""
		{
			"content":"图文1"
		}
		"""
	When tom访问jobs的webapp
	Then tom能收到群发
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

	
