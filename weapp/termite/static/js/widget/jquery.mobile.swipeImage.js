/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.swipeimage widget
 */
(function( $, undefined ) {

$.widget( "weizoom.swipeimage", $.mobile.widget, {
	options: {
		initSelector: ":jqmData(ui-role='swipeimage')",
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
		htmls.push('<div class="wui-swipeImage-border">');
		if (swipeImages.length === 0) {
			htmls.push('<div class="wui-swipeImage-images">暂无图片</div>');
		} else {
			htmls.push('<div class="wui-swipeImage-images"></div>');
			if (swipeImages.length !== 1) {
				htmls.push('<nav><ul class="wui-swipeImage-position">');
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
		}
		htmls.push('</div>');
		$el.addClass('wui-swipeImage').html($(htmls.join('\n')));
		$el.wrap('<div class="wui-swipeImageContainer"></div>');

		if ($el.innerWidth() !== 0) {
			this.refresh();
		}
	},

	refresh: function() {
		var $el = this.element;

		//确定轮播图区域的高度
        var ratio = this.options.imageHeight / this.options.imageWidth;
        var height = $el.innerWidth() * ratio;
        $el.find('.wui-swipeImage-images').height(height+'px');

        //创建swipe photo control
        var swipeImages = $.parseJSON($el.attr('data-images-json'));
        var PhotoSwipe = window.Code.PhotoSwipe;
        var photoSwipeOptions = {
        	target: $el.find('.wui-swipeImage-images')[0],
            preventHide: true,
            loop: true,
            autoStartSlideshow: true,
            captionAndToolbarAutoHideDelay: 0,
            swipeThreshold: 100,
            getImageSource: function(obj){
                return obj.url;
            },
            getImageCaption: function(obj){
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
        var _this = this;
        instance.addEventHandler(window.Code.PhotoSwipe.EventTypes.onDisplayImage, function(event) {
            $('li.on').removeClass('on');
            $('li[data-index="'+event.index+'"]').addClass('on');
        });
        instance.addEventHandler(window.Code.PhotoSwipe.EventTypes.onTouch, function(event) {
            if (event.action === 'tap') {
            	if (_this.options && !_this.options.design) {
	                var image = event.currentTarget.originalImages[event.currentTarget.currentIndex];
	                if (image && image.link_url) {
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
	$('[data-ui-role="swipeimage"]').swipeimage('refresh');
});
})( jQuery );