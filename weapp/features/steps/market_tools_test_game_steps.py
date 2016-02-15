# -*- coding: utf-8 -*-
import json
import time
from test import bdd_util
from market_tools.tools.test_game.models import *
from webapp.models import Workspace


#######################################################################
# __supplement_test_game: 补足一个趣味测试的数据
#######################################################################
def __supplement_test_game(test_game):
	test_game_prototype = {
			"name": u"测试1",
			"background_pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"is_non_member": u"非会员可参与",
			"prize_info": u"积分,10",
			"questions": [{
				"name": u"问题1",
				"index": '1',
				"answers": [{
					"index": "A",
					"name": u"问题1的答案1",
					"score": "0"
				},{
					"index": "B",
					"name": u"问题1的答案2",
					"score": "5"
				}]
			},{
				"name": u"问题2",
				"index": '2',
				"answers": [{
					"index": "A",
					"name": u"问题2的答案1",
					"score": "2"
				},{
					"index": "B",
					"name": u"问题2的答案2",
					"score": "5"
				}]
			}],
			"results": [{
				"index": "1",
				"title": u"评价1",
				"range": "0-5",
				"detail": u"评价详情"
			},{
				"index": "2",
				"title": u"评价2",
				"range": "6-10",
				"detail": u"评价详情"
			}]
		}

	test_game_prototype.update(test_game)
	return test_game_prototype


#######################################################################
# __process_test_game_data: 转换一个投票的数据
#######################################################################
def __process_test_game_data(test_game):
	#处理"非会员是否"
	test_game["is_non_member"] = 1 if test_game["is_non_member"] == u"非会员可参与" else 0

	#处理"奖励"
	prize_infos = test_game["prize_info"].split(',')
	if len(prize_infos) > 1:
		if prize_infos[0] == u'积分':
			test_game["award_prize_info"] = u'{"id":%s,"name":"_score-prize_","type":"积分"}' % prize_infos[1]
		elif prize_infos[0] == u'优惠券':
			test_game["award_prize_info"] = u'{"id":%s,"name":"%s","type":"优惠券"}' % (2, prize_infos[1])
		elif prize_infos[0] == u'实物奖励':
			test_game["award_prize_info"] = u'{"id":0,"name":"%s","type":"实物奖励"}' % (prize_infos[1])
	else:
		test_game["award_prize_info"] = u'{"id":-1,"name":"non-prize","type":"无奖励"}'

	#处理"问题列表"
	questions = test_game["questions"]
	for question in questions:
		key = 'test_game_question_%s' % question["index"]
		test_game[key] = question["name"]
		answers = question["answers"]
		for answer in answers:
			key = 'test_game_answer_score_%s_%s' % (question["index"], answer["index"])
			test_game[key] = answer["score"]
			key = 'test_game_answer_%s_%s' % (question["index"], answer["index"])
			test_game[key] = answer["name"]

	#处理"评价列表"
	results = test_game["results"]
	for result in results:
		key = 'result_name_%s' % result["index"]
		test_game[key] = result["title"]
		min, max = result["range"].split('-')
		key = 'max_score_%s' % result["index"]
		test_game[key] = max
		key = 'min_score_%s' % result["index"]
		test_game[key] = min
		key = 'result_detail_%s' % result["index"]
		test_game[key] = result["detail"]


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
# __add_test_game: 添加一个趣味测试
#######################################################################
def __add_test_game(context, test_game):
	test_game = __supplement_test_game(test_game)
	__process_test_game_data(test_game)
	context.client.post("/market_tools/test_game/test_game/create/", test_game)


@when(u"{user}添加趣味测试")
def step_impl(context, user):
	client = context.client
	context.test_games = json.loads(context.text)
	for test_game in context.test_games:
		__add_test_game(context, test_game)


@given(u"{user}已添加趣味测试")
def step_impl(context, user):
	context.client = bdd_util.login(user)

	context.test_games = json.loads(context.text)
	for test_game in context.test_games:
		__add_test_game(context, test_game)


@then(u"{user}能获取趣味测试列表")
def step_impl(context, user):
	context.client = bdd_util.login(user)
	response = context.client.get('/market_tools/test_game/')

	actual_test_games = response.context['test_games']
	actual_data = []
	for test_game in actual_test_games:
		actual_data.append({
			"name": test_game.name
		})

	expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual_data)


@then(u"{user}能获取趣味测试'{test_game_name}'")
def step_impl(context, user, test_game_name):
	existed_test_game = TestGame.objects.get(name=test_game_name)

	expected = json.loads(context.text)
	response = context.client.get('/market_tools/test_game/test_game/update/%d/' % existed_test_game.id)
	test_game = response.context['test_game']

	actual = {
		"name": test_game.name,
	}

	bdd_util.assert_dict(expected, actual)

@when(u"{user}更新趣味测试'{test_game_name}'")
def step_impl(context, user, test_game_name):
	existed_test_game = TestGame.objects.get(name=test_game_name)

	test_game = json.loads(context.text)
	test_game['id'] = existed_test_game.id
	__process_test_game_data(test_game)

	context.client.post('/market_tools/test_game/test_game/update/%d/' % existed_test_game.id, test_game)


@when(u"{user}删除趣味测试'{test_game_name}'")
def step_impl(context, user, test_game_name):
	test_game = TestGame.objects.get(name=test_game_name)
	url = '/market_tools/test_game/test_game/delete/%d/' % test_game.id
	context.client.get(url)


MEMBER_TOKEN="1122334455"
@given(u"{user}已有会员")
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


MEMBER_TOKEN="1122334455"
@given(u"微信用户")
def step_impl(context):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	webapp_id = context.client.user.profile.webapp_id

	webapp_users = json.loads(context.text)

	grade = MemberGrade.get_default_grade(webapp_id)
	Member.objects.all().delete()
	WebAppUser.objects.all().delete()
	for webapp_user in webapp_users:
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
			member_id = 0
		)


@when(u"{member}参加趣味测试'{test_game_name}'")
def step_impl(context, member, test_game_name):

	client = context.client
	test_game = TestGame.objects.get(name=test_game_name)
	url = '/workbench/jqm/preview/?module=market_tool:test_game&model=test_game&action=get&game_id=%s&woid=%s&fmt=%s' % (test_game.id, context.webapp_owner_id, context.member.token)
	# data = {
	# 	"module": u"market_tool:test_game",
	# 	"model": u"test_game",
	# 	"action": u"get",
	# 	"game_id": test_game.id
	# }
	context.client.get(url)

@when(u"{member}再次参加营销工具趣味测试'{test_game_name}'")
def step_impl(context, member, test_game_name):
	client = context.client
	test_game = TestGame.objects.get(name=test_game_name)
	url = '/workbench/jqm/preview/?module=market_tool:test_game&model=test_game&action=get&game_id=%s&woid=%s&fmt=%s' % (test_game.id, context.webapp_owner_id, context.member.token)
	# data = {
	# 	"module": u"market_tool:test_game",
	# 	"model": u"test_game",
	# 	"action": u"get",
	# 	"game_id": test_game.id,
	# 	"is_again": "1"
	# }
	context.client.get(url)
