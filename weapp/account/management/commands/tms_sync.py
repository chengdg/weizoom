# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from core.wxapi import get_weixin_api
from core.exceptionutil import unicode_full_stack
from account.models import UserProfile
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from weixin2.models import UserHasTemplateMessages, UserTemplateSettings


class Command(BaseCommand):
	help = ''
	args = ''
	
	def handle(self, *args, **options):
		"""
		同步模板
		"""
		print 'tms sync start...'
		l = len(args)
		if l == 1:
			if not args[0].isdigit():
				print '参数为user_id, 必须为正整数！！'
				return
			users = UserProfile.objects.filter(user_id=int(args[0]))
		else:
			users = [u.user for u in UserProfile.objects.filter(is_active=True, is_mp_registered=True, is_oauth=True)]

		for user in users:
			mpuser_access_token = _get_mpuser_access_token(user)
			if mpuser_access_token:
				user_id = user.id
				print 'start handle user [{}]`s templates...'.format(user.username)
				try:
					weixin_api = get_weixin_api(mpuser_access_token)
					curr_template_info = {t.template_id: t for t in
										  UserHasTemplateMessages.objects.filter(owner_id=user_id)}
					result = weixin_api.get_all_template_messages(True)
					template_list = result['template_list']
					need_create_list = []  # 商家新配置的模版
					all_sync_ids = []  # 商家配置的所有模版id
					need_delete_ids = []  # 商家删除的模版id
					for t in template_list:
						template_id = t['template_id']
						all_sync_ids.append(template_id)
						title = t['title']
						if template_id not in curr_template_info.keys():
							need_create_list.append(UserHasTemplateMessages(
								owner_id=user_id,
								template_id=template_id,
								title=title,
								primary_industry=t['primary_industry'],
								deputy_industry=t['deputy_industry'],
								content=t['content'],
								example=t['example']
							))
					for t_id in curr_template_info.keys():  # 如果当前库里的template_id不在获取的信息之中，那么就是商家已删除的
						if t_id not in all_sync_ids:
							need_delete_ids.append(t_id)
					# 删除模板库中的记录
					UserHasTemplateMessages.objects.filter(owner_id=user_id,
																		 template_id__in=need_delete_ids).delete()
					# 同时删除已配置过的模版
					UserTemplateSettings.objects.filter(owner_id=user_id,
																	  template_id__in=need_delete_ids).delete()
					# 新增模版
					UserHasTemplateMessages.objects.bulk_create(need_create_list)
				except:
					print unicode_full_stack()
			else:
				print 'weixin api failed!'

		print 'tms sync end...'

def _get_mpuser_access_token(user):
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return False

	if mpuser_access_token is None:
		return False

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None