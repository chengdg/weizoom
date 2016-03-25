# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from apps.models import UserappHasTemplateMessages
from core import resource
from core.jsonresponse import create_response
from django.template import RequestContext
from django.shortcuts import render_to_response
from core.exceptionutil import unicode_full_stack
from utils import url_helper
import models as app_models
from modules.member.models import Member
from mall.order.util import cancel_group_buying
from market_tools.tools.template_message.module_api import send_apps_template_message
from weapp import settings
from modules.member.models import Member, MemberHasSocialAccount

class GroupParticipance(resource.Resource):
	app = 'apps/group'
	resource = 'group_participance'

	def api_put(request):
		"""
		响应PUT
		"""
		try:
			member_id = request.member.id
			group_relation_id = request.POST['group_relation_id']
			fid = request.POST['fid']
			try:
				fid_member = Member.objects.get(id=fid)
			except:
				response = create_response(500)
				response.errMsg = u'不存在该会员'
				return response.get_response()
			group_relation = app_models.GroupRelations.objects(id=group_relation_id, member_id=fid).first()
			if group_relation.group_status == app_models.GROUP_RUNNING:

				#未提交订单，但是跳转过订单页面的情况
				group_detail = app_models.GroupDetail.objects(
					relation_belong_to=group_relation_id,
					owner_id=str(fid),
					grouped_member_id = str(member_id))
				if group_detail.count() > 0 :
					group_detail = group_detail.first()
					if group_detail.order_id != '':
						response = create_response(500)
						response.errMsg = u'只能参与一次'
						return response.get_response()
					else:
						response = create_response(200)
						return response.get_response()
				else:
					response = create_response(200)
					return response.get_response()
					#更新当前member的参与信息
					# total_number = int(group_relation.group_type)
					# sync_result = group_relation.modify(
					# 	query={'grouped_number__lt': total_number},
					# 	inc__grouped_number=1,
					# 	push__grouped_member_ids=str(member_id)
					# )
					# if sync_result:
					# 	try:
					# 		group_detail = app_models.GroupDetail(
					# 			relation_belong_to = group_relation_id,
					# 			owner_id = str(fid),
					# 			grouped_member_id = str(member_id),
					# 			grouped_member_name = request.member.username_for_html,
					# 			created_at = datetime.now()
					# 		)
					# 		group_detail.save()
					# 	except:
					# 		group_relation.update(dec__grouped_number=1,pop__grouped_member_ids=str(member_id))
					# 		response = create_response(500)
					# 		response.errMsg = u'只能参与一次'
					# 		return response.get_response()
					# else:
					# 	response = create_response(500)
					# 	response.errMsg = u'团购名额已满'
					# 	return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'参与失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	def api_post(request):
		"""
		我要开团
		"""
		group_record_id = request.POST['group_record_id']
		member_id = request.POST['fid']
		product_id =  request.POST['product_id']
		group_type = request.POST['group_type']
		group_days = request.POST['group_days']
		group_price = request.POST['group_price']

		#未提交订单，但是跳转过订单页面的情况
		group_relation = app_models.GroupRelations.objects(belong_to=group_record_id,member_id=member_id)
		if group_relation.count() > 0 :
			group_relation_id = group_relation.first().id
			group_detail = app_models.GroupDetail.objects.get(
				relation_belong_to=str(group_relation_id),
				owner_id=str(member_id),
				grouped_member_id = str(member_id))
			if group_detail.order_id != '':
				response = create_response(500)
				response.errMsg = u'只能开团一次'
				return response.get_response()
			else:
				group_relation = group_relation.first()
				if group_relation.group_type != group_type:
					group_relation.update(
						group_type = group_type,
						group_days = group_days,
						group_price = group_price
					)
				relation_belong_to = str(group_relation_id)
				response = create_response(200)
				response.data = {
					'relation_belong_to': relation_belong_to
				}
				return response.get_response()
		else:
			try:
				group_member_info = app_models.GroupRelations(
					belong_to = group_record_id,
					member_id = member_id,
					group_leader_name = request.member.username_size_ten,
					product_id = product_id,
					group_type = group_type,
					group_days = group_days,
					group_price = group_price,
					grouped_number = 1,
					grouped_member_ids = [member_id],
					created_at = datetime.now()
				)
				group_member_info.save()
				data = json.loads(group_member_info.to_json())
				relation_belong_to = data['_id']['$oid']
				group_detail = app_models.GroupDetail(
					relation_belong_to = relation_belong_to,
					owner_id = member_id,
					grouped_member_id = member_id,
					grouped_member_name = request.member.username_size_ten,
					created_at = datetime.now()
				)
				group_detail.save()
				response = create_response(200)
				response.data = {
					'relation_belong_to': relation_belong_to
				}
				return response.get_response()
			except:
				response = create_response(500)
				response.errMsg = u'只能开团一次'
			return response.get_response()


class CancelUnpaidGroup(resource.Resource):
	app = 'apps/group'
	resource = 'cancel_unpaid_group'

	def api_put(request):
		"""
		取消未支付的开团信息
		"""
		group_relation_id = request.POST['group_relation_id']
		member_id = request.POST['member_id']
		order_id = request.POST['order_id']
		try:
			group_relation = app_models.GroupRelations.objects.get(id=group_relation_id)
			group_detail = app_models.GroupDetail.objects.get(relation_belong_to=group_relation_id,grouped_member_id=member_id,is_already_paid=False)
			if order_id:
				cancel_group_buying(order_id)
			if group_relation.member_id == member_id :#如果是团长取消了开团
				group_relation.delete()
				fid = member_id
				group_relation_id = ''
			else:
				group_relation.update(dec__grouped_number=1,pop__grouped_member_ids=str(member_id))
				fid = group_relation.member_id
			group_detail.delete()
			response = create_response(200)
			response.data = {
				'group_relation_id': group_relation_id,
				'fid': fid
			}
		except Exception,e:
			print unicode_full_stack(),e
			response = create_response(500)
			response.errMsg = u'取消操作失败'
		return response.get_response()

class TestGroupTemplate(resource.Resource):
	app = 'apps/group'
	resource = 'test_group_template'


	def api_post(request):
		"""
		测试发送模板消息
		@return:
		"""
		response = create_response(200)
		args = request.POST.get('args', '').split('-')
		member_ids = args[0].split(',')
		status = args[1]
		group = app_models.Group.objects(owner_id=request.manager.id).first()

		result = send_group_template_message({
			"owner_id": request.manager.id,
			"record_id": group.id,
			"group_id": app_models.GroupRelations.objects(belong_to=str(group.id)).first().id,
			"fid": request.manager.id,
			"price": "321.2",
			"product_name": u"测试商品",
			"status" : status,
			"miss": 3
		}, [{"member_id": m, "order_id": 'asdfakljg;l124124'} for m in member_ids])
		if len(result) > 0:
			response = create_response(500)
			response.errMsg = result

		return response.get_response()

def send_group_template_message(activity_info, member_info_list):
	"""
	团购活动发送模板消息
	@param activity_info: 活动信息
		owner_id       登录商家id,
		record_id      (大)团购id,
		group_id	   (小)活动id
		fid			   活动所有者id
		price          团购价格(订单价格),
		product_name   参与团购的商品名称
		status         团购活动的状态: success  fail
		如果 status 是fail
		miss           未下单或未支付的人数

	@param member_info_list: 参与的会员列表
		[{
			member_id		会员id,
			order_id		订单号,

		},...]
	@return: 发送失败的会员id
	"""
	owner_id = int(activity_info['owner_id'])
	status = activity_info['status']
	app_url = 'http://%s/m/apps/group/m_group/?webapp_owner_id=%d&id=%s&group_relation_id=%s&fid=%s' % (settings.DOMAIN, owner_id, str(activity_info['record_id']), activity_info['group_id'], str(activity_info['fid']))
	member_ids = [m['member_id'] for m in member_info_list]
	member_id2openid = {m.member.id: m.account.openid for m in MemberHasSocialAccount.objects.filter(member_id__in=member_ids)}
	#获取模板内容
	um = UserappHasTemplateMessages.objects(owner_id=owner_id, apps_type="group")
	if um.count() <= 0:
		#没有配置过模板消息
		return
	um = um.first()
	template_data = um.data_control
	if not template_data:
		#没有配置过模板消息
		return

	detail_data = dict()
	template_id = ''
	if status == 'success':
		success_data = template_data.get('success', None)
		if not success_data:
			#没有设置拼团成功的模板
			return
		else:
			template_id = success_data['template_id']
			detail_data = {
				"first": u"您参团的商品[%s]已组团成功,%s" % (activity_info['product_name'], success_data['first']),
				"remark": u"点击查看团购活动详情"
			}

	if status == 'fail':
		fail_data = template_data.get('fail', None)
		if not fail_data:
			#没有设置拼团失败的模板
			return
		else:
			template_id = fail_data['template_id']
			detail_data = {
				"first": fail_data['first'],
				"remark": u"点击查看团购活动详情"
			}

	failed_member_ids = []
	for member_info in member_info_list:
		member_id = int(member_info['member_id'])
		if status == 'success':
			detail_data['keywords'] = {
				"keyword1": u"￥%s" % str(activity_info['price']),
				"keyword2": member_info['order_id']
			}
		elif status == 'fail':
			detail_data['keywords'] = {
				"keyword1": member_info['order_id'],
				"keyword2":	activity_info['product_name'],
				"keyword3": u"[差%d人] 成团" % int(activity_info['miss']),
				"keyword4": u"[￥%s] 将在5~7个工作日内完成退款" % str(activity_info['price'])
			}
		if template_id == "" or not template_id:
			#没有配置模板
			continue
		temp_dict = {
			"openid": member_id2openid[member_id],
			"app_url": app_url,
			"template_id": template_id,
			"member_id": member_id,
			"detail_data": detail_data
		}
		result, member_id = send_apps_template_message(owner_id, temp_dict)
		if not result:
			failed_member_ids.append(member_id)
	return failed_member_ids
