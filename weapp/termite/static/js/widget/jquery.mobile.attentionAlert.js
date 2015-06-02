/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <div data-ui-role="attentionAlert" is-hide-share="true"></div>
 * data-key //积分定义的字段名称
 * data-value //积分所需要的数据
 * window.locationHref //方法，重置HREF。加上对积分的支持
 * author: tianyanrong
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.attentionAlert", $.mobile.widget, {
        setting: {
            isShowButton: function(_this) {
                return _this.$el.attr('data-is-show-button') ? true : false;
            },
            isShowCover: function(_this) {
                return _this.$el.attr('data-is-show-cover') ? true : false;
            },
            getUrl: function(_this) {
                var url = _this.$el.attr('data-url');
                url = url.replace(/(^\s*)|(\s*$)/g,'');
                return url;
            }
        },
		_create : function() {
			this.$el = this.element;
            this.url = this.setting.getUrl(this);
            if(this.setting.isShowButton(this)) {
                this.render();
            }
        },
        
        render: function() {
            var url = this.url;
            var height;
            if(this.url) {
                this.$button = $('<a href="'+url+'">关注我们可查看账户积分、红包、优惠券等！<i class="xui-icon xui-icon-rightarrow"></i></a>');
                this.$el.html(this.$button);
                height = this.setting.isShowCover(this) ? '100%' : '60px';
            }
            else {
                height = this.setting.isShowCover(this) ? '100%' : '0px';
            }
            this.$el.css('height', height);
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
        $('[data-ui-role="attentionAlert"]').attentionAlert();
	});
    
})(jQuery);
