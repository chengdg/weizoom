# -*- coding: utf-8 -*-
from behave import *

from test import bdd_util
from features.testenv.model_factory import *
from modules.member.models import MemberGrade


@Then(u"{user}能获取会员等级列表")
def step_impl(context, user):
    json_data = json.loads(context.text)
    response = context.client.get('/mall2/member_grade_list/')
    member_grades = response.context['member_grades']
    response_data = []
    for grade in member_grades:
        data_dict = {}
        data_dict['name'] = grade.name
        data_dict['discount'] = grade.shop_discount
        if grade.is_auto_upgrade:
            data_dict['upgrade'] = u"自动升级"
        else:
            data_dict['upgrade'] = u"手动升级"

        if grade.is_auto_upgrade:
            data_dict["pay_times"] = grade.pay_times
            data_dict["pay_money"] = grade.pay_money
            # data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound
        response_data.append(data_dict)
    for data in json_data:
        if 'upgrade_lower_bound' in data:
            del data['upgrade_lower_bound']

    bdd_util.assert_list(json_data, response_data)


@When(u"{user}添加会员等级")
def step_impl(context, user):
    _add_member_grade(context, user)

@Given(u"{user}添加会员等级")
def step_impl(context, user):
    _add_member_grade(context, user)

def _add_member_grade(context, user):
    json_data = json.loads(context.text)
    response = context.client.get('/mall2/member_grade_list/')
    grades = response.context['member_grades']
    data = []
    name2grade = dict((grade['name'], grade) for grade in json_data)
    old_grade_names = []
    for grade in grades:
        old_grade_names.append(grade.name)
        data_dict = {
            "id": grade.id,
            "name": grade.name,
            "is_auto_upgrade": grade.is_auto_upgrade,
            "shop_discount": grade.shop_discount
        }
        if grade.name in name2grade.keys():
            content = name2grade[grade.name]
            data_dict['is_auto_upgrade'] = (content.get('upgrade', u'手动升级') == u'自动升级')
            data_dict['shop_discount'] = content.get('discount', 10)
        elif grade.is_auto_upgrade:
            data_dict["pay_times"] = grade.pay_times
            data_dict["pay_money"] = grade.pay_money
            data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound

        data.append(data_dict)

    for content in json_data:
        if content['name'] in old_grade_names:
            continue
        if content.has_key('discount') and not content.has_key('shop_discount'):
            content['shop_discount'] = content['discount']
        if content.get('upgrade', '') == u'手动升级':
            content['is_auto_upgrade'] = 0
        else:
            content['is_auto_upgrade'] = 1
        content['id'] = '-1'
        data.append(content)
    context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(data)})


@When(u"{user}删除会员等级'{name}'")
def step_impl(context, user, name):
    response = context.client.get('/mall2/member_grade_list/')
    grades = response.context['member_grades']
    data = []
    for grade in grades:
        if grade.name != name:
            data_dict = {
                "id": grade.id,
                "name": grade.name,
                "is_auto_upgrade": grade.is_auto_upgrade,
                "shop_discount": grade.shop_discount
            }

            if grade.is_auto_upgrade:
                data_dict["pay_times"] = grade.pay_times
                data_dict["pay_money"] = grade.pay_money
                data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound
            data.append(data_dict)

    context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(data)})


@When(u"{user}开启自动升级")
def step_impl(context, user):
    json_data = json.loads(context.text)
    condition = json_data['condition'][0]
    is_all_conditions = '0' if condition == u"满足一个条件即可" else '1'
    response = context.client.get('/mall2/member_grade_list/')
    grades = response.context['member_grades']
    data = []
    for grade in grades:
        data_dict = {
            "id": grade.id,
            "name": grade.name,
            "is_auto_upgrade": grade.is_auto_upgrade,
            "shop_discount": grade.shop_discount
        }

        if grade.is_auto_upgrade:
            data_dict["pay_times"] = grade.pay_times
            data_dict["pay_money"] = grade.pay_money
            data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound
        data.append(data_dict)
    context.client.post('/mall2/api/member_grade_list/?_method=post',
                        {'is_all_conditions': is_all_conditions, 'grades': json.dumps(data)})


@When(u"{user}更新会员等级'{name}'")
def step_impl(context, user, name):
    content = json.loads(context.text)
    response = context.client.get('/mall2/member_grade_list/')
    grades = response.context['member_grades']
    data = []
    for grade in grades:
        if grade.name != name:
            data_dict = {
                "id": grade.id,
                "name": grade.name,
                "is_auto_upgrade": grade.is_auto_upgrade,
                "shop_discount": grade.shop_discount
            }

            if grade.is_auto_upgrade:
                data_dict["pay_times"] = grade.pay_times
                data_dict["pay_money"] = grade.pay_money
                data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound
        else:
            if content['upgrade'] == u'手动升级':
                content['is_auto_upgrade'] = 0
            else:
                content['is_auto_upgrade'] = 1
                content['id'] = grade.id
            content['shop_discount'] = content['discount']
            data_dict = content
        data.append(data_dict)

    context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(data)})


@when(u"{user}更新'{webapp_user_name}'的会员等级")
def step_impl(context, user, webapp_user_name):
    json_data = json.loads(context.text)
    grade_name = json_data['member_rank']
    webapp_id = bdd_util.get_webapp_id_for(user)
    member = bdd_util.get_member_for(webapp_user_name, webapp_id)
    grade = MemberGrade.objects.get(name=grade_name, webapp_id=context.webapp_id)
    data = {
        'type': 'grade',
        'member_id': member.id,
        'checked_ids': grade.id
    }
    context.client.post('/member/api/update_member_tag_or_grade/', data)
