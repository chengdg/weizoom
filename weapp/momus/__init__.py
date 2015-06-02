# -*- coding: utf-8 -*-

import sys
import momus.restart_server

if sys.argv[0] == 'manage.py' and sys.argv[1] == 'runserver':
	from django.conf import settings
	from momus.loader import loader
	loader.load_to(settings.ROOT_URLCONF)
else:
	print 'DO NOT load momus file when execute command'
	
