# Django settings for viper project.

# -*- coding: utf-8 -*-
import os

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIRS = [
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	'%s/../order/templates' % PROJECT_HOME,
]

INSTALLED_APPS = [
	'order',
	'order.account',
    'order.delivery',
]

MIDDLEWARE_CLASSES = [
	#'order.account.middleware.FreightSessionMiddleware',
]