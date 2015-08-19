# -*- coding: utf-8 -*-

__author__ = 'robert'

import shutil
import logging

from prunt.decorator import register_task
import prunt


prunt.init_config({
	"hello": {
		"name": "robert"
	},
	"prunt-concat": {
		"files": {
			"src": [
				"static_v2/js/system/api.js",
				"static_v2/js/system/debug.js"
			],
			"dest": "robert.js"
		},
		"comment": "/* comment */"
	},

	"prunt-md5": {
		"files": {
			"src": [
				"static_v2/js/system/api.js",
				"static_v2/js/system/debug.js"
			]
		}
	},

	"prunt-uglify": {
		"files": {
			"src": [
				"static_v2/js/system/api.js",
				"static_v2/js/system/debug.js"
			]
		}
	},

	"prunt-replace": {
		"files": {
			"src": [
				"static_v2/js/system/dialog2.js"
			]
		},
		"rules": [{
			"pattern": "getTemplate:",
			"replacement": "getRobertTemplate:"
		}, {
			"pattern": "beforeShow:",
			"replacement": "beforeRobertShow:"
		}]
	}
})


@register_task('clean')
def clean(prunt):
	logger = logging.getLogger('clean')
	logger.info('remove dir ./cdn')
	shutil.rmtree('./cdn')


prunt.register_task('build:base_v2', 'weizoom-build', {
	"files": {
		"src": "templates/base_v2.html"
	}
})

prunt.register_task('build:webapp_content_base', 'weizoom-build', {
	"files": {
		"src": "templates/webapp_content_base.html"
	}
})

prunt.register_task('build:webapp_content_base_v4', 'weizoom-build', {
	"files": {
		"src": "templates/webapp_content_base_v4.html"
	}
})


prunt.register_task('default', ['clean', 'build:webapp_content_base_v4'])