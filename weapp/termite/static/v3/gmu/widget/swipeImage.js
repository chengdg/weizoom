/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.swipeimage widget
 */
(function( $, undefined ) {
gmu.define('SwipeImage', {
	options: {
		width: 0,
		height: 0,
		jsondata: [],
		design: false
	},
	
	_create: function() {
		var $el = this.$el;
		
		//确定轮播图区域的高度
		//var ratio = (this._options.width+0.0) / ($el.width() * 1.0);
        //var height = this._options.height / ratio;
        var height = $el.width();
        console.log(height);
        $el.height(height+'px').css('visibility', 'hidden');
        
		//生成html
		var swipeImages = this._options.jsondata;
		var htmls = []
		if (swipeImages.length === 0) {
			htmls.push('<div class="wui-swiper-wrapper">暂无图片</div>');
		} else {
			htmls.push('<div class="wui-swiper-wrapper">');
			for (var i = 0; i < swipeImages.length; ++i) {
				var image = swipeImages[i];
				htmls.push('<div class="wui-swiper-slide"><img src="'+image.url+'" style="width:100%;vertical-align: middle;" /></div>')
			}
			htmls.push('</div>');
			htmls.push('<div class="wui-swiper-pagination-fraction"><span class="xa-numerator wui-numerator"></span>/<span class="xa-denominator"></span></div>');
		}
		
		
		$el.addClass('wui-swiper-container wui-swipeImage').attr('id', 'swipeImage').html($(htmls.join('\n'))).css('visibility', 'visible');
		var $swipeSlide = $el.find('.wui-swiper-slide');
		$swipeSlide.css('line-height', height + "px");
	},

	refresh: function() {
		var $el = this.$el;
		var swipeImages = this._options.jsondata;
        var view = new Swiper('#swipeImage', {
	        mode:'horizontal',
	        loop: true,
	        autoplay: 3000,
	        onInit:function(){
	        	if(swipeImages.length == 1){
	        		view.stopAutoplay();
	        	}
	        }
	        //pagination: '.wui-swiper-pagination'
	    });
	    var $numerator = $el.find('.xa-numerator');
	    var $denominator = $el.find('.xa-denominator');
	    var activeIndex = view.activeLoopIndex + 1;
	    var imageLength = swipeImages.length;
	    $numerator.text(activeIndex);
	    $denominator.text(imageLength);	    
	    view.addCallback('SlideChangeStart',function(Swiper){
	    	var activeIndex = view.activeLoopIndex + 1;
	    	$numerator.text(activeIndex);
	    });
	    $el.data('view', view);
	}
});

$(function() {
	$('[data-ui-role="swipeimage"]').each(function() {
		var swipeImage = $(this).swipeImage();
		swipeImage.swipeImage('refresh');
	});
})
})( Zepto );