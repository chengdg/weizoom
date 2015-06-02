/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.CustomerInfomation = Backbone.Model.extend({

})

/*
* W.CustomerInfomations: 客户信息
*/
W.CustomerInfomations = W.ApiCollection.extend({
	model:W.CustomerInfomation,
	app: 'customerInfomation',

	initialize: function(models, options) {
		this.page = '1';
		this.groupId = -1;
	},

	url: function(){
		var url = W.getApi().getUrl('customer', 'customers/get',{
			page: this.page,
			groupId: this.groupId
		});
		return url;
	},

	setGroupId: function(groupId){
		this.groupId = groupId;
	},

	getGroupId: function(){
		return this.groupId;
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