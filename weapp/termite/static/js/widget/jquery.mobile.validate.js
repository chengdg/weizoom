/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <form method="post" action="/m/weapp/edit_ship_info/" data-ui-role="validate" submit-button="#btnSubmit">
 * $submitButton.bind('submit', function() {});
 * author: tianyanrong
 */
(function($, undefined) {
    
    Validate = function(options) {
        this.$el = options.$el;
        this.validate = function(keyName, valideteFn, msg) {
            var isValid = true;
            var msg = msg;
            this.$el.find('['+keyName+']:visible').each(function() {
                isValid = valideteFn($(this));
                if(!isValid) {
                    isValid = false;
                    msg = $(this).attr(keyName+'-msg') || msg;
                    return false;
                }
            });
            return {
                isValid: isValid,
                msg: msg
            };
        };

        var prototype = Validate.prototype;
        var key;
        var result;
        for(key in prototype) {
            if('function' === typeof prototype[key]) {
                result = this[key]();
                if(false === result.isValid) {
                    return result;
                }
            }
        }
        return result;
    }
    Validate.prototype.required = function() {
        return this.validate('required',function($el) {
            if(!$el.val()) {
                return false;
            }else {
                return true;
            }
        }, '请填写此字段');
    };
    Validate.prototype.max = function() {
         return this.validate('max',function($el) {
            var maxValue = parseFloat($el.attr('max'), 10) || 0;
            var value = parseFloat($el.val(), 10) || 0;
            if(value > maxValue) {
                return false;
            }else {
                return true;
            }
        }, '请填写正确的数字');
    };
    Validate.prototype.ple = function() {
         return this.validate('ple',function($el) {
            var ple = parseFloat($el.attr('ple'), 10);
            var value = parseFloat($el.val(), 10) || 0;
            if(value%ple !== 0) {
                return false;
            }else {
                return true;
            }
        }, '请输入正确的数值');
    };
    Validate.prototype.integer = function() {
         return this.validate('integer',function($el) {
            var value = $el.val();
            if(value.match(/\D/)) {
                return false;
            }else {
                return true;
            }
        }, '请输入整数');
    };
    Validate.prototype.cellphone_number = function() {
         return this.validate('cellphone_number',function($el) {
            var value = $.trim($el.val());
            if (value.length != 11) {
                return false;
            }

            if(value.match(/\D/)) {
                return false;
            }else {
                return true;
            }
        }, '请输入正确的手机号');
    };

	// component definition
	$.widget("mobile.validate", $.mobile.widget, {
        _validate: function() {
            this.validateView = new Validate({
                $el: this.$element
            })
            if(false === this.validateView.isValid) {
                $('body').alert({
                    isShow: true,
                    info: this.validateView.msg,
                    speed: 2000
                });
                $(document).trigger('validate-error', this.validateView.msg);
            }
            else {
                this.$element.trigger('validate-success');
            }
            return this.validateView;
        },
		_create : function() {
            this._bind();
			this.$element = this.element;
            this.$submitButton = $(this.$element.attr('submit-button'));
            var _this = this;
            this.$submitButton.click(function() {
                var valid = _this._validate();
                if(false === valid.isValid) {
                    return false;
                }else {
                    _this.$submitButton.trigger('submit');
                }
            });
        },

		_bind : function() {
		},
		
		_unbind : function() {
		},
		
		destroy : function() {
			// Unbind any events that were bound at _create
			this._unbind();

			this.options = null;
		}
	});

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=validate)", e.target).validate();
	});
    
})(jQuery);
