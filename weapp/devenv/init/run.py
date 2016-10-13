# -*- coding: utf-8 -*-

import subprocess
import os

def invoke(command):
	print '***** start output for `%s` *****' % command
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		line = p.stdout.readline()
		if not line:
			break
		print '\t', line
	print '***** finish output for %s *****' % command

def run():
	cmd = "behave -k --no-capture -t @full_init"
	invoke(cmd)

if __name__ == '__main__':
	if '_IS_WEIZOOM_DEV_VM' in os.environ:
		run()
		print '[init] done.'
	else:
		print 'not in weizoom dev vm, do nothing'
