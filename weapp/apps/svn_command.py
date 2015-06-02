# -*- coding: utf-8 -*-

__author__ = 'chuter'


from core.exceptionutil import unicode_full_stack

import subprocess

try:
	import pysvn
	using_pysvn = True
except:
	using_pysvn = False

class SvnCommandError(Exception):
	pass

class SvnCommand(object):
	SVN_INFO_VERSION_TAGSTR = 'revision="'

	def __init__(self, repository_path, username, passwd):
		if repository_path is None or username is None or passwd is None:
			raise Exception("repository_path, username and passwd must be given")

		self.repository_path = repository_path
		self.username = username
		self.passwd = passwd			

	def version(self):
		if using_pysvn:
			#TODO using pysvn ?
			return int(self.__get_version_by_shell())
		else:
			return int(self.__get_version_by_shell())

	def export_to(self, local_path, r='HEAD'):
		if local_path is None:
			return

		if using_pysvn:
			#TODO using pysvn ?
			self.__export_to_by_shell(local_path, r)
		else:
			self.__export_to_by_shell(local_path, r)

	def __get_version_by_shell(self):
		cmd = "svn --username={} --password={} info --non-interactive --xml {}".format(
				self.username,
				self.passwd,
				self.repository_path
			)
		svn_info = self.__run_cmd(cmd)
		try:

			svn_version_start = svn_info.find(self.SVN_INFO_VERSION_TAGSTR)
			svn_version_end = svn_info.find('"', svn_version_start+len(self.SVN_INFO_VERSION_TAGSTR))
			return svn_info[svn_version_start+len(self.SVN_INFO_VERSION_TAGSTR):svn_version_end].strip()
		except:
			raise SvnCommandError(u"解析版本号信息失败，svn info结果:\n{}\n, cause:\n{}"\
					.format(svn_info, unicode_full_stack()))

	def __export_to_by_shell(self, local_path, r):
		assert local_path is not None

		if 'HEAD' == r:
			cmd = "svn --username={} --password={} export --non-interactive --force {} {}".format(
					self.username,
					self.passwd,
					self.repository_path,
					local_path
				)
		else:
			cmd = "svn --username={} --password={} export --non-interactive --force -r {} {} {}".format(
					self.username,
					self.passwd,
					r,
					self.repository_path,
					local_path
				)

		return self.__run_cmd(cmd)


	def __run_cmd(self, cmd):
		converter = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout_and_stderr = converter.communicate()

		if converter.returncode != 0:
			err_msg = stdout_and_stderr[1]
			if err_msg is None:
				err_msg = stdout_and_stderr[0]

			try:
				unicode_err_msg = err_msg.decode('utf-8')
			except:
				unicode_err_msg = err_msg.decode('gbk')

			raise SvnCommandError(u"cmd:{}, error:\n{}".format(
					cmd,
					unicode_err_msg
				))
		else:
			return stdout_and_stderr[0]