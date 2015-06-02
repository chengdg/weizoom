W.CommonFilterCollection = W.ApiCollection.extend({
	model: W.ApiModel,
    
    app: '',
    api: '',

    args: {
        
	},
	
	initialize: function(options) {
        if(options) {
           if (options.args) {
                this.args = options.args;
           }
            this.app = options.app;
            this.api = options.api;
        }
	},
	
	url: function() {
        return this.getApiUrl(this.api, this.args);
	},
	
	parse: function(resp) {
        resp = resp.data || {};
        var i, k;
        var statusText = ['待支付', '已取消', '已支付', '待发货', '已发货', '已完成'];
        if(resp.items && resp.items.length) {
            for(i = 0, k = resp.items.length; i<k; i++) {
                resp.items[i].status = statusText[resp.items[i].status];
            }
        }
        this.cacheData = resp.items;
        this.cacheCategories = resp.categories;
		return resp.items || [];
	}
});