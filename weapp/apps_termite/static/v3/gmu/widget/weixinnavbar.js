/*
 * 仿微信的底部导航
 * 
 *
 * 使用示例;
 */
 (function( $, undefined ) {

gmu.define('weixinnavbar', {
    _create: function() {
        xlog('create weixinnavbar')
        var $el = this.$el;
        $el.addClass('wui-navBar-container');
        var $lis = $el.find('li');
        var liCount = $lis.length;
        var $a = $el.find('a');
        var width = 100/(liCount+0.0) + '%';
        $lis.each(function() {
            var $li = $(this);
            $li.css('width', width);
            var $nestedDiv = $li.find('div');
            if ($nestedDiv.length > 0) {
                $li.prepend('<span class="wui-navList-more"></span>');
                $nestedDiv.addClass('wui-navList');
                $nestedDiv.prepend('<span class="wui-navList-arrow wui-navList-beforearrow"></span><span class="wui-navList-arrow wui-navList-afterarrow"></span>');
                $nestedDiv.find('a:last-child').addClass('wui-navList-last');
            }
        });
        $el.find('li').addClass('wui-navBar-item');
        $a.highlight();

        this._bind();
        var $page =$el.siblings('.xui-page');
        var $Swiper = $page.find('.wui-swiper-container');
        var $ul = $Swiper.find('.xui-list ul');
        if ($Swiper.length > 0) {
            $ul.css('padding-bottom', '50px');
        }else{
            $page.css('padding-bottom','50px');
        };

        //在DOM中缓存this
        $el.data('view', this).show();
    },

    _bind: function() {
        var _this = this;
        this.$el.find('.wui-navBar-item').click(function(event){
            event.stopPropagation();

            var $otherItem = $(this).siblings().find('.wui-navList');
            var $el = $(this).find('.wui-navList');
            if($el.is(':visible')){
                $el.fadeOut(200);
                $otherItem.fadeOut(200);
            } else {
                $el.fadeIn(200);
                $otherItem.fadeOut(200);
            }
        });

        $(document).click(function(event) {
            _this.$el.find('.wui-navList').each(function() {
                var $popup = $(this);
                if ($popup.is(':visible')) {
                    $popup.fadeOut(200);
                }
            });
        });
    }
});

$(function() {
    $('[data-ui-role="weixinnavbar"]').each(function() {
        var $input = $(this);
        $(this).weixinnavbar();
    });
})
})( Zepto );