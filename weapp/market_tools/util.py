# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os

MARKET_TOOLS_HOME = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(MARKET_TOOLS_HOME, "tools")

def collect_all_market_tool_pathes():
	tool_pathes = []
	for tool_name in os.listdir(TOOLS_DIR):
		if tool_name.startswith("."):
			continue

		tool_path = os.path.join(TOOLS_DIR, tool_name)

		if os.path.isdir(tool_path):
			tool_pathes.append(tool_path)
	return tool_pathes