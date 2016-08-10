import json
from behave import *


@When(u"{user}新建渠道分销二维码")
def step_impl(context, user):
    expected = json.loads(context.text)
