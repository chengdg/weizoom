
/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 验证器
 */
W.ValidaterClass = function() {
	var ascii = /[^\x00-\xff]/g;

    var getWeiboStyleCotnentLength = function(element) {
        var valueLength;
        var value = $.trim(element.val());
        
        value = value.replace(/[^\x00-\xff]/g, "**");
        
        var reg = /(http:\/\/|https:\/\/)((\w|%|=|\?|\.|\/|&|-|#|:)+)/g;
        var https = value.match(reg);
        if(https != null){
            //处理文中的url链接长度，每个url链接的长度计算为20个长度
            value = value.replace(reg, '');
            httpLength = value.length/2;
            valueLength = httpLength + https.length * 10;
        } else {
            valueLength = value.length/2;
        }
        
        return valueLength;
    };

    var checkDuplicatePattern = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得rule
        xlog(element);
        var rule = element.attr('data-validate-rule');
        xlog(rule);

        //构造url, data
        var url = '/qa/api/pattern/check_duplicate/';
        var data = {
            patterns: value
        }
        if (rule) {
            data['rule'] = rule;
        }

        var result = false;
        var options = {
            type: 'POST',
            url: url,
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_PATTERN) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

    var checkDuplicateQaCategory = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得category
        var category = element.attr('data-validate-category');

        //构造data
        var url = '/qa/api/category/check_duplicate/';
        var data = {
            name: value
        }
        if (category) {
            data['category'] = category;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_QA_CATEGORY) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

    var checkDuplicateActivity = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得activity
        var activity = element.attr('data-validate-activity');

        //构造url
        var url = '/shop/api/activity/check_duplicate/';
        var data = {
            name: value
        }
        if (activity) {
            data['activity'] = activity;
        }

        //构造options
        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_ACTIVITY) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

    var checkDuplicateProductCategory = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得category
        var category = element.attr('data-validate-category');

        //构造url
        var url = '/shop/api/category/check_duplicate/';
        var data = {
            name: value
        }
        if (category) {
            data['category'] = category;
        }

        //构造options
        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_PRODUCT_CATEGORY) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

    var checkDuplicateProduct = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得category
        var product = element.attr('data-validate-product');

        //构造options
        var url = '/shop/api/product/check_duplicate/';
        var data = {
            name: value
        }
        if (product) {
            data['product'] = product;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_PRODUCT) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

    var checkDuplicateMenu = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得menu
        var menu = element.attr('data-validate-menu');

        //构造url
        var url = '/shop/api/menu/check_duplicate/';
        var data = {
            name: value
        }
        if (menu) {
            data['menu'] = menu;
        }

        //构造options
        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_SITE_MENU) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this
        }

        //调用api
        $.ajax(options);

        return result;
    };

	var checkDuplicateMallMenu = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得menu
		var menu = element.attr('data-validate-menu');

		//构造url
		var url = '/mall/api/menu/check_duplicate/';
		var data = {
			name: value
		}
		if (menu) {
			data['menu'] = menu;
		}

		//构造options
		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_SITE_MENU) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

	var checkDuplicateMallActivity = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得activity
		var activity = element.attr('data-validate-activity');

		//构造url
		var url = '/mall/api/activity/check_duplicate/';
		var data = {
			name: value
		}
		if (activity) {
			data['activity'] = activity;
		}

		//构造options
		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_ACTIVITY) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

	var checkDuplicateMallProductCategory = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得category
		var category = element.attr('data-validate-category');

		//构造url
		var url = '/mall/api/category/check_duplicate/';
		var data = {
			name: value
		}
		if (category) {
			data['category'] = category;
		}

		//构造options
		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_PRODUCT_CATEGORY) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

	var checkDuplicateMallProduct = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得category
		var product = element.attr('data-validate-product');

		//构造options
		var url = '/mall/api/product/check_duplicate/';
		var data = {
			name: value
		}
		if (product) {
			data['product'] = product;
		}

		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_PRODUCT) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

	var checkDuplicateCustomerGroup = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得menu
		var group = element.attr('data-validate-group');

		//构造url
		var url = '/customer/api/groups/check_duplicate/';
		var data = {
			name: value
		}
		if (group) {
			data['group'] = group;
		}

		//构造options
		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_CUSTOMER_GROUP) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

	var checkDuplicateQuestionPattern = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}

		//获得rule
		xlog(element);
		var question = element.attr('data-validate-question');
		xlog(question);

		//构造url, data
		var url = '/question/api/pattern/check_duplicate/';
		var data = {
			patterns: value
		}
		if (question) {
			data['question'] = question;
		}

		var result = false;
		var options = {
			type: 'POST',
			url: url,
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_PATTERN) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);
		return result;
	};

    var checkDuplicateScenicspot = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //获得rule
        xlog(element);
        var scenicspot = element.attr('data-validate-scenicspot');
        xlog(scenicspot);

        //构造url, data
        var url = '/tour/api/scenicspot/check_duplicate/';
        var data = {
            name: value
        }
        if (scenicspot) {
            data['scenicspot'] = scenicspot;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_PRODUCT) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };
    
    var checkDuplicateTourBuiltName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var builtName = element.attr('data-validate-activity');
        xlog(builtName);

        //构造url, data
        var url = '/tour/api/built_name/check_duplicate/';
    
        var data = {
            name: value
        }
        if (builtName) {
            data['builtName'] = builtName;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
               if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_ACTIVITY) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

	var noDuplicateCosmeticBuiltName = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}
		//获得rule
		xlog(element);
		var builtName = element.attr('data-validate-page');
		xlog(builtName);

		//构造url, data
		var url = '/cosmetic/api/built_name/check_page_built_name_duplicate/';
		var data = {
			name: value
		}
		if (builtName) {
			data['builtName'] = builtName;
		}

		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_ACTIVITY) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}

		//调用api
		$.ajax(options);

		return result;
	};

    var noDuplicateWineBuiltName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var builtName = element.attr('data-validate-page');
        xlog(builtName);

        //构造url, data
        var url = '/wine/api/built_name/check_page_built_name_duplicate/';
        var data = {
            name: value
        }
        if (builtName) {
            data['builtName'] = builtName;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
               if (data.code == W.SUCCESS) {
                    result = true;
                } else if (data.code == W.ERR_DUPLICATE_ACTIVITY) {
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this            
        }

        //调用api
        $.ajax(options);

        return result;
    };

	var noDuplicateWineProductBuiltName = function(element) {
		//获得value
		var value = element.val();
		if (!value) {
			return true;
		}

		value = $.trim(value);
		if (value.length == 0) {
			return true;
		}
		//获得rule
		xlog(element);
		var id = element.attr('data-validate-product');
		xlog(id);

		//构造url, data
		var url = '/wine/api/product/check_product_built_name_duplicate/';
		var data = {
			builtName: value
		}
		if (id) {
			data['id'] = id;
		}
		var result = false;
		var options = {
			url: url,
			type: 'POST',
			data: data,
			cache: false,
			async: false,
			dataType: 'json',
			success: function(data) {
				if (data.code == W.SUCCESS) {
					result = true;
				} else if (data.code == W.ERR_DUPLICATE_PRODUCT_BUILT_NAME) {
					result = false;
					this.errorHint = data.errMsg;
				}
			},
			error: function(resp) {
				result = false;
			},
			context: this
		}
		//调用api
		$.ajax(options);
		return result;
	};

    var noDuplicateDowningPageBuiltName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var id = element.attr('data-validate-downing-page');
        xlog(id);

        //构造url, data
        var url = '/downing/api/page/check_page_built_name_duplicate/';
        var data = {
            builtName: value
        }
        if (id) {
            data['id'] = id;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else{
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this
        }

        //调用api
        $.ajax(options);

        return result;
    };

     var noDuplicateQrcodeName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var id = element.attr('data-validate-name');
        xlog(id);

        //构造url, data
        var url = '/market_tools/qcrod_channel/api/check_qrcode_name_duplicate/';
        var data = {
            builtName: value
        }
        if (id) {
            data['id'] = id;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else{
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this
        }

        //调用api
        $.ajax(options);

        return result;
    };


    var noDuplicateVoteSettingsName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var id = element.attr('data-validate-name');
        xlog(id);

        //构造url, data
        var url = '/market_tools/vote/api/check_vote_settings_name_duplicate/';
        var data = {
            builtName: value
        }
        if (id) {
            data['id'] = id;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else{
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this
        }

        //调用api
        $.ajax(options);

        return result;
    };
    var noDuplicateActivityName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }
        //获得rule
        xlog(element);
        var id = element.attr('data-validate-name');
        xlog(id);

        //构造url, data
        var url = '/market_tools/activity/api/check_activity_name_duplicate/';
        var data = {
            builtName: value
        }
        if (id) {
            data['id'] = id;
        }

        var result = false;
        var options = {
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data.code == W.SUCCESS) {
                    result = true;
                } else{
                    result = false;
                    this.errorHint = data.errMsg;
                }
            },
            error: function(resp) {
                result = false;
            },
            context: this
        }

        //调用api
        $.ajax(options);

        return result;
    };

	this.validateRules = {
		'int': {
			//整数
			type: 'regex',
            extract: 'value',
			regex: /^\d+$/g,
			errorHint: '格式不正确，请输入整数'
		}, 
		'float': {
			type: 'regex',
            extract: 'value',
			regex: /^\d{1,5}(\.\d{1,2})?$/g,
			errorHint: '格式不正确，请重新输入'
		},
        'price': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,2})?$/g,
            errorHint: '价格不正确，请输入0-99999之间的价格'
        },
		'prize-count': {
			type: 'regex',
			extract: 'value',
			regex: /^\d{1,9}?$/g,
			errorHint: '您只能输入0到999999999之间的整数'
		},
		'date': {
			type: 'regex',
			extract: 'value',
			regex: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/g,
			errorHint: '输入格式为2013-01-01的日期'
		},
		'required-mail': {
			type: 'regex',
			extract: 'value',
			regex:  /^([a-zA-Z0-9]+[_|_|.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|_|.]?)*[a-zA-Z0-9]+\.(?:com|cn)$/g,
			errorHint: '输入有效的E_mail'
		},
		'name': {
			//name: 长度小于100的字符串
			type: 'function',
            extract: 'element',
			check: function(element) {
                var value = $.trim(element.val());
                
                var length = element.attr('data-validate-max-length');
                if (!length) {
                    length = 30;
                } else {
                    length = parseInt(length);
                }

				if(!value.match(/^[\u4E00-\u9FA5A-Za-z0-9_]{1,100}$/)) {
                    this.errorHint = '请输入长度在1到'+length+'之间的字符，只能包含中英文、数字、下划线'
					return false;
				}

				//var asciiReplacedValue = value.replace(ascii, "**");
                var asciiReplacedValue = value;
                xlog('length: ' + asciiReplacedValue.length);
                if(asciiReplacedValue.length < 1 || asciiReplacedValue.length > length) {
                    this.errorHint = '请输入长度在1到'+length+'之间的字符，只能包含中英文、数字、下划线'
                    return false;
				}
				return true;
			},
			errorHint: ''
		},
		'required': {
			type: 'function',
            extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

                var length = element.attr('data-validate-max-length');
                var min = element.attr('data-validate-min-length') || 1;
                if (!length) {
                    length = 50;
                } else {
                    length = parseInt(length);
                }

				if (trimedValue.length < min || trimedValue.length > length) {
                    this.errorHint = '内容长度必须在'+min+'到'+length+'之间，请重新输入';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		'required-none': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				if (trimedValue.length == 0) {
					this.errorHint = '内容不能为空';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		//可以为空，但有字符长度限制
		'can-none-length-limit': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				var length = element.attr('data-validate-max-length');
				var min = element.attr('data-validate-min-length') || 0;
				if (!length) {
					length = 50;
				} else {
					length = parseInt(length);
				}

				if (trimedValue.length == 0) {
					return true;
				}
				if (trimedValue.length < min || trimedValue.length > length) {
					this.errorHint = '内容长度必须在'+min+'到'+length+'之间，请重新输入';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
        'require-select': {
            type: 'function',
            extract: 'value',
            check: function(value) {
                var trimedValue = $.trim(value);
                if (trimedValue.length == 0) {
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: '请选择一个选项'
        },
		'require-select-valid-option': {
			type: 'function',
			extract: 'value',
			check: function(value) {
				var value = parseInt(value);
				if (value < 0) {
					return false;
				} else {
					return true;
				}
			},
			errorHint: '请选择一个选项'
		},
        'require-image': {
            type: 'function',
            extract: 'value',
            check: function(value) {

                if (value.length == 0) {
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: '请选择一张图片'
        },
		'require-video': {
			type: 'function',
			extract: 'value',
			check: function(value) {

				if (value.length == 0) {
					return false;
				} else {
					return true;
				}
			},
			errorHint: '请选择一份视频'
		},
        'required-swip': {
            type: 'function',
            extract: 'element',
            check: function(element) {
               if (element.find('div[id=oneSwipePhoto-div]').length == 0) {
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: '请添加轮播图片'
        },
        'require-swip-image': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                if (element.find('.swipeImagesSelector-oneImage').length == 0) {
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: '请添加轮播图片'
        },
        'required-select-area': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                if (element.find('#searchOption_province').val()==-1 || element.find('#searchOption_city').val()==-1){
                    return false;
                } else{
                    return true
                }
              
            },
            errorHint: '请选择国籍'
        },
        'url': {
            type: 'function',
            extract: 'value',
            check: function(value) {
                var length = 256;
                if (value.length == 0) {
                    this.errorHint = '请输入正确的URL，以http://为前缀';
                    return false;
                }else if (!value.match(/^http(s?):\/\//g)) {
                    this.errorHint = '请输入正确的URL，以http://为前缀';
                    return false;
                }else if (value.length > length) {
                    this.errorHint = '内容长度已超出'+length+'个字符，请去掉'+(value.length - length)+'个字符';
                    return false;
                }else{
                    return true;
                }
            },
            errorHint: '请输入正确的URL，以http://为前缀'
        },
        'customer-url': {
            type: 'function',
            extract: 'value',
            check: function(value) {
                var length = 256;

                if(value!= '' && !value.match(/^http(s?):\/\//g)) {
                    return false;
                } else {
                    if (value.length > length) {
                        this.errorHint = '内容长度已超出'+length+'个字符，请去掉'+(value.length - length)+'个字符';
                        return false;
                    } else {
                        return true;
                    }
                }
            },
            errorHint: '请输入正确的URL，以http://为前缀'
        },
        'selectCheckbox': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var result = false;
                element.find('input[type="checkbox"]').each(function() {
                    if($(this).is(":checked")) {
                        result = true;
                    }
                });
                if(element.find('input[type="checkbox"]').length == 0) {
                    this.errorHint = '请创建分类';
                    return false;
                }else{
                    this.errorHint ='请选择至少一个选项';
                }
                return result;
            },
            errorHint: '请选择至少一个选项'
        },
        'noDuplicatePattern': {
            type: 'function',
            extract: 'element',
            check: checkDuplicatePattern,
            errorHint: ''
        },
        'noDuplicateQaCategory': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateQaCategory,
            errorHint: ''
        },
        'noDuplicateProductCategory': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateProductCategory,
            errorHint: ''
        },
        'noDuplicateProduct': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateProduct,
            errorHint: ''
        },
        'noDuplicateActivity': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateActivity,
            errorHint: ''
        },
        'noDuplicateMenu': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateMenu,
            errorHint: ''
        },
		'noDuplicateCustomerGroup': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateCustomerGroup,
			errorHint: ''
		},
		'noDuplicateMallMenu': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateMallMenu,
			errorHint: ''
		},
		'noDuplicateMallProductCategory': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateMallProductCategory,
			errorHint: ''
		},
		'noDuplicateMallProduct': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateMallProduct,
			errorHint: ''
		},
		'noDuplicateMallActivity': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateMallActivity,
			errorHint: ''
		},
		'noDuplicateQuestionPattern': {
			type: 'function',
			extract: 'element',
			check: checkDuplicateQuestionPattern,
			errorHint: ''
		},
        'noDuplicateScenicspot': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateScenicspot,
            errorHint: ''
        },
        'noDuplicateTourBuiltName': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateTourBuiltName,
            errorHint: ''
        },
        'noDuplicateWineBuiltName': {
            type: 'function',
            extract: 'element',
            check: noDuplicateWineBuiltName,
            errorHint: ''
        },
		'noDuplicateWineProductBuiltName': {
			type: 'function',
			extract: 'element',
			check: noDuplicateWineProductBuiltName,
			errorHint: ''
		},
        'noDuplicateDowningPageBuiltName': {
            type: 'function',
            extract: 'element',
            check: noDuplicateDowningPageBuiltName,
            errorHint: ''
        },
        'noDuplicateQrcodeName': {
            type: 'function',
            extract: 'element',
            check: noDuplicateQrcodeName,
            errorHint: ''
        },
        'noDuplicateVoteSettingsName': {
            type: 'function',
            extract: 'element',
            check: noDuplicateVoteSettingsName,
            errorHint: ''
        },
         'noDuplicateActivityName': {
            type: 'function',
            extract: 'element',
            check: noDuplicateActivityName,
            errorHint: ''
        },
		'noDuplicateCosmeticBuiltName': {
			type: 'function',
			extract: 'element',
			check: noDuplicateCosmeticBuiltName,
			errorHint: ''
		},
        'weiboStyleContent': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var maxLength = element.attr('data-validate-max-length');
                if (!maxLength) {
                    maxLength = 300;
                } else {
                    maxLength = parseInt(maxLength);
                }

                var contentLength = getWeiboStyleCotnentLength(element);

                if (contentLength <= maxLength) {
                    return true;
                } else {
                    this.errorHint = '字数超出限制';
                    return false;
                }
            },
            errorHint: ''
        }
	};

	this.getRule = function(type) {
		return this.validateRules[type];
	}
};

W.Validater = new W.ValidaterClass();

//验证入口
W.validate = function(el, checkDynamicElement) {
	var elements = [];
	if (el) {
		elements.push(el.find('input[data-validate]'))
        elements.push(el.find('textarea[data-validate]'));
        elements.push(el.find('select[data-validate]'));
        elements.push(el.find('div.wx-checkboxGroup[data-validate]'));
        elements.push(el.find('div[data-validate]'));
	} else {
		elements.push($('input[data-validate]'));
        elements.push($('textarea[data-validate]'));
        elements.push($('select[data-validate]'));
        elements.push($('div.wx-checkboxGroup[data-validate]'));
        elements.push($('div[data-validate]'));
	}

	var toggleErrorHint = function(el, isValidate, hint) {
        if (isValidate) {
            xlog('hide error hint: ' + hint);
        } else {
            xlog('show error hint: ' + hint);
        }
		var parent = el.parent();
		var errorHint = parent.find('.errorHint');
		if (errorHint) {
			if (isValidate) {
				errorHint.hide().html('');
			} else {
                var elementHint = errorHint.attr('data-error-hint');
                if (elementHint) {
                    hint = elementHint;
                }
                errorHint.html(hint).show();
			}
		}
	}

    var hasError = false;

    var elementCount = elements.length;
    for (var i = 0; i < elementCount; ++i) {
        var subElements = elements[i];

        subElements.each(function() {
            xlog('------------------ new element ----------------');
            var $el = $(this);
            /*
            if (!$el.is(":visible")) {
                //没有显示的元素，直接返回
                return
            }
            */

            if ($el.attr('data-validate-dynamic') === 'true') {
                if (!checkDynamicElement) {
                    //不检查dynamic类型的输入控件，直接返回
                    return;
                }
            }

            var value = $el.val();
            var validateTypeStr = $el.attr('data-validate');
            if (!validateTypeStr) {
                return;
            }
            xlog('validate type str: ' + validateTypeStr);

            var validateTypes = validateTypeStr.split(',');
            var validateCount = validateTypes.length;
            for (var j = 0; j < validateCount; ++j) {
                var validateType = validateTypes[j];
                xlog('run ' + validateType);
                //执行验证
                var validater = W.Validater.getRule(validateType);
                xlog(validater);
                if (!validater) {
                    continue;
                }
                if (validater.type === 'function') {
                    if (validater.extract == 'element') {
                        value = $el;
                    }

                    if (validater.check.call(validater, value)) {
                        //验证成功
                        xlog('valid');
                        toggleErrorHint($el, true, validater.errorHint);
                    } else {
                        //验证失败
                        hasError = true;
                        xlog('invalid');
                        toggleErrorHint($el, false, validater.errorHint);
                    }
                } else if (validater.type === 'regex') {
                    if (value.match(validater.regex)) {
                        //验证成功
                        xlog('valid');
                        toggleErrorHint($el, true, validater.errorHint);
                    } else {
                        //验证失败
                        hasError = true;
                        xlog('invalid');
                        toggleErrorHint($el, false, validater.errorHint);
                    }
                }
                xlog('====================-----------------------');
                xlog(validater.errorHint);
                if (hasError) {
                    //发现一个错误，跳出循环
                    break;
                }
            }
        });
    }

    return !hasError;
}