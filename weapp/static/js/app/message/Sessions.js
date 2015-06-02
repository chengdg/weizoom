/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * W.Session: 一个微信会话
 *
 * @constructor
 *
 */
W.Session = Backbone.Model.extend({
	initialize: function(attrs, options) {
		
	},

	validate: function(attrs) {
	}
});


/**
 * W.Session: 微信会话的集合
 *
 * @constructor
 * @see W.Message
 *
 */
W.Sessions = W.ApiCollection.extend({
	model: W.Session,
	
	initialize: function(models, options) {
        this.page = '1';
	},
	
	
	url: function() {
		var timestamp = new Date().getTime();
		return W.getApi().getUrl('message', 'sessions/get', {
			timestamp: timestamp,
            page: this.page
		});
		//return '/message/api/list/get/?timestamp='+timestamp;
	},
	
	getPageData: function(data) {
		return this.pageInfo;
	},

    setPage: function(page){
        this.page = page;
    },
	
	parse: function(response) {
		var data = response.data;
		if(!data) {
			return [];
		}
		this.pageInfo = data.page_info;
		return data.items;
	}
});