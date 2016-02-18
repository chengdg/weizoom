/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.model.weixin');
/**
 * W.Session: 一个微信会话
 *
 * @constructor
 *
 */
W.model.weixin.WeixinMessage = Backbone.Model.extend({
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
W.model.weixin.WeixinMessages = W.ApiCollection.extend({
	model: W.model.weixin.WeixinMessage,
	
	initialize: function(models, options) {
        this.page = '1';
	},
	
	
	url: function() {
		var timestamp = new Date().getTime();

		return W.getApi().getUrl('weixin/message/message', 'messages/get', {
			timestamp: timestamp,
            page: this.page,
            is_collected: this.is_collected,
            search_content: this.search_content
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