# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

STATUS2NAME = [u'待审核', u'已通过', u'通过并置顶', u'已屏蔽']
STATUS_DENIED = -1
STATUS_WAITTING = 0
STATUS_PASSED = 1
STATUS_TOP = 2

#默认评价置顶时间
DEFAULT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')

class ProductEvaluates(models.Document):
	"""
	所有用户的商品评价
	"""
	owner_id = models.LongField()
	member_id= models.LongField() #评价用户
	order_id = models.StringField(default='', max_length=50)  # Order.order_id ！！！
	product_id = models.IntField() #商品id
	order_evaluate_id = models.StringField(max_length=100, default='') #关联的order_evaluate
	order_has_product_id = models.LongField() #order_has_product的id
	score = models.IntField(default=5)  # 商品评分
	detail = models.DynamicField()  # 评价详情
	pics = models.ListField() #上传的图片
	created_at = models.DateTimeField()  # 评价时间
	top_time = models.DateTimeField() # 置顶时间
	status = models.IntField(default=STATUS_WAITTING)  # 审核状态
	shop_reply = models.StringField(max_length=256, default='')  #商家留言

	old_id = models.LongField(default=0) #mysql中的id，用于迁移数据

	meta = {
		'collection': 'evaluate_product_evaluates',
		'db_alias': 'apps'
	}

class OrderEvaluates(models.Document):
	"""
	订单评价
	"""
	owner_id = models.LongField()
	member_id= models.LongField() #评价用户
	order_id = models.StringField(default='', max_length=50, unique=True)  # Order.order_id ！！！
	serve_score = models.IntField(default=5)  # 服务态度评分
	deliver_score = models.IntField(default=5)  # 发货速度评分
	process_score = models.IntField(default=5)  # 物流服务评分

	old_id = models.LongField(default=0) #mysql中的id，用于迁移数据

	meta = {
		'collection': 'evaluate_order_evaluates',
		'db_alias': 'apps'
	}

class EvaluateTemplateSetting(models.Document):
	"""
	手机端评价页面模版
	"""
	owner_id = models.LongField(unique=True) #创建人id
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
