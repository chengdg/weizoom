# Django settings for market_tools project.

# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
from market_tools import ToolModule

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
	tool_module.package for tool_module in ToolModule.all_tool_modules()
]

