
/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 移动环境下的验证器
 */
W.ValidaterClass = function() {
	var ascii = /[^\x00-\xff]/g;

	this.validateRules = {
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
        'require-max-int-value': {
            type: 'function',
			extract: 'element',
			check: function(element, args) {
				var trimedValue = parseInt($.trim(element.val()));
				var maxValue = parseInt(args && args[0]);

				return trimedValue <= maxValue;
			},
			errorHint: ''
        },
        'require-positive-int': {
            //整数
            type: 'regex',
            extract: 'value',
            regex: /^[1-9][0-9]*$/g,
            errorHint: '格式不正确，请输入正整数'
        },
        'require-float': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,2})?$/g,
            errorHint: '格式不正确，请输入\'3.14\'或\'5\'这样的数字'
        },
        'require-float-three': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{1,3})?$/g,
            errorHint: '格式不正确，请输入\'3.147\'或\'5\'这样的数字'
        },
        'require-price': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,9}(\.\d{1,2})?$/g,
            errorHint: '价格不正确，请输入0-999999999之间的价格'
        },
        'require-date': {
            type: 'regex',
            extract: 'value',
            regex: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/g,
            errorHint: '输入格式为2013-01-01的日期'
        },
		'require-tel-phone': {
			type: 'regex',
			extract: 'value',
			regex: /^(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/g,
			errorHint: '输入的电话号码有错误。区号和电话号码之间请用-分割'
		},
		'require-mobile-phone': {
			type: 'regex',
			extract: 'value',
			regex: /^0{0,1}(13[0-9]|15[0-9]|17[0-9]|18[0-9])[0-9]{8}$/g,
			errorHint: '输入正确11位有效的手机号码'
		},
        'require-email': {
            type: 'regex',
            extract: 'value',
            regex: /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/g,
            errorHint: '输入正确的邮箱'
        },
		'require-notempty': {
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
        'require-select-input': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var $selectedInput = element.find('input:checked');
                if ($selectedInput.length > 0) {
                    return true;
                } else {
                    return false;
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
        'require-custom-function': {
            type: 'function',
            extract: 'element',
            check: function(element) {
            	var funcName = element.attr('data-validate-function');
            	var result = window[funcName](element);
            	this.errorHint = result['errorHint'];
            	return result.isValidate;
            }
        }
	};

	this.getRule = function(type) {
		xwarn(type);
		xwarn(this.validateRules);
		return this.validateRules[type];
	}
};

W.Validater = new W.ValidaterClass();

//验证入口
W.validate = function(el, checkDynamicElement) {
	var elements = [];
	if (el) {
		elements.push(el.find('[data-validate]'));
	} else {
		elements.push($('[data-validate]'));
	}

    var hasError = false;
    var elementCount = elements.length;
    var errorHint = null;
    for (var i = 0; i < elementCount; ++i) {
        var subElements = elements[i];
        subElements.each(function() {
            xlog('------------------ new element ----------------');
            var $el = $(this);
            xlog('el name: ' + $el.attr('name'));
            if (!$el.is(":visible")) {
                if ($el.data('force-validate')) {
                    //we don't break even the $el is invisible if use force-validate
                } else {
                    return;
                }
            }

            var value = $el.val();
            var validateTypeStr = $el.attr('data-validate');
            if (!validateTypeStr) {
                return;
            }
            xlog('validate type str: ' + validateTypeStr);

            var validateTypes = validateTypeStr.split(',,');
            var validateCount = validateTypes.length;
            for (var j = 0; j < validateCount; ++j) {
                var validateType = $.trim(validateTypes[j]);
                //validateType最多可能是如下形式: "require-notempty::abcd,, require-func1(a,b)::xyz"
                var items = validateType.split('::');
                var validateRule = null;
                var validateArgs = null;
                var validateErrorHint = null;
                if (items.length === 2) {
                	validateRule = items[0];
                	validateErrorHint = items[1];
                } else {
                	validateRule = items[0];
                }
                //是否有参数
                var pos = validateRule.indexOf('(');
                if (pos !== -1) {
                	items = validateRule.split('(');
                	validateRule = items[0];
                	validateArgs = items[1].substring(0, items[1].length-1).split(',');
                }
                	
                xlog('run ' + validateType);
                //执行验证
                var validater = W.Validater.getRule(validateRule);
                xlog(validater);
                if (!validater) {
                    continue;
                }
                if (validater.type === 'function') {
                	var target = value;
                    if (validater.extract == 'element') {
                        target = $el;
                    }

                    if (!validater.check.call(validater, target, validateArgs)) {
                    	hasError = true;
                    	errorHint = validateErrorHint ? validateErrorHint : validater.errorHint;
                    }
                } else if (validater.type === 'regex') {
                    if (!value.match(validater.regex)) {
                        hasError = true;
                    	errorHint = validateErrorHint ? validateErrorHint : validater.errorHint;
                    }
                }
                if (hasError) {
                    //发现一个错误，跳出循环
                    break;
                }
            }

            return !hasError;
        });
    }

    if (errorHint) {
    	$('body').alert({
            isShow: true,
            info: errorHint,
            isSlide: true,
            speed:2500
        });
    }

    return !hasError;
}