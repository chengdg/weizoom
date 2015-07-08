# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'
import json
import time
from test import bdd_util
from market_tools.tools.vote.models import *


#######################################################################
# __supplement_vote: 补足一个投票的数据
#######################################################################
def __supplement_vote(vote):
	vote_prototype = {
		"name": u"投票1",
		"detail": u"投票1内容详情",
		"is_non_member": u"可参与",
		"show_style": u"带图片",
		"prize_info": u"积分,10",
		"vote_options": [{
	         "name": u"票项a",
	         "pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
         },{
	         "name": u"票项b",
	         "pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
         }]
	}

	vote_prototype.update(vote)
	return vote_prototype


#######################################################################
# __process_vote_data: 转换一个投票的数据
#######################################################################
def __process_vote_data(vote):
	#处理投票选项
	if 'vote_options' in vote:
		vote['vote_options'] = json.dumps(vote['vote_options'])

	#处理"非会员是否"
	vote["is_non_member"] = 1 if vote["is_non_member"] == u"可参与" else 0

	#处理"展示样式"
	vote["show_style"] = 1 if vote["show_style"] == u"不带图片" else 0

	#处理"奖励"
	prize_infos = vote["prize_info"].split(',')
	if len(prize_infos) > 1:
		if prize_infos[0] == u'积分':
			vote["prize_info"] = u'{"id":%s,"name":"_score-prize_","type":"积分"}' % prize_infos[1]
		elif prize_infos[0] == u'优惠劵':
			vote["prize_info"] = u'{"id":%s,"name":"%s","type":"优惠劵"}' % (2, vote["prize_info"])
		elif prize_infos[0] == u'实物奖励':
			vote["prize_info"] = u'{"id":0,"name":"%s","type":"实物奖励"}' % (prize_infos[1])
	else:
		vote["prize_info"] = u'{"id":-1,"name":"non-prize","type":"无奖励"}'

	#处理"奖项"
	vote_options = json.loads(vote["vote_options"])
	for option in vote_options:
		option_id = -1
		if 'old_name' in option and 'id' in vote:
			option_id = VoteOption.objects.get(vote_id=vote['id'], name=option['old_name']).id

		option['id'] = option_id
	vote["vote_options"] = json.dumps(vote_options)


#######################################################################
# __translate_data_prize_info: 翻译奖数据信息
#######################################################################
def __translate_data_prize_info(award_prize_info):
	data_prize_info = eval(award_prize_info)
	type = data_prize_info['type'].decode('utf8')
	name = data_prize_info['name'].decode('utf8')
	if type == u'积分':
		prize_info = u'积分,%d' % data_prize_info['id']
	elif type == u'实物奖励':
		prize_info = u'实物奖励,%s' % name
	elif type == u'优惠劵':
		prize_info = u'优惠劵,%s' % name
	else:
		prize_info = u'无奖励'
	return prize_info


#######################################################################
# __add_vote: 添加一个投票
#######################################################################
def __add_vote(context, vote):
	vote = __supplement_vote(vote)
	__process_vote_data(vote)
	context.client.post("/market_tools/vote/api/vote/create/", vote)


@when(u"{user}添加微信投票")
def step_impl(context, user):
	client = context.client
	context.votes = json.loads(context.text)
	for vote in context.votes:
		__add_vote(context, vote)


@given(u"{user}已添加'微信投票'")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)

	context.votes = json.loads(context.text)
	for vote in context.votes:
		__add_vote(context, vote)


@then(u"{user}能获取投票列表")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	response = context.client.get('/market_tools/vote/')

	actual_votes = response.context['votes']
	actual_data = []
	for vote in actual_votes:
		actual_data.append({
			"name": vote.name
		})

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_data)


@then(u"{user}能获取投票'{vote_name}'")
def step_impl(context, user, vote_name):
	existed_vote = Vote.objects.get(name=vote_name)

	expected = json.loads(context.text)
	response = context.client.get('/market_tools/vote/update/%d/' % existed_vote.id)
	vote = response.context['vote']

	actual = {
		"name": vote.name,
		"detail": vote.detail,
		"is_non_member": u"可参与" if vote.is_non_member else u"不可参与",
		"show_style": u"不带图片" if vote.show_style else u"带图片",
		"prize_info": __translate_data_prize_info(vote.award_prize_info),
		"vote_options": []
	}
	existed_vote_options = VoteOption.objects.filter(vote=existed_vote).order_by('id')
	for option in existed_vote_options:
		one_option = {
			"name": option.name
		}
		if not vote.show_style:
			one_option['pic_url'] = option.pic_url
		actual["vote_options"].append(one_option)

	bdd_util.assert_dict(expected, actual)


@when(u"{user}修改微信投票")
def step_impl(context, user):
	client = context.client
	context.votes = json.loads(context.text)
	for vote in context.votes:
		__add_vote(context, vote)


@when(u"{user}更新微信投票'{vote_name}'")
def step_impl(context, user, vote_name):
	existed_vote = Vote.objects.get(name=vote_name)

	vote = json.loads(context.text)
	vote['id'] = existed_vote.id
	__process_vote_data(vote)

	context.client.post('/market_tools/vote/api/vote/update/', vote)


@when(u"{user}删除投票'{vote_name}'")
def step_impl(context, user, vote_name):
	vote = Vote.objects.get(name=vote_name)
	url = '/market_tools/vote/delete/%d/' % vote.id
	context.client.get(url)

MEMBER_TOKEN="1122334455"
@given(u"{user}已添加会员")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	webapp_id = context.client.user.profile.webapp_id

	members = json.loads(context.text)

	grade = MemberGrade.get_default_grade(webapp_id)
	Member.objects.all().delete()
	WebAppUser.objects.all().delete()
	for member in members:
		member = Member.objects.create(
			token = MEMBER_TOKEN,
			webapp_id = webapp_id,
			user_icon = '',
			username_hexstr = member['name'],
			grade = grade,
			remarks_name = '',
			is_for_test = True
		)
		WebAppUser.objects.create(
			token = "123",
			webapp_id = webapp_id,
			member_id = member.id
		)


@then(u"{user}查询微信投票'{vote_name}'的票项统计")
def step_impl(context, user, vote_name):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)

	vote = Vote.objects.get(name=vote_name)
	url = '/market_tools/vote/vote_statistics/%d/' % vote.id
	response = context.client.get(url)
	actual_vote_options = response.context['vote_options']

	actual_data = []
	for option in actual_vote_options:
		actual_data.append({
			"name":  option.name,
		    "count": option.vote_count
		})

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_data)


@When(u"会员'{member_name}'在'{vote_name}'中的'{vote_option_name}'项投票")
def step_impl(context, member_name, vote_name, vote_option_name):
	webapp_id = context.client.user.profile.webapp_id

	member = Member.objects.get(webapp_id=webapp_id, token=MEMBER_TOKEN)
	vote = Vote.objects.get(owner=context.client.user, name=vote_name)
	options = VoteOption.objects.filter(vote=vote, name=vote_option_name)
	webapp_user = WebAppUser.objects.get(webapp_id = webapp_id, member_id=member.id)
	if options.count() > 0:
		option = options[0]
		VoteOptionHasWebappUser.objects.create(
			vote_option = option,
			webapp_user = webapp_user
		)
		option.vote_count = option.vote_count + 1
		option.save()



