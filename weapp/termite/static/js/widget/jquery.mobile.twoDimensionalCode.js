/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <img src="" data-ui-role="twoDimensionalCode" api="" app="" args="{}" effective-time="">
 * $submitButton.bind('submit', function() {});
 * author: tianyanrong
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.twoDimensionalCode", $.mobile.widget, {
        setting: {
            api: function(_this) {
                return _this.$el.attr('api');
            },
            app: function(_this) {
                return _this.$el.attr('app');
            },
            args: function(_this) {
                return _this._evalJson(_this.$el.attr('args')) || {};
            },
            effectiveTime: function(_this) {
                return parseInt(_this.$el.attr('effective-time'), 10) || 0;
            },
            src: function(_this) {
                return _this.$el.attr('src');
            },
            isUnderDevelop: function() {
                return _this.$el.attr('is-under-develop') ? true : false;
            }
        },
        
        setLoading: function(isShow) {
            this.writeLog('loading的状态:'+isShow);
            if(isShow) {
                this.$parent.addClass('xui-two-dimensional-code-loading');
            }
            else {
                this.$parent.removeClass('xui-two-dimensional-code-loading');
            }
        },
        
		_create : function() {
            this._bind();
			this.$el = this.element;
            this.$el.wrap('<span class="xui-two-dimensional-code-img"></span>');
            this.$parent = this.$el.parent();
            this.effectiveTime = this.setting.effectiveTime(this);
            var imgUrl = this.setting.src(this);
            this.setLoading(true);
            if(!imgUrl) {
                this._fetch();
            }
            else {
                this.writeLog('初始时二维码路径:'+imgUrl);
                this.$el.attr('src', '');
                this.$el.attr('src', imgUrl);
                this._refetch();
            }
            var _this = this;
            this.$el[0].onload = function() {
                _this.setLoading(false);
            }
        },
        
        writeLog: function(msg) {
            
        },
        
        _fetch: function() {
            var _this = this;
            var  member_id = $('#member_id').val();
            if (member_id != '0') { 
                this.writeLog('正在发送二维码API请求');
                W.getApi().call({
                    api: this.setting.api(this),
                    app: this.setting.app(this),
                    args: this.setting.args(this),
                    success: function(data) {
                        _this.writeLog('二维码API请求成功, URL='+data.qcord_url+';失效时间='+data.expired_second);
                        if(data.expired_second) {
                            _this.effectiveTime = data.expired_second;
                        }
                        if(data.qcord_url) {
                            _this.setLoading(true);
                            _this.$el.attr('src', data.qcord_url);
                            _this._refetch();
                        }else {
                            _this._fetch();
                        }
                    },
                    error: function(resp) {
                        _this.writeLog('二维码API请求失败');
                        _this._fetch();
                    }
                });
            }
        },
        
        _refetch: function() {
            var _this = this;
            setTimeout(function() {
                _this._fetch();
            }, (_this.effectiveTime-60)*1000);
        },
        
        _setUneffective: function() {
            var $parent = this.$el.parent();
            this.$error = $parent.find('.tx_error');
            if(this.$error && this.$error.length) {
                //this.$error.show();
            }
            else {
                this.$el.before('<div class="tx_error" style="color:#ff0000; line-height:25px;">该二维码已经失效，请刷新</div>');
            }
        },
        
        _evalJson: function(x) {
            try{
                x = (new Function('return (' + x +')'))();
            }catch(e){
                if('string' === typeof x && x.indexOf('":')){
                    
                }
            }
            return x;
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
		$(":jqmData(ui-role=twoDimensionalCode)", e.target).twoDimensionalCode();
	});
    
})(jQuery);
