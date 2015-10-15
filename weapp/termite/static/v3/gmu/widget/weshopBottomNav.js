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
		$('.wa-page').css('padding-bottom',60);
		$('.wa-shopBottomNavPage').css('padding-bottom',25);

		var _this = this;
		$(document).delegate('.xa-menu', 'click', function(event){
			var $subMenuContainer = $(this).siblings('.xui-subMenuContainer');
			$subMenuContainer.toggleClass('xui-show');
			if( $subMenuContainer.hasClass('xui-show')){
				_this.clickShowSubmenu(event);
			}
		});

		// 点击别的地方，二级菜单消失，但是可能有问题
	    $(document).on('click',function(event){
	    	if(!$(event.target).parent().is('.xa-menu')){
	            $('.xui-subMenuContainer').removeClass('xui-show');
	        }
	    });
	    $('.xui-subMenuContainer').click(function(){

	    });
	},
	

	clickShowSubmenu:function(event){
		var $target = $(event.currentTarget);
		var $menu = $('.xa-menu'); 
		var menuWidth = $menu.eq(0).width();
		var $subMenuContainer = $target.siblings('.xui-subMenuContainer');
		var $subLink = $target.siblings('.xui-subMenuContainer').find('.xui-subMenu li');
        var $otherSubMenuContainer = $target.parents('.xui-globalBottomBar').find('.xui-subMenuContainer');
        var width = $subMenuContainer.width();
        $otherSubMenuContainer.removeClass('xui-show');
         if( $subLink.length>0){
         	$subMenuContainer.toggleClass('xui-show');
         	width = $subMenuContainer.width();
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
         	$subMenuContainer.css('margin-left',-width/2 - menuWidth);
         	$otherSubMenuContainer.eq(1).css('margin-left',-width/2);
         	$otherSubMenuContainer.eq(2).css({
         		'right':8,
         		'left':'auto',
				'margin-left':0
			});
			if($otherSubMenuContainer.eq(2).width() > 92){
				console.log($otherSubMenuContainer.eq(2),'5555555')
				$otherSubMenuContainer.eq(2).find('.xui-menuArrow').css({
					'right':40,
					'left':'auto',
					'margin-left':0
				});
				$otherSubMenuContainer.eq(2).find('.xui-menuArrowBorder').css({
					'right':40,
					'left':'auto',
					'margin-left':0
				});
			}
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