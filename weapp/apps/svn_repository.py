# -*- coding: utf-8 -*-

__author__ = 'chuter'

from svn_command import SvnCommand

class SvnRepository(object):
	def __init__(self, repository_path, username, passwd):
		self.svn_command = SvnCommand(repository_path, username, passwd)

	@property
	def version(self):
		if not hasattr(self, '__version'):
			self.__version = self.svn_command.version()

		return self.__version

	def export_to(self, path, r='HEAD'):
		self.svn_command.export_to(path, r)

	def __str__(self):
		return self.repository_path
	