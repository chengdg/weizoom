# -*- coding: utf-8 -*-
import json
import time
import copy
from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from modules.member.models import MemberGrade


@Then(u"{user}能获取会员等级列表")
def step_impl(context, user):
    # if hasattr(context, 'client'):
    #     context.client.logout()
    # context.client = bdd_util.login(user)
    client = context.client
    # user = UserFactory(username=user)
    json_data = json.loads(context.text)
    response = context.client.get('/mall2/member_grade_list/')
    member_grades = response.context['member_grades']
    #context.tc.assertEquals(len(member_grades), len(json_data))
    response_data = []
    for grade in member_grades:
        data_dict = {}
        data_dict['name'] = grade.name
        data_dict['shop_discount'] =  grade.shop_discount
        if grade.is_auto_upgrade:
            data_dict['upgrade'] = u"自动升级"
        else:
            data_dict['upgrade'] = u"手动升级"

        if grade.is_auto_upgrade:
            data_dict["pay_times"] = grade.pay_times
            data_dict["pay_money"] = grade.pay_money
            data_dict["upgrade_lower_bound"] = grade.upgrade_lower_bound
     
        response_data.append(data_dict)

    bdd_util.assert_list(json_data, response_data)


@When(u"{user}添加会员等级")
def step_impl(context, user):
    user = context.client.user
    json_data = json.loads(context.text)
    grades = []
    for content in json_data:
        if content['upgrade'] == u'手动升级':
            content['is_auto_upgrade'] = 0
        else:
            content['is_auto_upgrade'] = 1
        db_grade = MemberGrade.objects.filter(name=content['name'], webapp_id=user.get_profile().webapp_id)
        if len(db_grade) > 0:
            content['id'] = str(db_grade[0].id)
        grades.append(content)
    context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(grades)})


@Given(u"{user}添加会员等级")
def step_impl(context, user):
    context.execute_steps(u"when %s添加会员等级" % user)


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
            print("---------------")
            print(data_dict['name'])
            data.append(data_dict)

    context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(data)})


@When(u"{user}开启自动升级")
def step_impl(context, user):
    # json_data = json.loads(context.text)
    # condition = json_data['condition']
    # is_all_conditions = True if condition == u"满足一个条件即可" else False
    # data = {
    #     'is_all_conditions': is_all_conditions
    # }
    # context.client.post('/mall2/api/member_grade_list/?_method=post', data)
    pass


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
            data_dict = content
        data.append(data_dict)

        context.client.post('/mall2/api/member_grade_list/?_method=post', {'grades': json.dumps(data)})