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
                var qrcode_image = _this.$el.attr('data-qrcode-image');
                return qrcode_image;
            }
        },
		_create : function() {
			// this.$el = this.element;
            this.qrcode_image = this.setting.getQrcodeImage(this);
            var height = window.screen.height;
            if(this.setting.isShowButton(this)) {
                this.render();
            }
            $('body').append('<div class="xui-mask xa-mask none"><div class="xui-attentionBox"><img class="xui-twoDimensionImg" src="'+this.qrcode_image+'"/></div></div>');
            $('.xui-mask').css({
                height: height,
                width: '100%',
                background:'rgba(0,0,0,0.5)',
                position:'fixed',
                top:0,
                left:0,
                'z-index':10003
            });
            $('.xui-attentionBox').css({
                width: 233,
                height: 270,
                'background':'url(/static_v2/img/termite2/two-dimension.png)',
                'background-size':'100%',
                position:'fixed',
                top:'50%',
                left:'50%',
                'margin-top':'-135px',
                'margin-left':'-115px'
            });
            $('.xui-twoDimensionImg').css({
                width: 148,
                height: 155,
                position:'absolute',
                top:42,
                left:42
            });
        },

        render: function() {
            var height;
            this.$button = $('<a class="xa-guideAttention">关注我们可查看账户积分、红包、优惠券等！</a>');
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
            height = this.setting.isShowCover(this) ? '100%' : '40px';
            this.$el.css('height', height);
        },

        clickGuideAttention :function() {
            $('.xa-mask').removeClass('none');
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
        $('.xui-attentionAlert').click(function(){
            $(this).attentionAlert('clickGuideAttention');
        });
        $('.xa-mask').click(function(){
            $(this).addClass('none');
        });

	})
})(Zepto);