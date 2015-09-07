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
				//获取上一页的url，再通过href转向(修复history.back(-1)不刷新页面的问题)
				var preUrl = document.referrer;
				var host = window.location.host;
				preUrl = preUrl.substr(preUrl.indexOf(host)+host.length);
				console.log(preUrl);
				if(!preUrl){//当前页如果不是通过超链接进来的话，会得到null
					window.history.back(-1);
				}else{
					window.location.href = preUrl;
				}
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