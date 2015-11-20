/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.AttentionAlert widget
 */
 (function($, undefined) {
	// component definition
	gmu.define('AttentionAlert', {
        setting: {
            isShowButton: function(_this) {
                return _this.$el.data('is-show-button') ? true : false;
            },
            isShowCover: function(_this) {
                return _this.$el.data('is-show-cover') ? true : false;
            },
            getDataId: function(_this) {
                var id = _this.$el.data('id');
                return id;
            },
            getQrcodeImage: function(_this) {
                var qrcode_image = _this.$el.data('qrcode-image');
                return qrcode_image;
            }
        },
		_create : function() {
            this.qrcode_image = this.setting.getQrcodeImage(this);
            var height = window.screen.height;
            if('True' === this.$el.data('varnish')){
                this.$el.data('view', this);
            }else if(this.setting.isShowButton(this)) {
                this.render();
            }
        },

        render: function() {
            this.$button = $('<a class="wa-guideAttention">关注我们可查看账户积分、红包、优惠券等！</a>');
            this.$el.html(this.$button);
            if($('.xa-page')){
                $('.xa-page').css('padding-top','40px');
            }
            if($('.wa-page')){
                $('.wa-page').css('padding-top','40px');
            }
            //编辑订单页的布局因为配合iscroll滚动所以使用了绝对定位脱离了page，因而单独处理
            if($('xa-editOrderPage')){
                $('#wrapper').css('top','40px');
            }
            var height = this.setting.isShowCover(this) ? '100%' : '40px'
            this.$el.css('height', height);
            $('body').append('<div data-ui-role="swipemask" class="xa-qrcodeMask" data-background="rgba(0,0,0,.5)"><div class="wui-attentionBox"><img class="wui-twoDimensionImg" src="'+this.qrcode_image+'"/></div></div>');

            $('.xa-qrcodeMask').swipeMask().bind('click', function(event) {
                $(this).attentionAlert('clickMask');
            });

        },

        clickGuideAttention :function() {
            $('.xa-qrcodeMask').swipeMask('show');
        },
        clickMask: function(){
            $('.xa-qrcodeMask').swipeMask('hide');
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
	$(function() {
    	$('[data-ui-role="attentionAlert"]').each(function() {
    		$(this).attentionAlert();
    	});
        $('.wui-attentionAlert').click(function(){
            $(this).attentionAlert('clickGuideAttention');
        });
<<<<<<< HEAD
        // $('.xa-qrcodeMask').bind('click', function(event) {
        //     $(this).attentionAlert('clickMask');
        // });
        // $('body').delegate('.xa-qrcodeMask', 'click', function(event) {
        //     $(this).attentionAlert('clickMask');
        
        // });

=======
>>>>>>> f_mall_6096
	})
})(Zepto);