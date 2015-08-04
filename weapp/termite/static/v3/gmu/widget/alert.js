/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * alert信息显示框
*/
(function($) {
var alertTimeoutValue = null;
$.fn.alert = function(options) {
	var $el = $(this);
	var $alert = $el.find('.wui-alert');

	if(alertTimeoutValue) {
		clearTimeout(alertTimeoutValue);
		alertTimeoutValue = null;
	}
	
	if(!$alert.length) {
		$el.append('<div class="loding loading tx_alert wui-alert wui-loading" name="loading" style="display:none;"><span>加载中...</span></div>');
		$alert = $el.find('.wui-alert');
	}
    

    if(options.isLager){
        $alert.addClass('wui-lagerAlert');
        
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
        });
        //because zepto can't calculate invisible element's height, we use this trick
        $alert.css({
            'top': -500 + 'px',
            'display': 'block'
        });
        var height = $alert.height();
        $alert.css({
            'top': -height+'px'
        })

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

    //支持test
    if (options.isError) {
        var $errMsg = $('#xt-errMsg');
        $errMsg.val(options.info);
    }
	
	if(options.speed) {
		alertTimeoutValue = setTimeout(function() {
			clearTimeout(alertTimeoutValue);
			alertTimeoutValue = null;
            if(options.isSlide) {
                var height = $alert.height();
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
} (Zepto))