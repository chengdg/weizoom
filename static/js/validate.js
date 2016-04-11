/*
Copyright (c) 2011-2012 Weizoom Inc
*/
// enhance flux store
(function($, undefined) {
var ValidaterClass = function() {
	var ascii = /[^\x00-\xff]/g;

	this.validateRules = {
        'require-three-number': {
            type: 'regex',
            extract: 'value',
            regex: /^\d{1,3}?$/g,
            errorHint: '格式不正确，请输入3位数'
        },
	};

	this.getRule = function(type) {
		return this.validateRules[type];
	}
};

var validaterObj = new ValidaterClass();

//验证入口
var validate = function(el, checkDynamicElement) {
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
                    toggleErrorHint($el, true);
                    return;
                }
            }

            var value = $el.val();
            var validateTypeStr = $el.data('validate');
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
                    toggleErrorHint($el, true);
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
                var validater = validaterObj.getRule(validateRule);
                if (!validater) {
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
                        toggleErrorHint($targetEl, false, errorHint);
						return true; 
                    } else {
                        toggleErrorHint($targetEl, true);
                    }
                } else if (validater.type === 'regex') {
                    var $targetEl = $el;
                    if (!value.match(validater.regex)) {
                        hasError = true;
                    	errorHint = validateErrorHint ? validateErrorHint : validater.errorHint;
                        toggleErrorHint($targetEl, false, errorHint);
						return true;
                    } else {
                        toggleErrorHint($targetEl, true);
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

var toggleErrorHint = function(el, isValidate, hint) {
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
    console.log(event.currentTarget,"gggggggggggg")
    validate($(event.currentTarget).parent());
});
})(jQuery);