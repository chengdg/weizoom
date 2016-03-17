# -*- coding: utf-8 -*-
import json

from behave import *

from features.steps.behave_utils import set_context_attrs, get_context_attrs
from test import bdd_util


@when(u"weapp设置context")
def step_impl(context):
	"""
	@type context: behave.runner.Context
	"""
	text = json.loads(context.text)
	set_context_attrs(context, text)

@Then(u"weapp获得context")
def step_impl(context):
	"""
	@type context: behave.runner.Context
	"""
	expected = json.loads(context.text)
	actual = get_context_attrs(context)
	bdd_util.assert_dict(expected, actual)