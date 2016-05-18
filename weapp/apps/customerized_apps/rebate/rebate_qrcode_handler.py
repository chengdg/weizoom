# -*- coding: utf-8 -*-
__author__ = 'aix'

from core.exceptionutil import unicode_full_stack
from weixin.message.handler.event_handler import *
from weixin.message.material.models import News

import models as apps_models

class RebateQrcodeHandler(MessageHandler):

	def name(self):
		return "RebateQrcodeHandler"

	def handle(self, context, is_from_simulator=False):
		message = context.message

		if message.is_optimization_message:
			print 'RebateQrcodeHandler only handle is_optimization_message = true'
			return None

		username = message.fromUserName
		user_profile = context.user_profile
		member = context.member

		if not hasattr(context.message, 'event'):
			return None

		if not hasattr(context.message, 'ticket') or context.message.ticket is None:
			return None
		ticket = context.message.ticket

		if not hasattr(context.message, 'eventKey') or context.message.eventKey is None or ticket == '':
			return None

		#优化处理
		if hasattr(context, 'is_member_qrcode') and (context.is_member_qrcode is True):
			return None

		if member and (hasattr(member, 'is_new') is False):
			member.is_new = False

		try:
			rebate_record = apps_models.Rebate.objects.get(owner_id=user_profile.user_id, ticket=ticket, status=apps_models.STATUS_RUNNING)
		except:
			print unicode_full_stack()
			return None
		member_info = apps_models.RebateParticipance.objects(belong_to=str(rebate_record.id), member_id=member.id)
		if member_info.count() <= 0:
			member_info = apps_models.RebateParticipance(
				belong_to=str(rebate_record.id),
				member_id=member.id,
				is_new=member.is_new,
				created_at=datetime.now())
			member_info.save()

		if rebate_record.reply_type == 1 and rebate_record.reply_detail:
			if is_from_simulator:
				return generator.get_text_response(username, message.toUserName, emotion.change_emotion_to_img(rebate_record.reply_detail), username, user_profile)
			else:
				return generator.get_text_response(username, message.toUserName, rebate_record.reply_detail, username, user_profile)
		news = get_material_news_info(rebate_record.reply_material_id)
		if rebate_record.reply_type == 2 and news:
			return generator.get_news_response(username, message.toUserName, news, username)

		return None

def get_material_news_info(material_id):
	try:
		material_id = int(material_id)
		news = list(News.objects.filter(material_id=material_id, is_active=True))
		return news
	except:
		return None