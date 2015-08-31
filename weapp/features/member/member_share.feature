# __author__ : "崔帅帅"
@func:webapp.modules.user_center.views
Feature: 微信会员分享信息和关系建立
	A和B是会员,其余不是会员
	1.A-->(E,F,G)
	2.A-->B-->(E,F,G)
	3.A-->C-->(E,F,G)
	4.A-->C-->B-->(E,F,G)
	5.A-->C-->D-->(E,F,G)

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

@crm @member @member.member_share
Scenario: 建立好友关系传播情景,A-->(E,F,G)

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When tom点击bill分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		}]
		"""

	When 清空浏览器
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack点击bill分享链接
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击bill分享链接
	When nokia访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		},{
		"name": "nokia",
		"source": "会员分享",
		"is_fans": "是"
		}
		]
		"""

@crm @member @member.member_share
Scenario: 建立好友关系传播情景,A-->B-->(E,F,G)
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When li关注jobs的公众号
	When li访问jobs的webapp
	When li点击bill分享链接
	When li分享bill分享jobs的微站链接到朋友圈

	When 清空浏览器
	When tom点击li分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""
	When 清空浏览器
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack点击li分享链接
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击li分享链接
	When nokia访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

@crm @member @member.member_share
Scenario: 建立好友关系传播情景,A-->C-->(E,F,G)
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When li点击bill分享链接
	When li分享bill分享jobs的微站链接到朋友圈
	When 清空浏览器
	When tom点击li分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		}]
		"""

	When 清空浏览器
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack点击li分享链接
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击li分享链接
	When nokia访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		},{
		"name": "nokia",
		"source": "会员分享",
		"is_fans": "是"
		}]
		"""

@crm @member @member.member_share
Scenario: 建立好友关系传播情景,A-->C-->B-->(E,F,G)
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When ma点击bill分享链接
	When ma分享bill分享jobs的微站链接到朋友圈

	When 清空浏览器
	When li关注jobs的公众号
	When li访问jobs的webapp
	When li点击ma分享链接
	When li分享ma分享jobs的微站链接到朋友圈

	When 清空浏览器
	When tom点击li分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack点击li分享链接
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击li分享链接
	When nokia访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "li",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""


@crm @member @member.member_share
Scenario: 建立好友关系传播情景,A-->C-->D-->(E,F,G)
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When ma点击bill分享链接
	When ma分享bill分享jobs的微站链接到朋友圈

	When 清空浏览器
	When jordan点击ma分享链接
	When jordan分享ma分享jobs的微站链接到朋友圈

	When 清空浏览器
	When tom点击jordan分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		}]
		"""

	When 清空浏览器
	When jack关注jobs的公众号
	When jack访问jobs的webapp
	When jack点击jordan分享链接
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		}]
		"""

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击jordan分享链接
	When nokia访问jobs的webapp
	When 清空浏览器
	Given jobs登录系统
	Then jobs能获取到bill的好友
		"""
		[{
		"name": "tom",
		"source": "会员分享",
		"is_fans": "是"
		},{
		"name": "jack",
		"source": "直接关注",
		"is_fans": "否"
		},{
		"name": "nokia",
		"source": "会员分享",
		"is_fans": "是"
		}
		]
		"""
