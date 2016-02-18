/*
 * 仿微信的底部导航
 * 
 *
 * 使用示例;
 */
(function($, undefined) {
	$.widget( "weizoom.weixinnavbar", $.mobile.widget, {
        options: {
            initSelector: ":jqmData(ui-role='weixinnavbar')",
        },

        _create: function() {
            this.$el = this.element;
            var $el = this.$el;
            $el.addClass('wui-navBar-container');
            var $lis = $el.find('li');
            var liCount = $lis.length;
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

            this._bind();
            $el.siblings('.ui-page').css('padding-bottom','46px');
        },

        _bind: function() {
            var _this = this;
            this.$el.find('.wui-navBar-item').click(function(event){
                event.stopPropagation();

                var $otherItem = $(this).siblings().find('.wui-navList');
                var $el = $(this).find('.wui-navList');
                if($el.is(':visible')){
                    $el.slideUp(200);
                    $otherItem.slideUp(200);
                } else {
                    $el.slideDown(200);
                    $otherItem.slideUp(200);
                }
            });

            $(document).click(function(event) {
                _this.$el.find('.wui-navList').each(function() {
                    var $popup = $(this);
                    if ($popup.is(':visible')) {
                        $popup.slideUp(200);
                    }
                });
            });
        }

    });

    //auto self-init widgets
    $.mobile.document.bind("pagecreate create", function( e ) {
        //$.weizoom.weixinnavbar.prototype.enhanceWithin(e.target, true);
        $("[data-ui-role='weixinnavbar']").weixinnavbar();
    });
    
})(jQuery);
