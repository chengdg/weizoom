# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

SCORE = [0, 1, 2, 3, 4, 5]
STATUS2NAME = [u'待审核', u'已通过', u'通过并置顶', u'已屏蔽']
STATUS_DENIED = -1
STATUS_WAITTING = 0
STATUS_PASSED = 1
STATUS_TOP = 2

class Evaluates(models.Document):
	"""
	所有用户的商品评价
	"""
	owner_id = models.LongField()
	member_id= models.LongField() #评价用户
	order_id = models.StringField(default='', max_length=50)  # Order.order_id ！！！
	product_id = models.IntField() #商品id
	score = models.IntField(default=SCORE[5])  # 商品评分
	detail = models.DynamicField()  # 评价详情
	pics = models.ListField() #上传的图片
	created_at = models.DateTimeField()  # 评价时间
	top_time = models.DateTimeField() # 置顶时间
	status = models.IntField(default=STATUS_WAITTING)  # 审核状态

	meta = {
		'collection': 'evaluate_evaluates',
		'db_alias': 'apps'
	}

class EvaluateTemplateSetting(models.Document):
	"""
	手机端评价页面模版
	"""
	owner_id = models.LongField() #创建人id
	template_type = models.StringField(default='ordinary', max_length=20) #模版类型
	related_page_id = models.StringField(default='', max_length=100) #组件page_id

	meta = {
		'collection': 'evaluate_evaluate_template_setting',
		'db_alias': 'apps'
	}


class EvaluatesRelations(models.Document):
	"""
	关联评价
	"""
	owner_id = models.LongField()  #商家id
	created_at = models.DateTimeField()  # 关联时间
	related_product_ids = models.ListField()  #关联商品id集合

	meta = {
		'collection': 'evaluate_relations',
		'db_alias': 'apps'
	}

class EvaluatesRelatedProducts(models.Document):
	"""
	已经关联过的商品
	"""
	belong_to = models.StringField(default="", max_length=100)  # 对应的评价关联id
	owner_id = models.LongField()  #商家id
	product_id = models.IntField() #商品id
	meta = {
		'collection': 'evaluate_related_products',
		'db_alias': 'apps'
	}
