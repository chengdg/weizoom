# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import subprocess

parser = OptionParser()
parser.add_option("--port", dest="port", help="service's port")

options = None

def invoke(command):
	print '***** start output for `%s` *****' % command
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		line = p.stdout.readline()
		if not line:
			break
		print '\t', line
	print '***** finish output for %s *****' % command

def do_register():
	if os.name == 'posix':
		template = './linux.tmpl'
	else:
		template = './windows.tmpl'

	with open(template) as f:
		commands_tmpl = f.read()

	commands = commands_tmpl % {"port": options.port}
	with open('./register_service.sh', 'wb') as f:
		f.write(commands)

	invoke('bash ./register_service.sh')
	print 'success'

def register():
	if '_IS_WEIZOOM_DEV_VM' in os.environ:
		do_register()
	else:
		print 'not in weizoom dev vm, do nothing'

if __name__ == '__main__':
	options, args = parser.parse_args()
	register()