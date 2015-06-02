#!python
from subprocess import Popen, PIPE
import shutil
import os
import MySQLdb
import sys

def parse_pid():
    pid_file_path = None

    uwsgi_ini_file = open('./weapp/weapp.ini')
    for line in uwsgi_ini_file:
        if 'pidfile' in line:
            pid_file_path =  line.strip().split('=')[1]
    uwsgi_ini_file.close()

    if uwsgi_ini_file:
        pid_file = open(pid_file_path)
        pid = pid_file.read().strip()
        pid_file.close()
        return pid
    else:
	return -1

def get_running_status():
    buf = ['========== running status ==========']
    pid = parse_pid()

    if not pid:
        print 'failed to get the pid'
        return

    output = Popen('ps aux | grep -v "grep" | grep %s' % pid, stdout=PIPE, shell=True).communicate()[0]
    if output.strip():
        buf.append('running')
    else:
        buf.append('stoped')
	
    return '\n'.join(buf)


def get_ip(domain_name):
    output = Popen('ping %s -c 1' % domain_name, stdout=PIPE, shell=True).communicate()[0]
    if 'unknown host' in output:
        return 'unknown host'
    else:
        beg = output.find('(')
        end = output.find(')', beg)
        return output[beg+1:end]


def get_db_config():
    buf = ['========== db config ==========',]
    shutil.copyfile('./weapp/weapp/settings.py', './settings.py')
    import settings
    buf.append(str(settings.DATABASES))
    host = settings.DATABASES['default']['HOST']
    buf.append('%s: %s' % (host, get_ip(host)))
    os.remove('./settings.py')

    return '\n'.join(buf)


def get_hosts_config():
    hosts = [
    ]

    buf = ['========== hosts config ==========',]
    for host in hosts:
        buf.append('%s: %s' % (host, get_ip(host)))
    return '\n'.join(buf)


def get_version_info():
    buf = ['========== svn info ==========', '***** info *****']
    output = Popen('svn info', stdout=PIPE, shell=True).communicate()[0]
    buf.append(output)
    buf.append('***** log *****')
    output = Popen('svn log -l 2', stdout=PIPE, shell=True).communicate()[0]
    buf.append(output)
    return '\n'.join(buf)


def main():
	type = sys.argv[1]
	if 'simple' == type:
		status = get_running_status().strip()
		pos = status.rfind('=')
		print status[pos+1:].strip()
	elif 'detail' == type:
		items = [get_running_status(), get_db_config(), get_hosts_config(), get_version_info()]
		print '\n\n'.join(items)



if __name__ == '__main__':
	main()
