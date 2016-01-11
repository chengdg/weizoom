# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sourcefile_manager import SourceFileManager


class Command(BaseCommand):
	help = "merge a module from Viper app"
	args = '[app name] [module name] [viper path]'

	def handle(self, app, module, viper_path, **options):
		self.app_dir = app
		self.viper_dir = os.path.join(viper_path, app)

		source_file_manager = SourceFileManager(app, viper_path)
		source_file_manager.remove_module_from_python_files(module)
		source_file_manager.remove_module_html_files(module)
