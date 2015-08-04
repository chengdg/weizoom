/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 图片自适应等比例缩放高度
*/
$.fn.imageAutoHeight = function(options) {
	var $el = $(this);
	options = options || {};
	options.attr = options.attr || 'auto_height';
	$el.each(function() {
		var defaultScale = '134:112';
		var scale = $(this).attr(options.attr) || defaultScale;
		scale = scale && scale.indexOf(':') > 0 ? scale : defaultScale;
		if(scale) {
			scale = scale.split(':');
			var width = $(this).width();
			$(this).css({
				'height': (width / parseInt(scale[0], 10) * parseInt(scale[1], 10)) + 'px'
			})
		}
	})
};