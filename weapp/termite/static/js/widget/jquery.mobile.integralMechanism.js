/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <div data-ui-role="integralMechanism" is-hide-share="true"></div>
 * data-key //积分定义的字段名称
 * data-value //积分所需要的数据
 * window.locationHref //方法，重置HREF。加上对积分的支持
 * author: tianyanrong
 */
(function($, undefined) {
    var KEY_NAME, DATA_VALUE;
    window.locationHref = function(href) {
        if(DATA_VALUE) {
            href = href.indexOf('?') >= 0 ? href + '&'+KEY_NAME+'=' + DATA_VALUE : href + '?'+KEY_NAME+'=' + DATA_VALUE;
        }
        window.location.href = href;
    }
	// component definition
	$.widget("mobile.integralMechanism", $.mobile.widget, {
        setting: {
            isHideShare: function() {
                var href = window.location.href;
                var isHasArgs = href.indexOf('?sct=')>=0 || href.indexOf('&sct=')>=0;
                return isHasArgs;
            },
            dataValue: function(_this) {
                return _this.$element.attr('data-value');
            },
            dataKey: function(_this) {
                return _this.$element.attr('data-key');
            }
        },
		_create : function() {
			this.$element = this.element;
            this.setFmt();
        },
        
        writeLog: function(msg) {
            /* if($.writeLog) {
                $.writeLog(msg);
            } */
        },
        
        setFmt: function() {
            var value = this.setting.dataValue(this);
            var key = this.setting.dataKey(this);
            KEY_NAME = key;
            DATA_VALUE = value;
            if(!value) {
                return;
            }
            var _this = this;
            $('a').each(function() {
                var href = this.getAttribute('href');
                var host = window.location.host;
                if(href && (href.match(/^(\.\/|\/)\S/g) || href.indexOf(host) >= 0)) {
                    href = href.indexOf('?') >= 0 ? href + '&'+key+'=' + value : href + '?'+key+'=' + value;
                    this.setAttribute('href', href);
                    _this.writeLog('把按钮"'+$(this).text()+'"的href修改为:'+href);
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
        $('[data-ui-role="integralMechanism"]').integralMechanism();
	});
    
})(jQuery);
