/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用示例;
 * <div class="xui-globalBottomBar xa-globalBottomBar hidden" data-ui-role="bottomNav"></div>
 * weizoom.weshopBottomNav widget
 */
(function( $, undefined ) {
gmu.define('BottomNav', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
		$('body').height($('body').height()+50);

		var _this = this;
		$(document).delegate('.xa-menu', 'click', function(event){
			_this.clickShowSubmenu(event);
		});

		// 点击别的地方，二级菜单消失，但是可能有问题
	    $(document).on('click',function(event){
	    	if(!$(event.target).parent().is('.xa-menu')){
	            $('.xui-subMenuContainer').removeClass('xui-show');
	        }
	    })
	},
	

	clickShowSubmenu:function(event){
		var $target = $(event.currentTarget);
		var $menu = this.$el.find('.xa-menu');
		var menuWidth = $menu.eq(0).width();
		var $subMenuContainer = $target.siblings('.xui-subMenuContainer');
		var $subLink = $target.siblings('.xui-subMenuContainer').find('.xui-subMenu li');
        var $otherSubMenuContainer = $target.parents('.xui-globalBottomBar').find('.xui-subMenuContainer');
        var width = $subMenuContainer.width();
        $otherSubMenuContainer.removeClass('xui-show');
         if( $subLink.length>0){
         	$subMenuContainer.toggleClass('xui-show');
         }
         if($menu.length == 1){
           $subMenuContainer.css('margin-left',-width/2);
         }else if($menu.length == 2){
         	$subMenuContainer.css('margin-left',-width/2- menuWidth/2);
         	$otherSubMenuContainer.eq(1).css({
         		'right':8,
         		'left':'auto',
				'margin-left':0
			});

         }else {
         	$subMenuContainer.css('margin-left',-width/2- menuWidth/2);
         	$otherSubMenuContainer.eq(1).css('margin-left',-width/2+ menuWidth/2);
         	$otherSubMenuContainer.eq(2).css({
         		'right':8,
         		'left':'auto',
				'margin-left':0
			});
         }
	}
});

$(function() {
	$('[data-ui-role="bottomNav"]').each(function() {
		var $bottomNav = $(this);
		$bottomNav.bottomNav();
	});
})
})( Zepto );