# -*- coding: utf-8 -*-

__author__ = 'chuter'

import hashlib



def __get_checksum(data):
	return hashlib.md5(data).hexdigest()

"""
项目中是以gzip来进行定制化APP打包的

"""
#TODO 考虑线程安全性？？
class AppTarball(object):
	def read(self):
		if not hasattr(self, '__read_data'):
			self.__read_data = self._do_read()

		return self.__read_data

	def _do_read(self):
		raise NotImplementedError

	@property
	def checksum(self):
		if not hasattr(self, '_checksum'):
			self._checksum = __get_checksum(self.read())

		return self._checksum

	def write(self, target_path):
		pass

	def unpackage_to(self, target_path):
		pass

	def package_fromfs(self, target_path):
		pass

	def is_the_same(self, that_tarball):
		if that_tarball is None:
			return False

		if not isinstance(that_tarball, AppTarball):
			return False

		return self.checksum == that_tarball.checksum


class RemoteAppTarball(AppTarball):
	def __init__(self, request):
		super(RemoteGzipFile, self).__init__()

		self.request = request

	def _do_read(self):
		file_name = request.POST['Filename']
		file = request.FILES.get('Filedata', None)
		content = []
		if file is not None:
			for chunk in file.chunks():
				content.append(chunk)
			return ''.join(content)
		else:
			return None


class LocalAppTarball(AppTarball):
	def __init__(self, fs_path):
		super(LocalAppTarball, self).__init__()

		self.fs_path = fs_path

	def _do_read(self):
		input_file = gzip.open(self.fs_path, 'rb')
		try:
		    return input_file.read()
		finally:
		    input_file.close()