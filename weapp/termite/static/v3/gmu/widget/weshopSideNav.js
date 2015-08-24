  /*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用示例;
 * <div class="xui-globalSideBar xa-globalSideBar" data-ui-role="sideNav"></div>
 * weizoom.weshopsideNav widget
 */
(function( $, undefined ) {
gmu.define('SideNav', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
		$('.wa-page').css('padding-bottom',50);

		var _this = this;
		this.isIScrollInitialized = false;
		// 判断是否是pc编辑页，底部导航不可切换
		if (!this._options['disable-switch']) {
			$el.find('.xa-category').click(function(){
				var $categoryBtn = $(this);
				_this.showLeftPanel();
				if (!_this.isIScrollInitialized) {
					var myscroll = new iScroll('xa-wrapper',{hScrollbar:false});	
					_this.isIScrollInitialized = true;
				}
				$categoryBtn.find('i').addClass('xui-active');
			});
		}

		var activeTarget = this._options['auto-active'];
		if (!activeTarget) {
			activeTarget = W.currentPageName;
		}
		if (activeTarget) {
			var $targetBtn = $el.find('[data-page="'+activeTarget+'"]');
			$targetBtn.find('i').addClass('xui-active');

			if (activeTarget == 'product-category') {
				this.showLeftPanel();
			}
		}

		$(document).delegate('.xa-firstNav', 'click', _.bind(this.onClickFirstNav, this));
	},
	
	showLeftPanel: function() {
		this.$el.find('.xa-sidePanel').show();
	},

	hideLeftPanel: function() {
		this.$el.find('.xa-sidePanel').hide();
	},

	onClickFirstNav:function(event){
		var $firstNav = $(event.currentTarget);

		var $arrow = $firstNav.find('i');
        var $subMenu = $firstNav.find('.xui-subMenu');
        if( $subMenu.find('li').length >0 ){
	        var display = $subMenu.css('display');
	        if( display != 'block' ){
	            $arrow.removeClass('xui-leftArrow');
	            $arrow.addClass('xui-topArrow');
	            $subMenu.show();
	        }else{
	            $arrow.removeClass('xui-topArrow');
	            $arrow.addClass('xui-leftArrow');
	            $subMenu.hide();
	        }
	    }
	}
});

$(function() {
	$('[data-ui-role="sideNav"]').each(function() {
		var $sideNav = $(this);
		$sideNav.sideNav();
	});
})
})( Zepto );