/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用示例;
 * <div class="wui-returnTop xa-returnTop hidden" data-ui-role="return-top"></div>
 * weizoom.ReturnTop widget
 */
(function( $, undefined ) {
gmu.define('ReturnTop', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
	},
	

	show: function() {
		this.$el.find('.wui-returnTop').css({
            'display': 'block'
        });
	},

	hide: function() {
		this.$el.find('.wui-returnTop').css({
            'display': 'none'
        });
	},
	slideShow:function(){
		var flag = $('.xa-content').parent('.ui-refresh-wrapper');
		if(flag.length == 0){
			var scrollTop = $('body').scrollTop(); 
	        if(scrollTop > 10){
	             $('body').returnTop('show');
	        }else{
	            $('body').returnTop('hide');
	        } 
		}else{
			var transform = $('.xa-content').css('-webkit-transform');
	        var matrix = new WebKitCSSMatrix(transform);

	        if(matrix.m42 < 0){
	            $('body').returnTop('show');
	        }else{
	            $('body').returnTop('hide');
	        } 
		}
		
	},
	returnTop:function(){
	var flag = $('body').find('.ui-refresh-wrapper');
	if(flag.length == 0){
		$('body').scrollTop(0);
	}else{
		$('.xa-content').css('-webkit-transform','translateY(0)');
	}
		$('body').returnTop('hide');
	}
});

$(function() {
	$('[data-ui-role="return-top"]').each(function() {
		var $returnTop = $(this);
		$returnTop.returnTop();
	});

	$('body').bind('touchstart, touchmove',function(){
        $('[data-ui-role="return-top"]').returnTop('slideShow');
    });

    $('.xa-returnTop').click(function(){
        $('[data-ui-role="return-top"]').returnTop('returnTop');
    });
})
})( Zepto );