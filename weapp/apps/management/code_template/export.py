# -*- coding: utf-8 -*-

#
# 百宝箱
#
APPS_FIRST_NAV = 'apps'
APPS_USER_SURVEY_NAV = 'apps_user_survey'
APPS_LOTTERY_NAV = 'apps_lottery'
APPS_FEEDBACK_NAV = 'apps_feedback'
APPS_ACTIVITY_NAV = 'apps_activity'
APPS_VOTE_NAV = 'apps_vote'

APPS_FEEDBACK_TEST_NAV = 'apps_feedback_test'
APPS_USER_SURVEY_TEST_NAV = 'apps_user_survey_test'
APPS_USER_SURVEY_ITEM_TEST_NAV = 'apps_user_survey_item_test'
APPS_USER_SURVEY_TEXT_TEST_NAV = 'apps_user_survey_text_test'
APPS_NAV = {
    'section': u'百宝箱',
    'navs': [
        {
            'name': APPS_LOTTERY_NAV,
            'title': u'抽奖',
            'url': '/apps2/lottery/',
            'need_permissions': []
        },
        {
            # 对应原来的'complain'
            'name': APPS_FEEDBACK_NAV,
            'title': u'用户反馈',
            'url': '/apps2/feedback/',
            'need_permissions': []
        },
        {
            'name': APPS_USER_SURVEY_NAV,
            'title': u'用户调研',
            'url': '/apps2/user_survey/',
            'need_permissions': []
        },
        {
            'name': APPS_ACTIVITY_NAV,
            'title': u'活动报名',
            'url': '/apps2/activity/',
            'need_permissions': []
        },
        {
            'name': APPS_VOTE_NAV,
            'title': u'微信投票',
            'url': '/apps2/vote/',
            'need_permissions': []
        },
        {
            'name': APPS_FEEDBACK_TEST_NAV,
            'title': u'用户反馈测试数据',
            'url': '/apps2/feedback_test/',
            'need_permissions': []
        },
        {
            'name': APPS_USER_SURVEY_TEST_NAV,
            'title': u'用户调研测试数据',
            'url': '/apps2/user_survey_test/',
            'need_permissions': []
        },
        {
            'name': APPS_USER_SURVEY_ITEM_TEST_NAV,
            'title': u'调研选择题测试数据',
            'url': '/apps2/user_survey_item_test/',
            'need_permissions': []
        },
        {
            'name': APPS_USER_SURVEY_TEXT_TEST_NAV,
            'title': u'调研问答题测试数据',
            'url': '/apps2/user_survey_text_test/',
            'need_permissions': []
        },
    ]
}

def get_apps_second_navs(request):
    if request.user.username == 'manager':
        pass
    else:
        # webapp_module_views.get_modules_page_second_navs(request)
        second_navs = [APPS_NAV]

    return second_navs
