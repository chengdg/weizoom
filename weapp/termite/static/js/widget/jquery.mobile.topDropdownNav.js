/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.swipeimage widget
 */
(function( $, undefined ) {

$.widget( "weizoom.topdropdownnav", $.mobile.widget, {
	options: {
		initSelector: ":jqmData(ui-role='top-dropdown-nav')",
	},
	_create: function() {
		var $el = this.element;
		$el.wrap('<div class="wui-topDropdownMenu"></div>');
		var $menu = $el.parent();
		
		$menu.append('<a href="javascript:void(0);" class="wui-dropdownTrigger"><div class="wui-circle"><div class="wui-dropdownIndicator wui-dropdownIndicator-down"></div></div></a>');
		var count = $el.find('li').length;
		var expandTop = '-20px';
		var bodyHeight = window.document.body.clientHeight;
		var max_height = bodyHeight * 0.7;
		var collapsedTop = '-'+(count*41)+'px';
		if (count*41 > max_height) {
			collapsedTop = '-'+(max_height)+'px';
		}
		$menu.css('top', collapsedTop);
		$menu.find('ul').wrap('<div style="overflow: hidden;"></div>');
		$menu.find('ul').css('max-height', max_height+'px');
		$menu.find('ul').css('overflow', 'auto');
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

//auto self-init widgets
$.mobile.document.bind( "pagecreate create", function( e ) {
	$.weizoom.topdropdownnav.prototype.enhanceWithin(e.target, true);
});

})( jQuery );