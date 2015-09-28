# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from weixin2 import export
from core.exceptionutil import unicode_full_stack
from core import resource
from core import paginator
from core.jsonresponse import create_response
from weixin2.models import MessageRemarkMessage,Message,FanCategory,FanHasCategory,Session
from modules.member.models import *
from .util import get_members
from .fans_category import DEFAULT_CATEGORY_NAME

#COUNT_PER_PAGE = 2
COUNT_PER_PAGE = 50
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

#DEFAULT_CATEGORY_NAME=u"未分组"

class Fanses(resource.Resource):
	app = 'new_weixin'
	resource = 'fanses'

	@login_required
	def get(request):
		"""
		获取粉丝列表页面
		"""
		webapp_id = request.user_profile.webapp_id
		# TODO: 缓存粉丝数量
		member_count = Member.objects.filter(webapp_id=webapp_id, is_for_test=False).count()
		has_fans = member_count>0

		# 获取粉丝分组数据
		categories = get_fan_category_list(webapp_id, member_count)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_weixin_second_navs(request),
			'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
			'third_nav_name': export.ADVANCE_MANAGE_FANS_NAV,
			'has_fans': has_fans,
			'categories': categories
		})

		return render_to_response('weixin/advance_manage/fanses.html', c)

	@login_required
	def api_get(request):
		"""
		获取粉丝列表页面

		"""
		# 获取当前页数
		cur_page = int(request.GET.get('page', '1'))
		# 获取每页个数
		#count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		count_per_page = COUNT_PER_PAGE
		# 处理排序
		sort_attr = request.GET.get('sort_attr', '-id')
		# 获取搜索参数
		filter_value = request.GET.get('filter_value', None)

		members = get_members(request, filter_value, sort_attr)
		pageinfo, members = paginator.paginate(members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for member in members:
			try:
				one_member = {}
				one_member['id'] = member.id
				one_member['nickname'] = member.username_for_html
				if MemberInfo.get_member_info(member.id) is None:
					one_member['name'] = ''
				else:
					one_member['name'] = member.member_info.name
				one_member['level'] = member.grade.name
				(subscribe_at_date, subscribe_at_time) = member.created_at.strftime('%Y-%m-%d %H:%M:%S').split(' ')
				one_member['subscribed_at_date'] = subscribe_at_date
				one_member['subscribed_at_time'] = subscribe_at_time
				one_member['profile_img'] = member.user_icon
				one_member['is_subscribed'] = member.is_subscribed
				one_member['session_id'] = member.session_id
				try:
					(at_date, at_time) = Message.objects.get(id=member.last_message_id).created_at.strftime('%Y-%m-%d %H:%M:%S').split(' ')
					one_member['last_chat_at'] = at_date
					one_member['last_chat_at_time'] = at_time
				except:
					one_member['last_chat_at'] = ''
					one_member['last_chat_at_time'] = ''
				items.append(one_member)
			except BaseException as e:
				print('error is:', e)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '-id',
			'data': {}
		}
		return response.get_response()


def get_fan_category_list(webapp_id, total_fan_count=0):
	"""
	获取粉丝列表中的分类信息

	返回结果的格式举例：
	~~~~~~~~~~~~{.c}
	categories = [{
			"id": 0,
			"name": u"全部分组",
			"count": 100,
		}, {
			"id": 1,
			"name": u"未分组",
			"count": 99,
		}, {
			"id": 2,
			"name": u"活跃",
			"count": 2,
		}, {
			"id": 3,
			"name": u"星标组",
			"count": 0
		}]
	~~~~~~~~~~~~

	@todo 增加缓存
	"""
	fan_category_list = FanCategory.objects.filter(webapp_id=webapp_id).order_by("id")
	categories = [{
		"id": -1,
		"name": u"全部分组",
		"count": total_fan_count,
		"is_editable": False,
	}, {
		"id": 0,
		"name": DEFAULT_CATEGORY_NAME,
		"count": 0,
		"is_editable": False,		
	}]
	#print("webapp_id={}".format(webapp_id))
	uncategoried = total_fan_count
	for fan_category in fan_category_list:
		#print("category: {}".format(fan_category))
		# TODO: to be optimized，需要增加缓存
		count = FanHasCategory.objects.filter(category_id=fan_category.id).count()
		categories.append({
			"id": fan_category.id,
			"name": fan_category.name,
			"count": count,
			"is_editable": True,
			})
		uncategoried = uncategoried - count
	categories[1]['count'] = uncategoried
	return categories




class FansMemo(resource.Resource):
	"""
	粉丝备注
	"""
	app = 'new_weixin'
	resource = 'fans_memo'

	@login_required
	def api_post(request):
		"""
		添加粉丝备注名称信息
		"""
		try:
			member_id = request.POST.get('member_id')
			member_remarks = request.POST.get('member_remarks')
			if len(member_remarks) > 20:
				response = create_response(500)
				response.errMsg = u'备注姓名不能超过20字'
			else:
				if MemberInfo.objects.filter(member_id=member_id).count() == 0:
					MemberInfo.objects.create(member_id=member_id, name=member_remarks, sex=0)
				else:
					MemberInfo.objects.filter(member_id=member_id).update(name=member_remarks)
				response = create_response(200)
		except BaseException as e:
				print('error is:', e)
				response = create_response(400)	
		return response.get_response()


class MessageMemo(resource.Resource):
	"""
	消息备注
	"""
	app = 'new_weixin'
	resource = 'msg_memo'

	@login_required
	def api_post(request):
		"""
		添加消息备注名称信息
		"""
		try:
			session_id = request.POST.get('session_id','')
			message_id = request.POST.get('message_id','')	
			message_remark = request.POST.get('message_remark')
			status = request.POST.get('status')
			if session_id == '':
				if MessageRemarkMessage.objects.filter(message_id=message_id).count() == 0:
					MessageRemarkMessage.objects.create(message_id=message_id, owner_id=request.user.id,message_remark=message_remark,status=status)
				else:
					MessageRemarkMessage.objects.filter(message_id=message_id).update(message_remark=message_remark,status=status)
			else:
				session = Session.objects.get(id=session_id)
				session.unread_count = 0
				session.save()
				if MessageRemarkMessage.objects.filter(message_id=message_id).count() == 0:
					MessageRemarkMessage.objects.create(message_id=message_id, owner_id=request.user.id,message_remark=message_remark,status=status)
				else:
					MessageRemarkMessage.objects.filter(message_id=message_id).update(message_remark=message_remark,status=status)
		except BaseException as e:
			print ('error',e)
		return create_response(200).get_response()