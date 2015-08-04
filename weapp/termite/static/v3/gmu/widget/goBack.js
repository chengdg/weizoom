/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用范例：<i data-ui-role="goBack"></i>
 * weizoom.ReturnTop widget
 */
(function( $, undefined ) {
gmu.define('GoBack', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
		var $goBackBtn = $el.wrap('<a class="xa-goBack xui-returnPrev pa"></a>');
		$el.parent().click(function(event) {
			if(window.history.length == 1){
				window.location.href = './?woid='+W.webappOwnerId+'&module=mall&model=products&action=list';
			}else{
				window.history.back(-1);
			}
		});
	}
});

$(function() {
	$('[data-ui-role="goBack"]').each(function() {
		$(this).goBack();
	});
})
})( Zepto );