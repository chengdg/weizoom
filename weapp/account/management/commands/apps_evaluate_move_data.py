# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand

from apps.customerized_apps.evaluate import models as app_models
from mall import models as mall_models


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, *args, **options):
		"""
		将商品评价数据从mysql迁移到mongo中
		@param args:
		@param options:
		@return:
		"""
		print 'move data start...'
		start_time = time.time()
		#首先删除之前迁移的数据
		app_models.OrderEvaluates.objects(old_id__ne=0).delete()
		app_models.ProductEvaluates.objects(old_id__ne=0).delete()
		print 'delete last time moval'
		#从mysql中提取数据
		old_product_reviews = mall_models.ProductReview.objects.all()
		old_order_reviews = mall_models.OrderReview.objects.all()
		old_review_id2pics = dict()
		for p in mall_models.ProductReviewPicture.objects.all():
			if not old_review_id2pics.has_key(p.id):
				old_review_id2pics[p.id] = [p.att_url]
			else:
				old_review_id2pics[p.id].append(p.att_url)

		old_order_id2order_id = {o.id: o.order_id for o in mall_models.Order.objects.all()}

		print 'finished loading mysql data~'

		#插入到mongo中
		order_evaluate_creation_list = []
		#处理重复的订单,首先排除OrderEvaluates表中已存在的order_id
		has_old_id = set([o.order_id for o in app_models.OrderEvaluates.objects.all()])
		order_view_count = 0
		for old_review in old_order_reviews:
			temp_order_id = old_order_id2order_id[old_review.order_id]
			if temp_order_id in has_old_id:
				continue
			order_view_count += 1
			has_old_id.add(temp_order_id)
			order_evaluate_creation_list.append(app_models.OrderEvaluates(
				owner_id = old_review.owner_id,
				member_id = old_review.member_id,
				order_id = temp_order_id,
				serve_score = old_review.serve_score,
				deliver_score = old_review.deliver_score,
				process_score = old_review.process_score,
				old_id = old_review.id
			))
			print 'got %d order evaluates' % order_view_count

		if len(order_evaluate_creation_list) > 0:
			new_order_evaluates = app_models.OrderEvaluates.objects.insert(order_evaluate_creation_list)
			print 'moving order evaluates done ! next product evaluate'
			order_oldid2newid = {o.old_id: str(o.id) for o in new_order_evaluates}

			product_evaluate_creation_list = []
			product_view_count = 0
			for old_review in old_product_reviews:
				pics = old_review_id2pics.get(old_review.id, [])
				product_view_count += 1
				product_evaluate_creation_list.append(app_models.ProductEvaluates(
					owner_id = old_review.owner_id,
					member_id = old_review.member_id,
					order_id = old_order_id2order_id[old_review.order_id],
					old_id = old_review.id,
					product_id = old_review.product_id,
					order_evaluate_id = order_oldid2newid.get(old_review.id, 0),
					order_has_product_id = old_review.order_has_product_id,
					score = old_review.product_score,
					detail = old_review.review_detail,
					pics = pics,
					created_at = old_review.created_at,
					status = int(old_review.status),
					top_time = old_review.top_time,
					shop_reply = ''
				))
				print 'got %d product evaluates' % product_view_count
			app_models.ProductEvaluates.objects.insert(product_evaluate_creation_list)
			print 'moving product evaluates done !'
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'move data end...expend %s' % diff