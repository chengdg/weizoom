# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.contrib.auth.decorators import login_required
from django.conf import settings

from core.jsonresponse import create_response, decode_json_str
from core.exceptionutil import unicode_full_stack
from core import apiview_util
from modules.member import util as member_util

from models import *

from watchdog.utils import watchdog_warning, watchdog_error

@login_required
def get_duplicate_name(request):
	votes = Vote.objects.filter(owner=request.user, name=request.POST['name'])
	if votes.count() > 0:
		response = create_response(601)
		response.errMsg = u'名称重复'
	else:
		response = create_response(200)

	return response.get_response()

@login_required
def create_vote(request):
	created_vote = None
	try:
		vote_options_json_str = request.POST["vote_options"]
		vote_options = decode_json_str(vote_options_json_str)
		is_non_member = int(request.POST.get("is_non_member", 0))

		created_vote = Vote.objects.create(
			owner = request.user,
			name = request.POST["name"].strip(),
			detail = request.POST["detail"].strip(),
			award_prize_info = request.POST['prize_info'].strip(),
			is_non_member = is_non_member,
			show_style = int(request.POST.get('show_style', '1')),
			)
		
		for vote_option in vote_options:
			vote_option = VoteOption.objects.create(
				vote_id = created_vote.id,
				name = vote_option['name'].strip(),
				pic_url = vote_option.get('pic_url', ''),
				)

		response = create_response(200)
		response.data.vote_id = created_vote.id
	except:
		alert_msg = u"创建投票信息失败, cause:\n {}".format(unicode_full_stack())
		watchdog_error(alert_msg, user_id=request.user.id)

		#创建投票选项失败，需要把创建成功的投票选项和投票全部删除
		if created_vote is not None:
			try:
				created_vote.delete()				
			except:
				alert_msg = u"删除投票信息失败, cause:\n {}".format(unicode_full_stack())
				watchdog_warning(alert_msg, user_id=request.user.id)

		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

@login_required
def update_vote(request):
	try:
		vote_options_json_str = request.POST["vote_options"]
		vote_options = decode_json_str(vote_options_json_str)
		is_non_member = int(request.POST.get("is_non_member", 0))

		vote_id = int(request.POST['id'])

		Vote.objects.filter(id=vote_id, owner=request.user).update(
			name = request.POST["name"].strip(),
			detail = request.POST["detail"].strip(),
			award_prize_info = request.POST['prize_info'].strip(),
			is_non_member = is_non_member
			)

		#更新所有投票选项：
		#1. 获取之前库中存在的所有投票选项id集合update_vote_options_ids
		#2. 更新update_vote_options_ids对应的所有投票选项信息
		#3. 删除库中除update_vote_options_ids之外的所有选项
		#4. 创建本次提交的新增的投票选项
		#
		#在操作过程中如果发生异常中断，之前已经进行的操作
		#不会进行恢复
		update_vote_options_ids = []
		new_added_vote_options = []
		for vote_option in vote_options:
			vote_option_id = int(vote_option['id'])
			if vote_option_id == -1: #新创建的
				new_added_vote_options.append(vote_option)
			else: #更新之前的选项
				update_vote_options_ids.append(vote_option_id)
				if len(vote_option.get('pic_url', '')) > 0:
					VoteOption.objects.filter(id=vote_option_id).update(
						name = vote_option['name'].strip(),
						pic_url = vote_option['pic_url'],
						)
				else:
					VoteOption.objects.filter(id=vote_option_id).update(
						name = vote_option['name'].strip(),
						)

		VoteOption.objects.filter(vote_id = vote_id).exclude(id__in = update_vote_options_ids).delete()

		for new_vote_option in new_added_vote_options:
			vote_option = VoteOption.objects.create(
				vote_id = vote_id,
				name = new_vote_option['name'].strip(),
				pic_url = new_vote_option.get('pic_url', ''),
				)

		response = create_response(200)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

# @login_required
# def create_vote_option(request):
# 	try:
# 		vote_option = VoteOption.objects.create(
# 			vote_id = int(request.POST['vote_id']),
# 			name = request.POST['option_name'].strip(),
# 			pic_url = request.POST['pic_url'].strip(),
# 			vote_count = int(request.POST['vote_count'].strip())
# 			)

# 		response = create_response(200)
# 		response.data.option_id = vote_option.id
# 	except:
# 		response = create_response(500)
# 		response.innerErrMsg = unicode_full_stack()

# 	return response.get_response()

# @login_required
# def delete_vote_option(request):
# 	#进行校验，要删除的投票选项的确是当前访问用户所持有
# 	vote_id = int(request.GET['vote_id'])
# 	option_id = int(request.GET['option_id'])

# 	try:
# 		vote = Vote.objects.get(owner=request.user, id=vote_id)
# 	except:
# 		response = create_response(500)
# 		response.errMsg = u'该投票选项所属投票不存在'
# 		response.innerErrMsg = unicode_full_stack()
# 		return response.get_response()

# 	try:
# 		VoteOption.objects.filter(id=option_id, vote_id=vote_id).delete()
# 		response = create_response(200)
# 		return response.get_response()
# 	except:
# 		response = create_response(500)
# 		response.innerErrMsg = unicode_full_stack()
# 		return response.get_response()

# def __update_vote_option(vote_id, vote_option):
# 	VoteOption.objects.filter(vote_id=vote_id, id=vote_option['id']).update(
# 		name = vote_option['name'],
# 		pic_url = vote_option['pic_url'],
# 		vote_count = vote_option['vote_count']
# 		)

# @login_required
# def update_vote_options(request):
# 	try:
# 		#进行校验，要删除的投票选项的确是当前访问用户所持有
# 		vote_id = int(request.POST['vote_id'])

# 		vote_options = decode_json_str(request.POST['options'])
# 		for vote_option in vote_options:
# 			__update_vote_option(vote_id, vote_option)

# 		response = create_response(200)
# 		return response.get_response()
# 	except:
# 		response = create_response(500)
# 		response.innerErrMsg = unicode_full_stack()
# 		return response.get_response()

def __build_member_basic_json(member):
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'integral': member.integral,
		'grade_name': member.grade.name
	}

@login_required
def get_voted_members(request):
	try:
		vote_option_id = int(request.GET['vote_option_id'])

		voted_webapp_users = [relation.webapp_user for relation in \
			VoteOptionHasWebappUser.objects.filter(vote_option_id=vote_option_id)]
		member_ids = [webapp_user.member_id for webapp_user in voted_webapp_users]
		
		voted_members = Member.objects.filter(id__in=member_ids)
		return_voted_members_json_array = []
		for voted_member in voted_members:
			return_voted_members_json_array.append(__build_member_basic_json(voted_member))

		response = create_response(200)
		response.data.items = return_voted_members_json_array
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
	
	return response.get_response()

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)