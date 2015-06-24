# -*- coding: utf-8 -*-
__author__ = 'guoliyan'
import json
import time
from test import bdd_util
from apps.customerized_apps.shengjing.models import *

#######################################################################
# __supplement_course: 补足一个课程的数据
#######################################################################
def __supplement_course(course):
    course_prototype = {
        "name": u"1_盛景课程",
        "course_ids": u"3162",
        "course_id_name": u"1_盛景课程",
        "course_date": u"2014-06-16~2014-06-19",
        "detail": u"<p>343434<br/></p>",
        "non_participants": u"非学员可报名"
    }

    course_prototype.update(course)
    return course_prototype

#######################################################################
# __process_shengjing_course: 转换一个报名的数据
#######################################################################
def __process_shengjing_course(course):
    if course['non_participants'] == u'非学员可报名':
        course['non_participants'] = 'on'
    else:
         course['non_participants'] = 'off'



#######################################################################
# __add_shengjing_course: 添加一个课程
#######################################################################
def __add_shengjing_course(context, course):
    course = __supplement_course(course)
    __process_shengjing_course(course)
    url = '/apps/shengjing/?module=study_plan&resource=course&action=create'
    context.client.post(url, course)



@when(u"{user}添加盛景课程")
def step_impl(context, user):
    client = context.client
    context.courses = json.loads(context.text)
    for course in context.courses:
        __add_shengjing_course(context, course)
        time.sleep(1)


@then(u"{user}能获取盛景课程列表")
def step_impl(context, user):
    context.client = bdd_util.login(user)
    client = context.client
    url = '/apps/shengjing/api/study_plan/course_list/get'
    response = client.get(url)
    courses = json.loads(response.content)['data']['items']
    actual_data = []
    for c in courses:
        actual_data.append({
            "name": c['name']
        })

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual_data)

@then(u"{user}能获取课程{course_name}的详情")
def step_impl(context, user, course_name):
    id = ShengjingCourseConfig.objects.get(name=course_name).id
    url = '/apps/shengjing/?module=study_plan&resource=course&action=modify&config_id=%d' % id
    response = context.client.get(url)
    course = response.context['course']
    actual_data = []
    if course.non_participants:
        actual_data.append({"non_participants": u"非学员可报名"})
    else:
        actual_data.append({"non_participants": "off"})

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual_data)

@given(u"{user}已添加'盛景课程'")
def step_impl(context, user):
    if hasattr(context, 'client'):
        context.client.logout()
    context.client = bdd_util.login(user)

    context.courses = json.loads(context.text)
    for course in context.courses:
        __add_shengjing_course(context, course)
        time.sleep(1)


@when(u"{user}删除盛景课程'{course_name}'")
def step_impl(context, user, course_name):
    course = ShengjingCourse.objects.get(name=course_name)
    url = '/apps/shengjing/study_plan/api/course/delete/'
    context.client.get(url, {'id': course.id})
