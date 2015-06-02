# -*- coding: utf-8 -*-

__author__ = 'chuter'

"""
检测是否需要进行处理
目前只检测对应的系统用户是否已经解绑
如果解绑，那么不再处理收到的针对该系统用户的消息
"""
class ShouldProcessChecker(object):
	def pre_processing(self, context, is_from_simulator=False):
		if not context.user_profile.is_mp_registered:
			context.should_process = False