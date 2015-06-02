
/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 验证器
 */
 //TODO 支持自定义校验方法 chuter
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

    var checkDuplicateVoteName = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //构造url, data
        var url = '/market_tools/vote/api/duplicate_name/get/';
        var data = {
            name: value
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
        var rule = element.attr('data-validate-rule');

        //构造url, data
        var url = '/weixin/message/qa/api/pattern/check_duplicate/';
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

    var checkCouponNameDuplicatePattern = function(element) {
        //获得value
        var value = element.val();
        if (!value) {
            return true;
        }

        value = $.trim(value);
        if (value.length == 0) {
            return true;
        }

        //构造url, data
        var url = '/mall/api/coupon/check_name_duplicate/';
        var data = {
            name: value
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

	this.validateRules = {
		'int': {
			//整数
			type: 'regex',
			extract: 'value',
			regex: /^\d+$/g,
			errorHint: '格式不正确，请输入整数'
		},
        'require-letter': {
            //字母
            type: 'regex',
            extract: 'value',
            regex: /^[a-zA-Z0-9_]+$/g,
            errorHint: '格式不正确，请输入字母、数字、下划线'
        },
		'require-int': {
            //整数
            type: 'regex',
            extract: 'value',
            regex: /^\d+$/g,
            errorHint: '格式不正确，请输入整数'
        },
        'require-int-in-radio': {
            //整数
            type: 'function',
            extract: 'element',
			check: function(element) {
				var regex = /^\d+$/g;
                var value = $.trim(element.val());

                var $radio = element.parents('label').find('input[type="radio"]');
                if ($radio.length > 0 && $radio.is(':checked')) {
                	if (value.match(regex)) {
    	            	return true;
	                } else {
	                	return false;
	                }
                }

                return true;
			},
			errorHint: '格式不正确，请输入整数'
        },
        'require-positive-int': {
            //整数
            type: 'regex',
            extract: 'value',
            regex: /^[1-9][0-9]*$/g,
            errorHint: '格式不正确，请输入正整数'
        },
		'float': {
			type: 'regex',
            extract: 'value',
			regex: /^\d{1,5}(\.\d{1,2})?$/g,
			errorHint: '格式不正确，请重新输入'
		},
        // 'require-float-not-zero': {
        //     type: 'regex',
        //     extract: 'value',
        //     regex: /^\d{1,5}(\.\d{1,2})?$/g,
        //     errorHint: '格式不正确，请输入\'3.14\'或\'5\'这样大于0的数字'
        // },
        'require-float': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,2})?$/g,
            errorHint: '格式不正确，请输入\'3.14\'或\'5\'这样的数字'
        },
         'require-float-one': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,1})?$/g,
            errorHint: '格式不正确，请输入\'3.1\'或\'5\'这样的数字'
        },
        'require-float-three': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,3})?$/g,
            errorHint: '格式不正确，请输入\'3.147\'或\'5\'这样的数字'
        },
        'price': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,2})?$/g,
            errorHint: '价格不正确，请输入0-99999之间的价格'
        },
        'require-price': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,9}(\.\d{1,2})?$/g,
            errorHint: '价格不正确，请输入0-999999999之间的价格'
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
        'required-date': {
            type: 'regex',
            extract: 'value',
            regex: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/g,
            errorHint: '输入格式为2013-01-01的日期'
        },
		'required-tel-phone': {
			type: 'regex',
			extract: 'value',
			regex: /^(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/g,
			errorHint: '输入的电话号码有错误。区号和电话号码之间请用-分割'
		},
		'required-tel-zone': {
			type: 'regex',
			extract: 'value',
			regex: /^0\d{2,3}$/g,
			errorHint: '区号有误'
		},
		'required-tel-num': {
			type: 'regex',
			extract: 'value',
			regex: /^[1-9][0-9]{6,7}$/g,
			errorHint: '输入正确7至8位的电话号码'
		},
		'required-mobile-phone': {
			type: 'regex',
			extract: 'value',
			regex: /^0{0,1}(13[0-9]|15[3-9]|15[0-2]|18[0-9])[0-9]{8}$/g,
			errorHint: '输入正确11位有效的手机号码'
		},
        'required-location': {
            type: 'regex',
            extract: 'value',
            regex:  /^(-?((180)|(((1[0-7]\d)|(\d{1,2}))(\.\d+)?))),(-?((90)|((([0-8]\d)|(\d{1}))(\.\d+)?)))$/g,
            errorHint: '输入正确经纬度。经度和纬度要用,隔开'
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
				var is_has_special = element.attr('data-validate-enable-special') || true;
				if (is_has_special==='false') {
					is_has_special = false;
				} else {
					is_has_special = true;
				}
				if (! is_has_special){
					if(!trimedValue.match(/^[\u4E00-\u9FA5A-Za-z0-9]{1,100}$/)) {
                    	this.errorHint = '只能包含中英文、数字';
						return false;
					}
				}
                var length = element.attr('data-validate-max-length');
                var min = element.attr('data-validate-min-length') || 1;
                if (!length) {
                    length = 50;
                } else {
                    length = parseInt(length);
                }
				if (trimedValue.length < min || trimedValue.length > length) {
                    this.errorHint = '内容长度必须在'+min+'到'+length+'之间，请重新输入';
                    if (min==length){
                    	this.errorHint = '内容长度必须为'+min+'，请重新输入';
                    }
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		'require-float-not-zero': {
			type: 'function',
            extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
                if (trimedValue.length == 0 || trimedValue == 0) {
                	this.errorHint = '格式不正确，请输入\'3.14\'或\'5\'这样大于0的数字';
                	return false;
            	}
				if(!trimedValue.match(/^\d{1,5}(\.\d{1,2})?$/)) {
                	this.errorHint = '格式不正确，请输入\'3.14\'或\'5\'这样大于0的数字';
					return false;
				}else{
					return true;
				}
			},
			errorHint: ''
		},
		'cannot-contains': {
			type: 'function',
            extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

                var charactersCatStr = element.attr('data-validate-not-contain-characters');
                if (charactersCatStr.length > 0) {
                	var characters = charactersCatStr.split(',');
		            var charactersCount = characters.length;
		            for (var j = 0; j < charactersCount; ++j) {
		                var character = characters[j];
		                if (trimedValue.indexOf(character) > -1) {
		            		this.errorHint = "内容中不能包含"+character+",请重新输入";
							return false;
		                }
		            }
		            return true;
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
		'required-percentage': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
				var re = /^\d+$/g;
				var is_int = re.test(trimedValue);
				if (! is_int){
					return false;
				}
				try {
					var value = parseInt(trimedValue)
					if (value >=0 && value <= 100) {
						return true;
					} else {
						return false;
					}
				} catch(e) {
					return false;
				}
			},
			errorHint: '请输入0到100之间的整数（不包括0和100）'
		},
		'required-percentage-2': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
				var re = /^\d+$/g;
				var is_int = re.test(trimedValue);
				if (! is_int){
					return false;
				}
				try {
					var value = parseInt(trimedValue)
					if (value >=0 && value <= 100) {
						return true;
					} else {
						return false;
					}
				} catch(e) {
					return false;
				}
			},
			errorHint: '请输入0到100之间的整数'
		},
		'int-range': {
			type: 'function',
            extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
				var re = /^\d+$/g;
				var is_int = re.test(trimedValue);
				trimedValue.replace()
                var max = element.attr('data-validate-max') || 10000;
                var min = element.attr('data-validate-min') || 1;
                if (! is_int){
					this.errorHint = '请输入'+min+'到'+max+'之间的整数';
					return false;
				}
               try {
					var value = parseInt(trimedValue)
					if (value >=min && value <= max) {
						return true;
					} else {
						this.errorHint = '请输入'+min+'到'+max+'之间的整数';
						return false;
					}
				} catch(e) {
					this.errorHint = '请输入'+min+'到'+max+'之间的整数';
					return false;
				}
			},
			errorHint: ''
		},
		'required-percentage-not-border': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
				var re = /^\d+$/g;
				var is_int = re.test(trimedValue);
				if (! is_int){
					return false;
				}
				try {
					var value = parseInt(trimedValue)
					if (value >0 && value <= 100) {
						return true;
					} else {
						return false;
					}
				} catch(e) {
					return false;
				}
			},
			errorHint: '请输入0到100之间的整数（不包括0）'
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
		//可以为空，但有必须是价格
		'can-none-price': {
			//整数
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				if (trimedValue.length == 0) {
					return true;
				}
				if (!trimedValue.match(/^\d{1,9}(\.\d{1,2})?$/g)) {
					this.errorHint = '价格不正确，请输入0-999999999之间的价格';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		//可以为空，但有必须是整数
		'can-none-int': {
			//整数
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				if (trimedValue.length == 0) {
					return true;
				}
				if (!trimedValue.match(/^\d+$/g)) {
					this.errorHint = '格式不正确，请输入整数';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		//可以为空，但有必须是手机号
		'can-none-mobile-phone': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				if (trimedValue.length == 0) {
					return true;
				}
				if (!trimedValue.match(/^0{0,1}(19[0-9]|13[0-9]|15[3-9]|15[0-2]|18[0-9])[0-9]{8}$/g)) {
					this.errorHint = '输入正确11位有效的手机号码';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
		//qq号码
		'qq-number': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());

				if (trimedValue.length == 0) {
					return true;
				}
				if (!trimedValue.match(/^[0-9]{5,11}$/g)) {
					this.errorHint = '输入正确的QQ号码';
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
                } else if (value === '[]') {
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
		'require-file': {
			type: 'function',
			extract: 'value',
			check: function(value) {

				if (value.length == 0) {
					return false;
				} else {
					return true;
				}
			},
			errorHint: '请选择一份文件'
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
        'required-date-picker': {
        	type: 'function',
            extract: 'element',
            check: function(element) {
            	var regex = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/g;
            	var $inputs = element.find('[data-ui-role="date-picker"]');
            	for (var i = 0; i < $inputs.length; ++i) {
            		var $input = $inputs.eq(i);
            		var value = $.trim($input.val());
            		if (!value.match(regex)) {
            			return false;
            		}
            	}
            	return true;
            },
            errorHint: '请选择日期'
        },
        'required-custom-function': {
            type: 'function',
            extract: 'element',
            check: function(element) {
            	var funcName = element.attr('data-validate-function');
            	var result = window[funcName](element);
            	this.errorHint = result['errorHint'];
            	return result.isValidate;
            }
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
        'selectRadio': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var result = false;
                element.find('input[type="radio"]').each(function() {
                    if($(this).is(":checked")) {
                        result = true;
                    }
                });
                if(element.find('input[type="radio"]').length == 0) {
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
        'noDuplicateVoteName': {
            type: 'function',
            extract: 'element',
            check: checkDuplicateVoteName,
            errorHint: ''
        },
        'noDuplicateMallCouponName': {
            type: 'function',
            extract: 'element',
            check: checkCouponNameDuplicatePattern,
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
        var errorHint = el.siblings('.errorHint');
        if (errorHint.length == 0) {
	        var parent = el.parent();
			errorHint = parent.find('.errorHint');
        }
        if (errorHint.length == 0) {
            errorHint = el.parents('.x-errorHintContainer').find('.errorHint');
        }
        if (errorHint.length == 0) {
            errorHint = el.parents('.xa-errorHintContainer').find('.errorHint');
        }
		if (errorHint.length > 0) {
            //方式1：寻找与el同级的errorHint区域
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
            xlog('el name: ' + $el.attr('name'));
            /*
            if ($el.attr('data-ignore-validate') === 'true') {
            	xlog('ignore validate because of data-ignore-validate')
            	return;
            }
            */
            if (!$el.is(":visible")) {
                //没有显示的元素，直接返回
                if ($el.attr('data-validate') === 'require-image' || $el.attr('data-validate') === 'require-file') {
                	if ($el.parent().is(':visible')) {
                		//image不可见，但image的父元素可见，意味着需要使用上传图片控件
                	} else {
                		//image的父元素不可见，意味着整体不可用
                		return;
                	}
                } else {
                	return;
                }
            }

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
                	var target = value;
                    if (validater.extract == 'element') {
                        target = $el;
                    }

                    if (validater.check.call(validater, target)) {
                        //验证成功
                        toggleErrorHint($el, true, validater.errorHint);
                    } else {
                        //验证失败
                        hasError = true;
                        toggleErrorHint($el, false, validater.errorHint);
                    }
                } else if (validater.type === 'regex') {
                    if (value.match(validater.regex)) {
                        //验证成功
                        toggleErrorHint($el, true, validater.errorHint);
                    } else {
                        //验证失败
                        hasError = true;
                        xlog('invalid');
                        toggleErrorHint($el, false, validater.errorHint);
                    }
                }
                if (hasError) {
                    //发现一个错误，跳出循环
                    break;
                }
            }
        });
    }

    return !hasError;
}
