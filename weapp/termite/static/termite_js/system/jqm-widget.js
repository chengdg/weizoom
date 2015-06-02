/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.swipeimage widget
 */
(function( $, undefined ) {

$.widget( "weizoom.swipeimage", $.mobile.widget, {
	options: {
		initSelector: ":jqmData(role='swipeimage')",
		imageWidth: 0,
		imageHeight: 0,
		imagesJson: [],
		design: false
	},
	_create: function() {
		var $el = this.element;

		//生成html
		var swipeImages = this.options.imagesJson;
		var htmls = []
		htmls.push('<div class="swipeImage-border">');
		if (swipeImages.lenth === 0) {
			htmls.push('<div class="swipeImage-images">暂无图片</div>');
		} else {
			htmls.push('<div class="swipeImage-images"></div>');
			htmls.push('<nav><ul class="swipeImage-position">');
			for (var i = 0; i < swipeImages.length; ++i) {
				var image = swipeImages[i];
				if (i === 0) {
					htmls.push('<li class="on" data-index="' + i + '"></li>');
				} else {
					htmls.push('<li data-index="' + i + '"></li>');
				}
			}
			htmls.push('</ul></nav>');
		}
		htmls.push('</div>');
		$el.addClass('swipeImage').html($(htmls.join('\n')));

		if ($el.innerWidth() !== 0) {
			this.refresh();
		}
	},

	refresh: function() {
		var $el = this.element;

		//确定轮播图区域的高度
        var ratio = (this.options.imageWidth+0.0) / ($el.innerWidth() * 0.94);
        var height = this.options.imageHeight / ratio;
        console.warn($el.innerWidth());
        $el.find('.swipeImage-images').height(height+'px');

        //创建swipe photo control
        var swipeImages = $.parseJSON($('.swipeImage').eq(0).attr('data-images-json'));
        var PhotoSwipe = window.Code.PhotoSwipe;
        var photoSwipeOptions = {
        	target: $('.swipeImage-images')[0],
            preventHide: true,
            loop: true,
            autoStartSlideshow: true,
            getImageSource: function(obj){
                return obj.url;
            },
            getImageCaption: function(obj){
                return '';
            }
        }
        if (this.options.design) {
        	//design模式下的option
        	photoSwipeOptions['enableDrag'] = false;
            photoSwipeOptions['enableKeyboard'] = false;
            photoSwipeOptions['enableMouseWheel'] = false;
            photoSwipeOptions['allowUserZoom'] = false;
        }
        var instance = PhotoSwipe.attach(
            swipeImages,
            photoSwipeOptions
        );
        instance.addEventHandler(window.Code.PhotoSwipe.EventTypes.onDisplayImage, function(event) {
            $('li.on').removeClass('on');
            $('li[data-index="'+event.index+'"]').addClass('on');
        });
        instance.addEventHandler(window.Code.PhotoSwipe.EventTypes.onTouch, function(event) {
            if (event.action === 'tap') {
            	if (!this.options.design) {
	                var image = event.currentTarget.originalImages[event.currentTarget.currentIndex];
	                if (image) {
	                    //TODO: 使用jquery mobile的跳转函数
	                    window.location.href = image.link_url;
	                }
                }
            }
        });
        instance.show(0);
	}
});

//auto self-init widgets
$.mobile.document.bind( "pagecreate create", function( e ) {
	$.weizoom.swipeimage.prototype.enhanceWithin(e.target, true);
});

$.mobile.document.bind('pageshow', function(e) {
	$('[data-role="swipeimage"]').swipeimage('refresh');
});
})( jQuery );