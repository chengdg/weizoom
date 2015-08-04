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
        $el.height(height+'px').css('visibility', 'hidden');

		//生成html
		var swipeImages = this._options.jsondata;
		var htmls = []
		if (swipeImages.length === 0) {
			htmls.push('<div class="wui-swiper-wrapper">暂无图片</div>');
		} else {
			htmls.push('<div class="wui-swiper-wrapper">');
			var positionMode = this._options.positionmode;
			for (var i = 0; i < swipeImages.length; ++i) {
				var image = swipeImages[i];
				if (image.link_url && positionMode === 'dot') {
					htmls.push('<div class="wui-swiper-slide"><a href="'+image.link_url+'"><img src="'+image.url+'" style="width:100%;vertical-align: middle;" /></a></div>')
				} else {
					htmls.push('<div class="wui-swiper-slide"><img src="'+image.url+'" style="width:100%;vertical-align: middle;" /></div>')
				}
			}
			htmls.push('</div>');

			if (this._options.showtitle) {
				htmls.push('<span class="wui-i-bottomTitle wa-title" style="display:none;">'+swipeImages[0].title+'</span>');
			}
			if (positionMode === 'dot') {
				htmls.push('<div class="wui-i-dotPositions">');
				for (var i = 0; i < swipeImages.length; ++i) {
					var image = swipeImages[i];
					if (i == 0) {
						htmls.push('<span class="wui-i-dotPosition wui-i-activeDotPosition" data-index="0" data-title="'+image.title+'"></span>')
					} else {
						htmls.push('<span class="wui-i-dotPosition" data-index="'+i+'" data-title="'+image.title+'"></span>')
					}
				}	            
	            htmls.push('</div">');
	        } else {
	        	htmls.push('<div class="wui-swiper-pagination-fraction"><span class="xa-numerator wui-numerator"></span>/<span class="xa-denominator"></span></div>');
	        }			
		}
		
		
		$el.addClass('wui-swiper-container wui-swipeImage').attr('id', 'swipeImage').html($(htmls.join('\n'))).css('visibility', 'visible');
		var $swipeSlide = $el.find('.wui-swiper-slide');
		$swipeSlide.css('line-height', height + "px");

		var $title = $el.find('.wa-title');
	    if ($.trim($title.text()).length !== 0) {
	    	$title.show();	
	    }
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

	    var positionMode = this._options.positionmode;
	    var isShowTitle = this._options.showtitle;
	    view.addCallback('SlideChangeStart',function(Swiper){
	    	if (positionMode === 'dot') {
	    		$el.find('.wui-i-activeDotPosition').removeClass('wui-i-activeDotPosition');
	    		var $position = $el.find('[data-index="'+view.activeLoopIndex+'"]');
	    		$position.addClass("wui-i-activeDotPosition");
	    		if (isShowTitle) {
	    			var title = $.trim($position.attr('data-title'));
	    			var $title = $el.find('.wa-title');
	    			if (title.length === 0) {
	    				$title.hide().text('');
	    			} else {
		    			$title.text(title).show();
		    		}
	    		}
	    	} else {
	    		var activeIndex = view.activeLoopIndex + 1;
	    		$numerator.text(activeIndex);
	    	}
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