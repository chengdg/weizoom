/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.swipeimage widget
 */
(function( $, undefined ) {

gmu.define('SwipeDialog', {
	options: {
		width: 0,
		height: 0,
		jsondata: [],
		design: false
	},
	_create: function() {
		var $el = this.$el;

		var bodyHeight = window.document.body.clientHeight;
        var containerHeight = bodyHeight - 42; //tab height is 42px,tab-coupon height is 42px
        // var containerHeightNew = bodyHeight - 55; //tab height is 42px,tab-coupon height is 42px
        // isNewTab = $('.wui-swiper-container').parents('.xui-page').hasClass('xui-editOrderPage');
        // if(isNewTab){
        //     $el.find(".wui-swiper-container").css('height', containerHeightNew);
        //     $el.find(".wui-swiper-slide").css('height', containerHeightNew);
        // }else{
             $el.find(".wui-swiper-container").css('height', containerHeight);
             $el.find(".wui-swiper-slide").css('height', containerHeight);
        // }
        $el.css({
            top: screen.height,
            display:'block'
        });
        
        var tabsSwiper = new Swiper('.wui-swiper-container', {
            speed:500,
            onSlideChangeStart:(function(){
                $el.find(".wui-swiper-tabs .wui-inner-active,.wui-swiper-tabs-coupon .wui-inner-active").removeClass('wui-inner-active');
                $el.find(".wui-swiper-tabs a,.wui-swiper-tabs-coupon a").eq(tabsSwiper.activeIndex).addClass('wui-inner-active');
                if (/ipad|iphone|mac/i.test(navigator.userAgent)){
                    myscroll=new iScroll(tabsSwiper.activeSlide(),{hScrollbar:false});
                }
            })
        });
        $el.find(".wui-swiper-tabs a,.wui-swiper-tabs-coupon a").bind('click',function(e){
            e.preventDefault();
            var $link = $(this);
            $el.find(".wui-swiper-tabs .wui-inner-active,.wui-swiper-tabs-coupon .wui-inner-active").removeClass('wui-inner-active');
            $link.addClass('wui-inner-active');
            tabsSwiper.swipeTo( $link.index());
            if (/ipad|iphone|mac/i.test(navigator.userAgent)){
                myscroll=new iScroll(tabsSwiper.activeSlide(),{hScrollbar:false});
            }
        });

        //在DOM中缓存this
        $el.data('view', this);
	},

	show: function() {
		this.$el.css({
            top: 0
        });
	},

	hide: function() {
		this.$el.css({
            top: screen.height
        });
        $('.error-info').html('');
	}
});

$(function() {
	$('[data-ui-role="swipedialog"]').each(function() {
		var $dialog = $(this);
		$dialog.swipeDialog();
	});
})
})( Zepto );