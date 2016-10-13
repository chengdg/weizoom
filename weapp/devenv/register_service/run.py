# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import json
import subprocess
import socket
import etcd
import json
import sys

parser = OptionParser()
parser.add_option("--port", dest="port", help="service's port")

options = None

def get_local_ip():
	try:
		csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		csock.connect(('8.8.8.8', 80))
		(addr, port) = csock.getsockname()
		csock.close()
		return addr
	except socket.error:
		return "127.0.0.1"

def invoke(command):
	print '***** start output for `%s` *****' % command
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		line = p.stdout.readline()
		if not line:
			break
		print '\t', line
	print '***** finish output for %s *****' % command

def load_config_from_json_file():
	"""
	load config from json file
	"""
	with open('./config.json', 'rb') as f:
		content = f.read()

	base_dir = os.path.join('.', '../..')
	config = json.loads(content)
	locations = []
	if 'locations' in config:
		for location in config['locations']:
			root = os.path.abspath(os.path.join(base_dir, location['root']))
			locations.append("location %s { root %s; }" % (location['path'], root))

	config['locations'] = locations

	return config

def load_config_from_etcd(client, key):
	try:
		content = client.get(key)
		return json.loads(content.value)
	except:
		return None

def load_config(client, key):
	"""
	load config from etcd if etcd has the key
	otherwise, load config from config.json
	"""
	try:
		content = client.get(key)
		print '[register] use existed config from etcd'
		return json.loads(content.value)
	except:
		print '[register] use new config from config.json'
		return load_config_from_json_file()

def load_service_name():
	"""
	load service_name from service.json
	"""
	service_json_path = '../../service.json'
	with open(service_json_path, 'rb') as f:
		content = f.read()
		return json.loads(content)['name']

def register_to_other_service(client, current_service):
	"""
	检查json config中是否有需要添加到其他host的信息, 比如passproxy
	"""
	config = load_config_from_json_file()
	if 'passproxy_locations' in config:
		for passproxy_location in config['passproxy_locations']:
			service_name = passproxy_location['service']
			key = "/service/%s" % service_name
			service_config = load_config_from_etcd(client, key)
			if not service_config:
				print '[register] ERROR: Need service `%s` exists in etcd. But it is NOT EXISTED!!!' % service_name
				sys.exit(1)

			location = "location %s { proxy_pass http://%s; }" % (passproxy_location['path'], current_service)
			if not location in service_config['locations']:
				service_config['locations'].append(location)
			client.set(key, json.dumps(service_config))
			print '[register] add proxypass into %s' % service_name

def do_register():
	client = etcd.Client(host='etcd.weizoom.com')
	service_name = load_service_name()
	key = "/service/%s" % service_name
	config = load_config(client, key)
	host = '%s:%s' % (get_local_ip(), options.port)

	register_to_other_service(client, service_name)

	if '_DEV_IN_WINDOWS' in os.environ:
		#开发时，直接替换host
		config['hosts'] = [host]
	else:
		if not host in config['hosts']:
			config['hosts'].append(host)
	client.set(key, json.dumps(config))

def register():
	do_register()
	#if '_IS_WEIZOOM_DEV_VM' in os.environ:
	#	do_register()
	#else:
	#	print 'not in weizoom dev vm, do nothing'

def check_server_exists(domain_name, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(3)
	try:
		sock.connect((domain_name , port))
		print 'server online'
		return True
	except:
		print 'server offline'
		return False
	finally:
		sock.close()

def check_etcd_exists():
	if not check_server_exists('etcd.weizoom.com', 4001):
		print '[register] WARN: etcd server is not online, service will NOT REGISTERED into etcd!!!'
		return False
	else:
		return True

if __name__ == '__main__':
	if check_etcd_exists():
		options, args = parser.parse_args()
		register()