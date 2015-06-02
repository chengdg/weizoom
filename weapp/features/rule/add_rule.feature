# __author__ : "崔帅帅"
@func:weixin.message.qa.views.add_rule
Feature: Add Rule
	Jobs能通过管理系统添加"关键词自动回复规则"

@weixin.message.qa
Scenario: 添加"关键词自动回复规则"
	Jobs添加"关键词自动回复规则"后, 能获取他添加的规则
	
	Given jobs登录系统
	When jobs添加关键词自动回复规则
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"patterns": "keyword1",
			"answer": "answer1"
		}]	
		"""
	Then jobs能获取关键词自动回复规则'keyword1'
		"""
		{
			"type": "text",
			"patterns": "keyword1",
			"answer": "answer1",
			"material_id": 0
		}
		"""
	And bill无法获取关键词自动回复规则'keyword1'


@weixin.message.qa 
Scenario: 添加多个"关键词自动回复规则"
	Jobs添加多个"关键词自动回复规则"后，规则列表按添加顺序倒序排列
	
	Given jobs登录系统
	When jobs添加关键词自动回复规则
		"""
		[{
			"patterns": "keyword1",
			"answer": "answer1"
		}, {
			"patterns": "keyword2",
			"answer": "answer2"
		}, {
			"patterns": "keyword3",
			"answer": "answer3"
		}]	
		"""
	Then jobs能获取关键词自动回复规则列表
		"""
		[{
			"patterns": "keyword3",
			"answer": "answer3"
		}, {
			"patterns": "keyword2",
			"answer": "answer2"
		}, {
			"patterns": "keyword1",
			"answer": "answer1"
		}]	
		"""
	And bill能获取关键词自动回复规则列表
		"""
		[]
		"""