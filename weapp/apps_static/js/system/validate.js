
/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 验证器
 */
(function($, undefined) {

W.ValidaterClass = function() {
	var ascii = /[^\x00-\xff]/g;

	this.validateRules = {
        'require-word': {
            //字母
            type: 'regex',
            extract: 'value',
            regex: /^[^._$]+$/g,
            errorHint: '格式不正确，请输入除".","_"和"$"以外的字符'
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
            regex: /^-?\d+$/g,
            errorHint: '格式不正确，请输入整数'
        },
        'require-positive-int': {
            //正整数
            type: 'regex',
            extract: 'value',
            regex: /^[1-9][0-9]*$/g,
            errorHint: '格式不正确，请输入正整数'
        },
        'require-nonnegative': {
            /*非负数*/
            type: 'regex',
            extract: 'value',
            regex: /^\d+$/g,
            errorHint: '请输入非负整数'
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
        'require-float-one': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,5}(\.\d{0,1})?$/g,
            errorHint: '格式不正确，请输入\'3.147\'或\'5\'这样的数字'
        },
        'require-price': {
            type: 'regex',
            extract: 'value',
            regex: /^\d+(\.\d{0,2})?$/g,
            errorHint: '价格不正确，请输入0-999999999之间的价格'
        },
        'require-date': {
            type: 'regex',
            extract: 'value',
            regex: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/g,
            errorHint: '输入格式为2013-01-01的日期'
        },
        'require-percent': {
            type: 'regex',
            extract: 'value',
            regex: /^([1-9]|[1-9]\d|100)$/g,
            errorHint: '格式不正确，请输入1-100的整数'
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
		'require-notempty': {
			type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
                xwarn('trimed value:' + trimedValue);

				if (trimedValue.length == 0) {
					this.errorHint = '内容不能为空';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
		},
        'require-element-exist': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var selector = element.data('selector');
                if (element.find(selector).length > 0) {
                    return true;
                } else {
                    return false;
                }
            }
        },
        'require-string': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var trimedValue = $.trim(element.val());

                // 支持contenteditable jz
                if(element.attr('contenteditable') == 'true'){
                    trimedValue = element.attr('value');
                }
                var minLength = element.data('minlength') || element.data('min-length')|| 1;
                var maxLength = element.data('maxlength') || element.data('max-length') || 9999999;
                var actualLength = trimedValue.length;
                if (actualLength < minLength || actualLength > maxLength) {
                    if (maxLength == 9999999) {
                        this.errorHint = '输入值长度必须大于等于'+minLength;
                    } else {
                        this.errorHint = '请输入长度在'+minLength+'到'+maxLength+'之间的字符串';
                    }
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
                if (trimedValue.length == 0 || trimedValue === "-1") {
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: '请选择一个选项'
        },
		'require-select-positive-option': {
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
                if (!result.isValidate && !this.errorHint) {
                    this.errorHint = '请在data-validate-function函数中返回errorHint'
                }
            	return result.isValidate;
            }
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
        'require-length': {
            type: 'function',
            extract: 'element',
            check: function(element) {
                var trimedValue = $.trim(element.val());

                // 支持contenteditable jz
                if(element.attr('contenteditable') == 'true'){
                    trimedValue = element.attr('value');
                }
                var strLength = parseInt(element.attr('strlength')) || parseInt(element.attr('str-length'));
                var actualLength = trimedValue.length;
                if (actualLength !== strLength) {
                    this.errorHint = '请输入长度为'+strLength+'的字符串';
                    return false;
                } else {
                    return true;
                }
            },
            errorHint: ''
        },
        'require-countcontrol':{
            type: 'function',
			extract: 'element',
			check: function(element) {
				var trimedValue = $.trim(element.val());
                xwarn('trimed value:' + trimedValue);

                var total_prize_count = parent.window.total_prize_count;
                var prize_title = element.parents('.propertyGroup_property_dynamicControlField_content').find('input[data-field="title"]').val();
                var prize_count = total_prize_count[prize_title]['control_prize_count'];
				if (trimedValue < Number(prize_count)) {
					this.errorHint = '请输入大于'+prize_count+'数字';
					return false;
				} else {
					return true;
				}
			},
			errorHint: ''
        },
        'require-natural': {
            /*非负整数*/
            type: 'regex',
            extract: 'value',
            regex: /^([0]{0,1}|[1-9][0-9]*)$/g,
            errorHint: '请输入非负整数'
        },
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
        if(!el.attr('data-validate')) {
            elements.push(el.find('[data-validate]'));
        } else {
            elements.push(el);
        }
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
            if (!$el.is(":visible") || $el.css('visibility') == 'hidden') {
                if ($el.data('forceValidate')) {
                    //we don't break even the $el is invisible if use force-validate
                } else {
                    W.validate.toggleErrorHint($el, true);
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
                if ('norequire' == validateType && value.length == 0){
                    //hasError = false;
                    W.validate.toggleErrorHint($el, true);
                    break;
                }
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
                if (!validater) {
                    xerror('no validater for rule: ' + validateRule);
                    continue;
                }
                if (validater.type === 'function') {
                	var target = value;
                    var $targetEl = $el;
                    if (validater.extract == 'element') {
                        target = $el;
                    }

                    if (!validater.check.call(validater, target, validateArgs)) {
                    	hasError = true;
                    	errorHint = validateErrorHint ? validateErrorHint : validater.errorHint;
                        W.validate.toggleErrorHint($targetEl, false, errorHint);
						return true;
                    } else {
                        W.validate.toggleErrorHint($targetEl, true);
                    }
                } else if (validater.type === 'regex') {
                    var $targetEl = $el;
                    if (!value.match(validater.regex)) {
                        hasError = true;
                    	errorHint = validateErrorHint ? validateErrorHint : validater.errorHint;
                        W.validate.toggleErrorHint($targetEl, false, errorHint);
						return true;
                    } else {
                        W.validate.toggleErrorHint($targetEl, true);
                    }
                }
                // if (hasError) {
                //     //发现一个错误，跳出循环
                //     break;
                // }
            }
        });
    }

    return !hasError;
}

W.validate.toggleErrorHint = function(el, isValidate, hint) {
    if (isValidate) {
        xlog('hide error hint: ' + hint);
    } else {
        xlog('show error hint: ' + hint);
    }
    if (!el) {
        return;
    }
    var $errorHint = el.siblings('.errorHint');
    if ($errorHint.length == 0) {
        var parent = el.parent();
        $errorHint = parent.find('.errorHint');
    }
    if ($errorHint.length == 0) {
        $errorHint = el.parents('.xa-errorHintContainer').find('.errorHint');
    }
    if ($errorHint.length == 0) {
        $errorHint = el.parents('.x-errorHintContainer').find('.errorHint');
    }
    if ($errorHint.length == 0) {
        var targetSelector = el.data('errorHintTarget');
        if (targetSelector) {
            $errorHint = $(targetSelector);
        }
    }
    if ($errorHint.length > 0) {
        //方式1：寻找与el同级的errorHint区域
        if (isValidate) {
            $errorHint.hide().html('');
        } else {
            var elementHint = $errorHint.data('errorHint');
            if (elementHint) {
                hint = elementHint;
            }
            $errorHint.html(hint).show();
        }
    }
    // 支持contenteditable jz
    if(!isValidate && el.attr('errorhint-value') != undefined){
        el.attr('errorhint-value', hint)
    }

    //显示error hint提示
    var $container = el.parent();
    var isInputEl = (el.get(0).tagName.toLowerCase() === 'input');
    if (isInputEl) {
        //$container.addClass('has-feedback');
        //$container.find('.xa-feedback').remove();
        if (isValidate) {
            $container.removeClass('has-error');
            //$('<span class="xa-feedback glyphicon glyphicon-ok form-control-feedback"></span>').insertAfter(el);
        } else {
            $container.addClass('has-error');
            //$('<span class="xa-feedback glyphicon glyphicon-remove form-control-feedback"></span>').insertAfter(el);
        }
    }
}

$(document).delegate('input[data-validate]', 'blur', function(event) {
        W.validate($(event.currentTarget).parent());
});

})(jQuery);
