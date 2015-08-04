# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sourcefile_manager import SourceFileManager


class Command(BaseCommand):
	help = "merge app to Viper"
	args = '[app name] [viper path]'

	def handle(self, app, viper_path, **options):
		self.app_dir = app
		self.viper_dir = os.path.join(viper_path, app)

		if not os.path.exists(self.viper_dir):
			os.makedirs(self.viper_dir)

		source_file_manager = SourceFileManager(app, viper_path)
		source_file_manager.merge_python_files()
		source_file_manager.copy_html_files()
