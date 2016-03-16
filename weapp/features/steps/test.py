# -*- coding: utf-8 -*-
import json

from behave import *

from features.steps.behave_utils import set_context_attrs


@when(u"weapp设置context")
def step_impl(context):
	"""
	@type context: behave.runner.Context
	"""
	text = json.loads(context.text)
	set_context_attrs(context, text)