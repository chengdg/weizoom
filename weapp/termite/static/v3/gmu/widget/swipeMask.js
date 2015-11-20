/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.SwipeMask widget
 */

 /**  使用说明  **
 * <div data-ui-role="swipemask" class="xa-mask" data-background="rgba(181, 181, 181, .7) data-zIndex="10003"></div>
 *
 * 可选属性：data-background, data-zIndex；
 * 调用方法：(class是自定义的)
 * 			$('.xa-mask').swipeMask('show');
 * 			$('.xa-mask').swipeMask('hide');
 */
(function( $, undefined ) {
gmu.define('SwipeMask', {
	settings: {
		background:function(_this){
			return _this.$el.data('background') ? _this.$el.data('background') : "rgba(0, 0, 0, 0.8)";
		},
		zIndex:function(_this){
			return _this.$el.data('zIndex') ? _this.$el.data('zIndex') : 10000;
		}
	},
	
	_create: function() {
		var $el = this.$el;
        $el.css({
        	"height": "100%",
        	"width": "100%",
        	"background": this.settings.background(this),
        	"display": "none",
        	"z-index": this.settings.zIndex(this),
			"position": "fixed",
			"top": 0,
			"left": 0
        });
		
	},
	show: function(option) {
		this.$el.css({
            'display': 'block'
        });
	},

	hide: function() {
		this.$el.css({
            'display': 'none'
        });
	}
});

$(function() {
	$('[data-ui-role="swipemask"]').each(function() {
		var $swipemask = $(this);
		$swipemask.swipeMask();
	});
})
})( Zepto );