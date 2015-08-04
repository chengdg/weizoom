/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 图片自适应等比例缩放高度
*/
(function() {
var alertTimeoutValue = null;
$.fn.alert = function(options) {
	var $el = $(this);
	var $alert = $el.find('.tx_alert');
	if(alertTimeoutValue) {
		clearTimeout(alertTimeoutValue);
		alertTimeoutValue = null;
	}
	
	if(options.isShow === false) {
		$alert.hide();
		return;
	}
	
	if(!$alert.length) {
		$el.append('<div class="loding loading tx_alert" name="loading" style="display:none;"><span>加载中...</span></div>');
		$alert = $el.find('.tx_alert');
	}
	
	if(options.top) {
		var top = $(options.top)[0].clientHeight || $(options.top).height();
		$alert.find('span').css({
			'margin-top': top
		})
	}
	
	if(options.info) {
		$alert.find('span').html(options.info);
	}
	$alert.show();
	
	if(options.speed) {
		alertTimeoutValue = setTimeout(function() {
			clearTimeout(alertTimeoutValue);
			alertTimeoutValue = null;
			$alert.hide();
		}, options.speed)
	}
};
} ())