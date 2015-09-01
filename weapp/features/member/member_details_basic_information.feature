# __author__ : "王丽"

Feature: 会员列表-会员详情-基本信息
"""
	1、【会员昵称】："不可编辑"，会员的头像和昵称
	2、【关注时间】："不可编辑"，会员进入系统成为系统会员的时间
	3、【会员等级】："可编辑"，会员的在系统中的等级，下拉选择会员等级列表
	3、【姓名】："可编辑"，会员的姓名，不得超过8个字符
	4、【性别】："可编辑"，单选项（男、女、未知），默认"未知"
	5、【绑定手机】："可编辑"，会员在手机端的"个人中心"的绑定手机绑定的手机号，可以修改，添加手机号校验
	6、【上次交易时间】："不可编辑"，会员支付订单（订单状态为：待发货、已发货、已完成、退款中、退款成功）的最后一个订单的"下单时间"
	7、【所在分组】："可编辑"，会员所在的分组列表，"修改"：弹出选择分组列表，多选修改会员的分组，是修改分组，不是添加分组
	8、【本店积分】："可编辑"，会员的积分数，
					（1）"调积分"：弹出调积分窗体，可以填写正或负积分，积分原因，给会员在现有积分的基础上加上调整的积分
					（2）"积分明细"：点击弹出会员的积分明细列表
						【时间】：积分变化的时间
						【类型】：购物返利、首次关注、渠道扫码奖励、推荐扫码奖励、好友点击分享链接奖励、管理员赠送、取消订单返还积分
								购物抵扣、管理员扣减、参与抽奖，花费积分
						【原因】：调整积分时填写的原因
						【管理员】："管理员赠送"、"管理员扣减"时是店铺的系统账号名
						【明细】：积分的调整数量
						【余额】：会员积分当时的余数
	9、【好友数】："不可编辑"，本会员的好友数量
	10、【备注】："可编辑"，本会员的备注信息
	11、【查看聊天记录】:"不可编辑"，点击跳转到本会员的"消息详情"页
"""
Background:

	Given jobs登录系统

	And 开启手动清除cookie模式

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100
			}, {
				"name": "商品2",
				"postage":15,
				"price":100
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

	And bill关注jobs的公众号于"2015-05-20"

	#微信用户批量下订单
		When 微信用户批量消费jobs的商品
			| date         | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2015-06-01   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 		 |        | 110         |              | 110    | 0      | 0    | jobs,支付         |  待发货         |
			| 2015-06-02   | bill     |    购买   | jobs      | 商品2,2   | 未支付  | 支付宝         | 15      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,取消         |  已取消         |
			| 2015-06-03   | bill     |    购买   | jobs      | 商品2,2   | 支付    | 支付宝         | 15      | 100      |          |        | 215         |              | 215    | 0      | 0    | jobs,发货         |  已发货         |
			| 2015-06-04   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      |          |        | 110         |              | 0      | 110    | 0    | jobs,完成         |  已完成         |
			| 2015-07-01   | bill     |    购买   | jobs      | 商品1,1   | 未支付  | 微信支付       | 10      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,无操作       |  未支付         |
			| 2015-07-02   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 货到付款       | 10      | 100      |          |        | 110         |              | 0      | 0      | 110  | jobs,完成         |  已完成         |
			| 2015-08-04   | bill     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      |          |        | 115         |              | 0      | 115    | 0    | jobs,退款         |  退款中         |
			| 2015-08-05   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          |        | 110         |              | 110    | 0      | 0    | jobs,完成退款     |  退款完成       |

Scenario:1 会员基本信息（会员昵称、关注时间、上次交易时间、）展示，修改基本信息项（姓名、会员等级、性别、绑定手机、备注）

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":0,
			"friend_count":0,
			"remarks":""
		}
		"""
	When jobs修改会员详情
		"""
		{
			"name":"会员姓名",
			"member_rank":"金牌会员",
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
			"member_rank":"金牌会员",
			"name":"会员姓名",
			"sex":"女",
			"phone":"15934567895",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":0,
			"friend_count":0,
			"remarks":"会员备注信息"
		}
		"""

Scenario:2 会员基本信息修改"所在分组"

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":0,
			"friend_count":0,
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
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":["分组1", "分组3"],
			"integral":0,
			"friend_count":0,
			"remarks":""
		}
		"""

Scenario:3 会员基本信息修改"调积分"

	Given jobs登录系统

	When jobs访问'bill'会员详情
	Then jobs获得'bill'会员详情
		"""
		{
			"member_name":"bill",
			"attention_time":"2015-05-20",
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":"",
			"integral":0,
			"friend_count":0,
			"remarks":""
		}
		"""
	When jobs给"tom3"加积分
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
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":-10,
			"friend_count":0,
			"remarks":""
		}
		"""

	When jobs给"tom3"加积分
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
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":10,
			"friend_count":0,
			"remarks":""
		}
		"""

	Then jobs获得'积分明细'列表
		"""
		[{
			"date":今天,
			"type":"管理员赠送",
			"reason":"",
			" manager":"jobs",
			"integral":20,
			"residual_integral":10
		},{
			"date":今天,
			"type":"管理员扣减",
			"reason":"jobs调整积分的原因",
			" manager":"jobs",
			"integral":-10,
			"residual_integral":-10
		}]
		"""


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
			"member_rank":"",
			"name":"",
			"sex":"未知",
			"phone":"",
			"last_buy_time":"2015-08-05",
			"tags":[],
			"integral":0,
			"friend_count":1,
			"remarks":""
		}
		"""

