#watcher:wangli@weizoom.com,benchi@weizoom.com
#author: 王丽 2015-10-26

Feature:带参数二维码-添加和修改
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

	And bill关注jobs的公众号于'2015-10-01 10:00:00'
	And tom关注jobs的公众号于'2015-10-02'

@mall2 @senior @bandParameterCode
Scenario:1 添加带参数二维码
	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、否、无备注、否、扫码后回复文本
	#添加：积分奖励、金牌会员、分组1、是、带参数二维码备注、是、扫码后回复图文（设置了关联会员后又取消设置关联会员）
	#添加：优惠券奖励、金牌会员、分组1、是、带参数二维码备注、是、扫码后回复图文（设置了关联会员）

	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		},{
			"code_name": "带参数二维码-积分奖励",
			"create_time": "2015-10-11 10:20:30",
			"prize_type": "积分",
			"integral": 10,
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_time": "2015-10-10 10:20:30",
			"relation_member": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		},{
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
			"cancel_related_time": "",
			"relation_member": "tom",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}]
		"""
	Then jobs获得带参数二维码'带参数二维码-默认设置'
		"""
		{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}
		"""
	Then jobs获得带参数二维码'带参数二维码-积分奖励'
		"""
		{
			"code_name": "带参数二维码-积分奖励",
			"create_time": "2015-10-11 10:20:30",
			"prize_type": "积分",
			"integral": 10,
			"member_rank": "金牌会员",
			"tags": "分组1",
			"is_attention_in": "true",
			"remarks": "带参数二维码备注",
			"is_relation_member": "true",
			"relation_member": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""
	Then jobs获得带参数二维码'带参数二维码-优惠券奖励'
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
			"relation_member": "tom",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""

@mall2 @senior @bandParameterCode
Scenario:2 修改带参数二维码
	Given jobs登录系统
	#添加：无奖励、普通会员、未分组、否、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
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
	Then jobs获得带参数二维码'带参数二维码-默认设置'
		"""
		{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}
		"""

	#修改：优惠券奖励、金牌会员、分组1、是、带参数二维码备注、是、扫码后回复图文（设置了关联会员）
	When jobs更新带参数二维码'带参数二维码-默认设置'
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
			"relation_member": "tom",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""
	Then jobs获得带参数二维码'带参数二维码-优惠券奖励'
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
			"relation_member": "tom",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "图文",
			"scan_code_reply": "图文1"
		}
		"""
