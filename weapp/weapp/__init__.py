# -*- coding: utf-8 -*-
from __future__ import absolute_import

# [Hack Django]

#
# 修改Django RequestContext的默认行为，为request添加context_dict属性
#
from django.template.context import get_standard_processors, RequestContext, Context

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

def enhanced_init(self, request, dict_=None, processors=None, current_app=None, use_l10n=None, use_tz=None):
	Context.__init__(self, dict_, current_app=current_app, use_l10n=use_l10n, use_tz=use_tz)
	if processors is None:
		processors = ()
	else:
		processors = tuple(processors)

	request.context_dict = dict_
	for processor in get_standard_processors() + processors:
		self.update(processor(request))

RequestContext.__init__ = enhanced_init
