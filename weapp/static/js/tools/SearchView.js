/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.SearchView = function(options) {
	var $el = $(options.el);
	var $searchBtn = $el.find('#searchBtn');
	var $searchInput = $el.find('#searchInput');
	var defaultValue = $searchInput.val();
	var _this = this;
	$searchBtn.bind('click', function(event) {
		var $link = $(this);
		var value = $.trim($searchInput.val());
		_this.setLinkAttr($link, value);
		return false;
	});
	$el.delegate('.ui-input-clear', 'click', function() {
		$searchInput.val('');
		if(!defaultValue) {
			return;
		}
		else {
			$searchInput.blur();
		}
		_this.setLinkAttr($searchBtn, '');
		return;
	});
}

W.SearchView.prototype = {
	setLinkAttr: function($link, value) {
		value = value ? value : '';
		var href = $link.attr('href');
		if(!value) {
			href = href.indexOf('?') ? href.split('?')[0] : href;
			value = '';
		}
		else {
			href = href.indexOf('&query=') ? href.split('&query=')[0] : href;
			value = '&query='+value;
		}
		console.log(href+value)
		window.location.href = href+value;
	}
}

$(document).ready(function() {
	new W.SearchView({
		el: '.ui-search-box'
	})
});