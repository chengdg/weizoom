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
		$el.find('.xa-menu').click(function(event){
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
		var $subMenuContainer = $target.siblings('.xui-subMenuContainer');
        var $otherSubMenuContainer = $target.parent().siblings('.xui-flex').find('.xui-subMenuContainer');
         $subMenuContainer.toggleClass('xui-show');
         $otherSubMenuContainer.removeClass('xui-show');
         if( $subMenuContainer.length >0 ){
           var width = $subMenuContainer.width();
           $subMenuContainer.css('margin-left',-width/2);
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