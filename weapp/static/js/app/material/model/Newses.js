/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.material.News = Backbone.Model.extend({

})


/*
 * W.material.Newses: 图文消息
 */
W.material.Newses = W.ApiCollection.extend({
	model:W.material.News,
	app: 'material',

	initialize: function(models, options) {
		this.page = '1';
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