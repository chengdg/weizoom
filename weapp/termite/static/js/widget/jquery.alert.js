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
	
	if(!$alert.length) {
		$el.append('<div class="loding loading tx_alert wui-alert wui-loading" name="loading" style="display:none;"><span>加载中...</span></div>');
		$alert = $el.find('.tx_alert');
	}
    
    if(options.isShow === false) {
		$alert.css({display:'none'});
		return;
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
    if(options.isSlide) {
        var height = $alert.height();
        $el.css({
            'z-index':'999999',
            'position': 'relative'
        })
        $alert.css({
            'top': -height + 'px',
            'display': 'block'
        });
        setTimeout(function() {
            $alert.css({
                'top': '0px',
                '-moz-transition': 'top 0.5s',
                '-webkit-transition': 'top 0.5s',
                '-o-transition':  'top 0.5s',
                'transition':  'top 0.5s'
            });
        }, 0);
    }
    else {
        $alert.css({
            'display': 'block'
        });
    }
	
	if(options.speed) {
		alertTimeoutValue = setTimeout(function() {
			clearTimeout(alertTimeoutValue);
			alertTimeoutValue = null;
            if(options.isSlide) {
                $alert.css({
                    'top': -height+'px',
                    '-moz-transition': 'top 0.5s',
                    '-webkit-transition': 'top 0.5s',
                    '-o-transition':  'top 0.5s',
                    'transition':  'top 0.5s'
                });
            }
            else {
                $alert.css({display:'none'});
            }
            
            if(options.callBack) {
                options.callBack();
            }
		}, options.speed)
	}
    else {
        if(options.callBack) {
            options.callBack();
        }
    }
};
} ())