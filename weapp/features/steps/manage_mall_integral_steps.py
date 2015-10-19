# -*- coding: utf-8 -*-
from behave import Given
from test import bdd_util


@Given(u'{webapp_owner_name}给{webapp_user_name}增加{integral_count}积分')
def step_impl(context, webapp_owner_name, webapp_user_name, integral_count):
    url = '/member/api/integral/?design_mode=0&version=1'
    webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
    member_id = bdd_util.get_member_for(webapp_user_name, webapp_id).id
    data = {
        'integral': integral_count,
        'member_id': member_id
    }
    context.client.post(url, data)
