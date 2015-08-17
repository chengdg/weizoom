# -*- coding: utf-8 -*-

__author__ = 'robert'

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

prunt.register_task('build:base_v2', 'weizoom-build', {
	"files": {
		"src": "templates/base_v2.html"
	}
})


prunt.register_task('default', ['build:base_v2'])