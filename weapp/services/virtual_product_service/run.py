# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import tasks

tasks.deliver_virtual_product(None, None)