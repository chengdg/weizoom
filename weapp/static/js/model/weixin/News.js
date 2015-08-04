/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

ensureNS('W.model.weixin.material');
W.model.weixin.material.News = Backbone.Model.extend({

})


/*
 * W.model.weixin.material.Newses: 图文消息
 */
W.model.weixin.material.Newses = W.ApiCollection.extend({
	model: W.model.weixin.material.News,
	app: 'weixin/message/material',

	initialize: function(models, options) {
		this.page = '0';
	},

	url: function(){
		return this.getApiUrl('newses/get',{
			page: this.page
		});
	},

	/**
	 * 获得分页信息
	 */
	getPageData: function() {
		return this.pageInfo;
	},

	setPage: function(page){
		this.page = page;
	},

	parse: function(response){
		var data = response.data;
		if(!data) {
			return [];
		}
		this.pageInfo = data.page_info;
		return data.items;
	}
})