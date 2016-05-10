#author: 王丽 2015-10-26

Feature:带参数二维码-扫码
"""
	添加带参数二维码
	1 【二维码名称】：带参数二维码的名称，只在列表中使用；
	2 【扫码奖励】：扫描此二维码获得的奖励；
					可以为：
					(1)无奖励
					(2)积分
					(3)优惠券；可以是状态为"未开始"和"进行中"的所有的优惠券
	3 【成为指定等级会员】:扫码后成为会员，自动成为的会员等级设置；默认为"普通会员", 选项为会员等级下拉列表
	4 【添加到分组】：扫码后成为会员，会员进入的会员分组设置；默认为"未分组", 选项为会员分组下拉列表
	5 【已关注会员可参与】：设置已关注会员是否可参与；默认"否"
	6 【备注】：文本备注
	7 【关联会员】：设置是否关联会员；
					设置为"是"：
					(1)【关联会员】选择关联的会员;从会员列表中选择处于"关注"状态的会员,在系统中一个会员只能设置成一个带参数二维码的关联会员
					(2)【头衔】：设置关联会员的头衔；必填；设置后会在二维码页面显示头像名称，限制在5个字以内
					(3)【二维码描述语】：设置关联会员的文本二维码描述语；必填
	8 【扫码后回复】：扫码后回复；文本或者图文；必填；字数不能超过600字
"""
Background:
	Given jobs登录系统

		When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	And jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		},{
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"sub单条图文1文本内容"
		},{
			"title":"sub图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
			"cover_in_the_text":"false",
			"content":"sub单条图文2文本内容"
		},{
			"title":"sub图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/wufan1.jpg"
				}],
			"cover_in_the_text":"false",
			"jump_url":"www.baidu.com",
			"content":"sub单条图文3文本内容"
		}]
		"""

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码-扫码奖励（包含了对缓存和已关注会员可参与的校验）
	Given jobs登录系统
	#无奖励
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-奖励测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""

		#bill扫码成为会员
			When 清空浏览器
			When bill扫描带参数二维码"带参数二维码-奖励测试"
			When bill访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "bill",
					"integral": 0,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""
			Then jobs能获得优惠券'优惠券1'的码库
					"""
					{
						"coupon1_id_1": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_2": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_3": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_4": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_5": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						}
					}
					"""

	#积分奖励
		When jobs更新带参数二维码'带参数二维码-奖励测试'
			"""
			{
				"code_name": "带参数二维码-奖励测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "积分",
				"integral": 10,
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""

		#tom扫码成为会员
			When 清空浏览器
			When tom扫描带参数二维码"带参数二维码-奖励测试"
			When tom访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"integral": 10,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"integral": 0,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""
			Then jobs能获得优惠券'优惠券1'的码库
					"""
					{
						"coupon1_id_1": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_2": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_3": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_4": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_5": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						}
					}
					"""

	#优惠券奖励（已关注的会员可参与）
		When jobs更新带参数二维码'带参数二维码-奖励测试'
			"""
			{
				"code_name": "带参数二维码-奖励测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "优惠券",
				"coupon": "优惠券1",
				"is_attention_in": "true",
				"member_rank": "普通会员",
				"tags": "未分组",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""

		#marry成为会员扫码
			When 清空浏览器
			When marry关注jobs的公众号
			When marry访问jobs的webapp
			When marry扫描带参数二维码"带参数二维码-奖励测试"

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "marry",
					"integral": 0,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "tom",
					"integral": 10,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"integral": 0,
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""
			Then jobs能获得优惠券'优惠券1'的码库
					"""
					{
						"coupon1_id_1": {
							"money": 100.00,
							"status": "未使用",
							"consumer": "",
							"target": "marry"
						},
						"coupon1_id_2": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_3": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_4": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						},
						"coupon1_id_5": {
							"money": 100.00,
							"status": "未领取",
							"consumer": "",
							"target": ""
						}
					}
					"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码-重复扫码不重复奖励
	Given jobs登录系统

	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-重复扫码不重复奖励",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "积分",
			"integral": 10,
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#tom第一次扫码成为会员获得积分奖励
		When 清空浏览器
		When tom扫描带参数二维码"带参数二维码-重复扫码不重复奖励"
		When tom访问jobs的webapp

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 10,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""
	#tom第二次扫码不再获得积分奖励
		When 清空浏览器
		When tom扫描带参数二维码"带参数二维码-重复扫码不重复奖励"

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 10,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""
	#tom取消关注后第二次扫码关注不再获得积分奖励
		When 清空浏览器
		When tom取消关注jobs的公众号
		When tom扫描带参数二维码"带参数二维码-重复扫码不重复奖励"

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 10,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码-交叉扫码不重复奖励
	Given jobs登录系统

	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-交叉扫码不重复奖励1",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "积分",
			"integral": 10,
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		},{
			"code_name": "带参数二维码-交叉扫码不重复奖励2",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "积分",
			"integral": 20,
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#tom第一次扫码1成为会员获得积分奖励
		When 清空浏览器
		When tom扫描带参数二维码"带参数二维码-交叉扫码不重复奖励1"
		When tom访问jobs的webapp

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 10,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""
	#tom第一次扫码2获得积分奖励
		When 清空浏览器
		When tom扫描带参数二维码"带参数二维码-交叉扫码不重复奖励2"

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 30,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""
	#tom第二次扫码1不再获得积分奖励
		When 清空浏览器
		When tom扫描带参数二维码"带参数二维码-交叉扫码不重复奖励1"

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 30,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""
	#tom取消关注第二次扫码1关注不再过得积分奖励
		When 清空浏览器
		When tom取消关注jobs的公众号
		When tom扫描带参数二维码"带参数二维码-交叉扫码不重复奖励1"

		Given jobs登录系统
		Then jobs可以获得会员列表
			"""
			[{
				"name": "tom",
				"integral": 30,
				"source": "直接关注",
				"attention_time": "今天",
				"status": "已关注"
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:4 带参数二维码-成为指定等级会员（包含了对缓存和已关注会员可参与的校验）
	Given jobs登录系统

	#扫码关注会员的会员等级为设置会员等级
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-等级会员测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "铜牌会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""

		#bill扫码成为会员
			When 清空浏览器
			When bill扫描带参数二维码"带参数二维码-等级会员测试"
			When bill访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "bill",
					"member_rank": "铜牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

	#已关注会员扫码会员等级为设置会员等级
		When jobs更新带参数二维码'带参数二维码-等级会员测试'
			"""
			{
				"code_name": "带参数二维码-等级会员测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "金牌会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""

		#tom成为会员扫码
			When 清空浏览器
			When tom关注jobs的公众号
			When tom访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"member_rank": "铜牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

			When tom扫描带参数二维码"带参数二维码-等级会员测试"

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"member_rank": "金牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"member_rank": "铜牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

	#取消关注会员扫码关注等级为设置会员等级
			When 清空浏览器
			When marry关注jobs的公众号
			When marry访问jobs的webapp
			When marry取消关注jobs的公众号

			Given jobs登录系统
			#此处获得会员列表走了会员列表的默认查询条件"已关注"
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"member_rank": "金牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"member_rank": "铜牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

			When marry扫描带参数二维码"带参数二维码-等级会员测试"

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "marry",
					"member_rank": "金牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "tom",
					"member_rank": "金牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"member_rank": "铜牌会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

@mall2 @senior @bandParameterCode
Scenario:5 带参数二维码-添加到分组（包含了对缓存和已关注会员可参与的校验）
	Given jobs登录系统
	#扫码关注会员的会员分组为设置默认分组
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-添加到分组测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""
		#jack扫码成为会员
			When 清空浏览器
			When jack扫描带参数二维码"带参数二维码-添加到分组测试"
			When jack访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

	#扫码关注会员的会员分组为设置会员分组
		When jobs更新带参数二维码'带参数二维码-添加到分组测试'
			"""
			{
				"code_name": "带参数二维码-添加到分组测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "分组1",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""

		#bill扫码成为会员
			When 清空浏览器
			When bill扫描带参数二维码"带参数二维码-添加到分组测试"
			When bill访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "bill",
					"tags": ["分组1"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

	#已关注会员扫码会员分组为设置会员分组
		When jobs更新带参数二维码'带参数二维码-添加到分组测试'
			"""
			{
				"code_name": "带参数二维码-添加到分组测试",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "分组2",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}
			"""

		#tom成为会员扫码
			When 清空浏览器
			When tom关注jobs的公众号
			When tom访问jobs的webapp

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"tags": ["未分组"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"tags": ["分组1"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

			When tom扫描带参数二维码"带参数二维码-添加到分组测试"

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"tags": ["分组2"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"tags": ["分组1"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

	#取消关注会员扫码关注分组为设置会员分组
			When 清空浏览器
			When marry关注jobs的公众号
			When marry访问jobs的webapp
			When marry取消关注jobs的公众号

			Given jobs登录系统
			#此处获得会员列表走了会员列表的默认查询条件"已关注"
			Then jobs可以获得会员列表
				"""
				[{
					"name": "tom",
					"tags": ["分组2"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"tags": ["分组1"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

			When marry扫描带参数二维码"带参数二维码-添加到分组测试"

			Given jobs登录系统
			Then jobs可以获得会员列表
				"""
				[{
					"name": "marry",
					"tags": ["分组2"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "tom",
					"tags": ["分组2"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "bill",
					"tags": ["分组1"],
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				},{
					"name": "jack",
					"tags": ["未分组"],
					"member_rank": "普通会员",
					"source": "直接关注",
					"attention_time": "今天",
					"status": "已关注"
				}]
				"""

@mall2 @senior @bandParameterCode
Scenario:6 带参数二维码-扫码后回复
	Given jobs登录系统

	#扫码后文本回复
		When jobs添加带参数二维码
			"""
			[{
				"code_name": "带参数二维码-扫码后回复",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "false",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "文字",
				"scan_code_reply": "扫码后回复文本"
			}]
			"""
		#bill扫码成为会员
			When 清空浏览器
			When bill扫描带参数二维码"带参数二维码-扫码后回复"
			Then bill收到自动回复'扫码后回复文本'

	#已关注会员扫码获得图文回复
	Given jobs登录系统
		When jobs更新带参数二维码'带参数二维码-扫码后回复'
			"""
			{
				"code_name": "带参数二维码-扫码后回复",
				"create_time": "2015-10-10 10:20:30",
				"prize_type": "无奖励",
				"member_rank": "普通会员",
				"tags": "未分组",
				"is_attention_in": "true",
				"remarks": "",
				"is_relation_member": "false",
				"reply_type": "图文",
				"scan_code_reply": "图文1"

			}
			"""

		#tom成为会员扫码
			When 清空浏览器
			When tom关注jobs的公众号
			When tom访问jobs的webapp
			When tom扫描带参数二维码"带参数二维码-扫码后回复"

			Then tom收到自动回复'图文1'

	#取消关注会员扫码关注分组为设置会员分组
			When 清空浏览器
			When marry关注jobs的公众号
			When marry访问jobs的webapp
			When marry取消关注jobs的公众号

			When marry扫描带参数二维码"带参数二维码-扫码后回复"
			#此不是想实现取消关注的会员扫码再关注，看一下怎么实现合适

			Then marry收到自动回复'图文1'


@mall2 @senior @bandParameterCode @sun
Scenario:7 带参数二维码的修改优惠券，继续扫码
		#修改优惠券1奖励为优惠券2奖励，同一个用户只能领取一次优惠券奖励；
		#修改优惠券2奖励为优惠券1奖励时，提示该优惠券已被选用过，但是依然可以使用，但是不能被同一用户领取

	Given jobs登录系统
	When jobs添加优惠券规则
	"""
		[{
			"name": "优惠券2",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满5元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_2"
		}]
	"""
	When 清空浏览器
	When nokia关注jobs的公众号


	Given jobs登录系统
	When jobs添加带参数二维码
	"""
		[{
			"code_name": "带参数二维码-优惠券奖励",
			"create_time": "2016-05-10 10:00:00",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "2016-05-10 10:00:00",
			"relation_member": "nokia",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}]
	"""

	#未关注的用户直接扫描二维码获得优惠券奖励
	When 清空浏览器
	When mayun扫描带参数二维码"带参数二维码-优惠券奖励"于'2016-05-09 10:00:00'
	When mayun访问jobs的webapp

	#扫码的用户获得奖励
	When mayun访问jobs的webapp
	Then mayun能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""

	#同一用户再次扫码没有获得奖励
	When mayun扫描带参数二维码"带参数二维码-优惠券奖励"于'2016-05-09 11:00:00'
	When mayun访问jobs的webapp
	Then mayun能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	Given jobs登录系统
	When jobs更新带参数二维码'带参数二维码-优惠券奖励'
		"""
		{
			"code_name": "带参数二维码-优惠券奖励",
			"create_time": "2016-05-10 10:00:00",
			"prize_type": "优惠券",
			"coupon":"优惠券2",
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "2016-05-10 10:00:00",
			"relation_member": "nokia",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""

	When 清空浏览器
	When mayun扫描带参数二维码"带参数二维码-优惠券奖励"于'2016-05-10 11:00:00'
	When mayun访问jobs的webapp


	When mayun访问jobs的webapp
	Then mayun能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_2",
			"money": 100.00,
			"status": "未使用"
		}，{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""

	Given jobs登录系统
	When jobs更新带参数二维码'带参数二维码-优惠券奖励'
		"""
		{
			"code_name": "带参数二维码-优惠券奖励",
			"create_time": "今天",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "今天",
			"relation_member": "nokia",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""

	When 清空浏览器
	When mayun扫描带参数二维码"带参数二维码-优惠券奖励"于'2016-05-10 11:00:00'
	When mayun访问jobs的webapp


	When mayun访问jobs的webapp
	Then mayun能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_2",
			"money": 100.00,
			"status": "未使用"
		}，{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""

