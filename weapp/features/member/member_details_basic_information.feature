# __author__ : "王丽"
#editor: 新新 2016.3.28
#editor: 田丰敏 2016.5.31

Feature: 会员列表-会员详情-基本信息
"""
	#editor: 新新 
	2016.3.28修改需求
	1、【会员昵称】："不可编辑"，会员的头像和昵称
	2、【关注时间】："不可编辑"，会员进入系统成为系统会员的时间;关注方式
	3、【会员等级】："可编辑"，会员的在系统中的等级，下拉选择会员等级列表
	4、【备注姓名】："可编辑"，会员的姓名，不得超过8个字符
	5、【性别】："可编辑"，单选项（男、女、未知），默认"未知"
	6、【绑定手机】："可编辑"，会员在手机端的"个人中心"的绑定手机绑定的手机号，可以修改，添加手机号校验
	7、【最近交易时间】："不可编辑"，会员支付订单（订单状态为：已完成）
	8、【所在分组】："可编辑"，会员所在的分组列表，"修改"：弹出选择分组列表，多选修改会员的分组，是修改分组，不是添加分组;分组长的情况下移到下行显示
	9、【本店积分】："可编辑"，会员的积分数，
					（1）"调积分"：弹出调积分窗体，可以填写正或负积分，积分原因，给会员在现有积分的基础上加上调整的积分
					（2）"查看"：点击弹出会员的积分明细列表
						【时间】：积分变化的时间
						【类型】：购物返利、首次关注、渠道扫码奖励、推荐扫码奖励、好友点击分享链接奖励、管理员赠送、取消订单返还积分
								购物抵扣、管理员扣减、参与抽奖，花费积分
						【原因】：调整积分时填写的原因
						【管理员】："管理员赠送"、"管理员扣减"时是店铺的系统账号名
						【明细】：积分的调整数量
						【余额】：会员积分当时的余数
	10、【推荐数】："不可编辑"，本会员的推荐会员数
	11、【购买次数】："不可编辑"，本会员的购买次数（订单状态为：已完成）
	12、【平均客单价】："不可编辑"，本会员的平均客单价（订单状态为：已完成）
	13、【微众卡使用金额】："不可编辑"，本会员的微众卡使用金额（订单状态为：已完成）
	14、【备注】："可编辑"，本会员的备注信息
	15、【聊天记录】:"不可编辑"，点击跳转到本会员的"消息详情"页

	# __author__ : "王丽"
	2015-9新增需求
	1、会员分组默认有个分组："未分组"，不能修改（没有修改框）、不能删除（没有删除按钮）
	2、新增会员和调整没有分组的会员，默认进入"未分组"
"""
Background:

	Given jobs登录系统

	And 开启手动清除cookie模式

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10.00,
				"price":100.00
			}, {
				"name": "商品2",
				"postage":15.00,
				"price":100.00
			}]
			"""
		And jobs已添加支付方式
			"""
			[{
				"type": "货到付款",
				"is_active": "启用"
			},{
				"type": "微信支付",
				"is_active": "启用"
			},{
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""
		And jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"discount": "10"
			},{
				"name": "金牌会员",
				"upgrade": "手动升级",
				"discount": "9"
			}]
			"""

		When jobs添加会员分组
			"""
			{
				"tag_id_1": "分组1",
				"tag_id_2": "分组2",
				"tag_id_3": "分组3"
			}
			"""

	And bill关注jobs的公众号于'2015-05-20'

@mall2 @member @memberList @member_detail_new @bert
Scenario:1 会员基本信息（会员昵称、关注时间、上次交易时间只计算已完成订单时间）展示，修改基本信息项（姓名、会员等级、性别、绑定手机、备注）

	#微信用户批量下订单
		When 微信用户批量消费jobs的商品
			| order_id | date         | consumer |  product  | payment | pay_type | postage*|   price* | paid_amount*| alipay*| wechat*| cash* |    action     | order_status*|
			|   0001   | 2015-06-01   | bill     | 商品1,1   | 支付    | 支付宝   | 10.00   | 100.00   | 110.00      | 110.00 | 0.00   | 0.00  |               | 待发货       |
			|   0002   | 2015-06-02   | bill     | 商品2,2   |         | 支付宝   | 15.00   | 100.00   | 0.00        | 0.00   | 0.00   | 0.00  | jobs,取消     | 已取消       |
			|   0003   | 2015-06-03   | bill     | 商品2,2   | 支付    | 支付宝   | 15.00   | 100.00   | 215.00      | 215.00 | 0.00   | 0.00  | jobs,发货     | 已发货       |
			|   0004   | 2015-06-04   | bill     | 商品1,1   | 支付    | 微信支付 | 10.00   | 100.00   | 110.00      | 0.00   | 110.00 | 0.00  | jobs,完成     | 已完成       |
			|   0005   | 2015-07-01   | bill     | 商品1,1   |         | 微信支付 | 10.00   | 100.00   | 0.00        | 0.00   | 0.00   | 0.00  |               | 待支付       |
			|   0006   | 2015-07-02   | bill     | 商品1,1   | 支付    | 货到付款 | 10.00   | 100.00   | 110.00      | 0.00   | 0.00   | 110.00| jobs,完成     | 已完成       |
			|   0007   | 2015-08-04   | bill     | 商品2,1   | 支付    | 微信支付 | 15.00   | 100.00   | 115.00      | 0.00   | 115.00 | 0.00  | jobs,退款     | 退款中       |
			|   0008   | 2015-08-05   | bill     | 商品1,1   | 支付    | 支付宝   | 10.00   | 100.00   | 110.00      | 110.00 | 0.00   | 0.00  | jobs,完成退款 | 退款成功     |

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"今天",
			"tags": ["未分组"],
			"integral":0,
			"fans_count":0,
			"remarks":""
		}
		"""
	When jobs修改会员详情
		"""
		{
			"name":"会员姓名",
			"grade":"金牌会员",
			"sex":"女",
			"phone":"15934567895",
			"remarks":"会员备注信息"
		}
		"""
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"金牌会员",
			"name":"会员姓名",
			"sex":"女",
			"phone":"15934567895",
			"last_buy_time":"今天",
			"tags": ["未分组"],
			"integral":0,
			"fans_count":0,
			"remarks":"会员备注信息"
		}
		"""

@mall2 @member @memberList @member_detail_new @bert
Scenario:2 会员基本信息修改"所在分组"

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags": ["未分组"],
			"integral":0,
			"fans_count":0,
			"remarks":""
		}
		"""
	When jobs给"bill"调分组
		"""
		[
			"分组1", "分组3"
		]
		"""
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags":["分组1", "分组3"],
			"integral":0,
			"fans_count":0,
			"remarks":""
		}
		"""

@mall2 @member @memberList  @member_detail_new @bert
Scenario:3 会员基本信息修改"调积分"

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags": ["未分组"],
			"integral":0,
			"fans_count":0,
			"remarks":""
		}
		"""
	When jobs给"bill"加积分
			"""
			{
				"integral":-10,
				"reason":"jobs调整积分的原因"
			}
			"""
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags": ["未分组"],
			"integral": -10,
			"fans_count":0,
			"remarks":""
		}
		"""

	When jobs给"bill"加积分
			"""
			{
				"integral":20,
				"reason":""
			}
			"""
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags": ["未分组"],
			"integral": 10,
			"fans_count":0,
			"remarks":""
		}
		"""

	Then jobs获得'积分明细'列表
		"""
		[{
			"date":"今天",
			"event_type":"管理员赠送",
			"reason":"",
			"manager":"jobs",
			"integral_count": "20",
			"current_integral": "10"
		},{
			"date":"今天",
			"event_type":"管理员扣减",
			"reason":"jobs调整积分的原因",
			"manager":"jobs",
			"integral_count":"-10",
			"current_integral":"-10"
		}]
		"""

@mall2 @member @memberList  @member_detail_new @bert
Scenario:4 会员基本信息推荐数验证
	#bill和tom建立好友关系
			When bill访问jobs的webapp
			When bill把jobs的微站链接分享到朋友圈
			When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'

			When 清空浏览器
			When tom点击bill分享链接
			Then tom在jobs公众号中有uuid对应的webapp_user
			Then 浏览器cookie包含"[fmt, uuid]"
			Then 浏览器cookie等于
				"""
				{"fmt":"mt_{bill_jobs}"}
				"""
			When tom关注jobs的公众号
			When tom访问jobs的webapp

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"grade":"普通会员",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"",
			"tags": ["未分组"],
			"integral":0,
			"fans_count":1,
			"remarks":""
		}
		"""

