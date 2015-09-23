/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用示例;
 * <div class="" data-ui-role="notice"></div>
 * weizoom.Notice widget
 */
(function( $, undefined ) {
gmu.define('Notice', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
        var $content = $el.find('.wa-content');

	 	var left = 0;                         // 向左移动的距离
        var width = $el.width();              // 屏幕的宽度
        var widthStartRoll = width * 0.9;     // 滚动临界值
        var contentWidth = $content.width();  // 内容长度

        var startRoll = function($content) {
            window.setInterval(function() {
                if (left == -contentWidth) {
                    left = width;
                }
                else {
                    left = left -1;
                }
                $content.css('left',left);
            },15)  
        };
 
        if (contentWidth == widthStartRoll || contentWidth > widthStartRoll) {
            startRoll($content);
        }

	}
	

});

$(function() {
	$('[data-ui-role="notice"]').each(function() {
		var $notice = $(this);
		$notice.notice();
	});
})
})( Zepto );