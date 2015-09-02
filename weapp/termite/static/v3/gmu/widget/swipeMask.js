/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.SwipeMask widget
 */
(function( $, undefined ) {
gmu.define('SwipeMask', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
		//确定蒙版区域的宽高
        var height = window.document.body.clientHeight;
        var width = window.document.body.clientWidth; 
        console.log(width,'width')
        console.log(height,'width')
        $el.find('.mask').css({
        	"height": height,
        	"width": width,
        	"background":"rgba(181, 181, 181, 0.3)",
        	"display": "none",
        	"z-index": 10000,
			"position": "absolute",
			"top": 0
        });
		
	},
	show: function() {
		this.$el.find('.mask').css({
            'display': 'block'
        });
	},

	hide: function() {
		this.$el.find('.mask').css({
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