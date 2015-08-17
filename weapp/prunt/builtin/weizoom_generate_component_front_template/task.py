# -*- coding: utf-8 -*-

__author__ = 'robert'

import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

import logging
logger = logging.getLogger('weizoom-generate-component-front-template')

from prunt.decorator import register_task
from prunt.util import template_util
import prunt


@register_task('weizoom-generate-component-front-template')
def weizoomGenerateComponentFrontTemplate(prunt):
	u"""
	将component的模板文件转换为前端使用的handlebar模板
	"""
	from utils import component_template_util
	components_dir = 'termite/static/termite_js/app/component/wepage'
	logger.info('convert component template in "%s" to handlebar template', components_dir)
	handlebar_template = component_template_util.generate_handlebar_template(components_dir)
	prunt.set_last_result(handlebar_template)