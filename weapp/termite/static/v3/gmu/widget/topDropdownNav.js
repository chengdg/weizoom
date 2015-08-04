/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.topDropdowntop widget
 */
(function( $, undefined){
gmu.define('topDropdownNav',{
	_create: function() {
		var $el = this.$el;
		setTimeout(function(){
			$el.removeClass('hidden');
		},500);
		$el.wrap('<div class="wui-topDropdownMenu"></div>');
		var $menu = $el.parent();
		$menu.append('<a href="javascript:void(0);" class="wui-dropdownTrigger"><div class="wui-circle"><div class="wui-dropdownIndicator wui-dropdownIndicator-down"></div></div></a>');
		setTimeout(function(){$menu.find('.wui-dropdownTrigger').css('opacity','1');},200);
		var count = $el.find('li').length;
		var expandTop = '-20px';
		var bodyHeight = window.document.body.clientHeight;
		var max_height = bodyHeight * 0.7;
		var collapsedTop;
		if (count*41 > max_height) {
			collapsedTop = '-'+(max_height) +'px';
		}else{
			collapsedTop = '-'+(count*41 - 20)+'px';
		}
		$menu.css('top', collapsedTop);
		$menu.find('ul').wrap('<div style="overflow: hidden;"></div>');
		$menu.find('ul').css('max-height', max_height+'px');
		this.menuState = 'collapsed';
		var _this = this;
		$menu.on('click', function(event) {
	        if (_this.menuState === 'collapsed') {
	            $menu.addClass('wui-dropdownMenuExpand');
	            $menu.css('top', expandTop);
	            $menu.find('.wui-dropdownIndicator').removeClass('wui-dropdownIndicator-down').addClass('wui-dropdownIndicator-up');
	            _this.menuState = 'expand';
	        } else {
	            $menu.removeClass('wui-dropdownMenuExpand');
	            $menu.css('top', collapsedTop);
	            $menu.find('.wui-dropdownIndicator').removeClass('wui-dropdownIndicator-up').addClass('wui-dropdownIndicator-down');
	            _this.menuState = 'collapsed';
	        }
		});
	}
});
$(function() {
	function delay(){
		$('[data-ui-role="top-dropdown-nav"]').each(function() {
		var topDropdownNav = $(this).topDropdownNav();
		
	});
	}
	delay()
	// _.delay(delay, 100);

})
})( Zepto );