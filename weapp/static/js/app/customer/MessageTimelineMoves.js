/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.MessageTimelineMoves = W.ApiCollection.extend({
	dataCache: null,
	
	submit: function(options) {
		W.getApi().call(_.extend({}, options, {
			app: 'message',
			api: 'category_user/get'
		}));
	},
	
	url: function() {
		var appName = 'groups/get';
		var url = W.getApi().getUrl('customer', appName);
		return url;
	},
	
	getText: function(data) {
		
	},
	
	editJson: function(data) {
		var i, k, name;
		for(i = 0, k = data.length; i<k; i++) {
			name = data[i].name;
			data[i].name = name;
		}
		return data;
	},
	
	parse: function(resp) {
		var data = resp.data;
		this.dataCache = data;
		return this.dataCache;
	}
});