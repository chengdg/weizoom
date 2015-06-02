/*传播监控 微博传播分析详情*/
W.WineOrderDetailCollection = W.ApiCollection.extend({
	model: W.ApiModel,
    
    app: 'wine',
    
    args: {
        
	},
	
	initialize: function(attrs, options) {
        if(attrs.args) {
            this.args = attrs.args;
        }
	},
	
	url: function() {
        return this.getApiUrl('orders', this.args);
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
		return resp.items || [];
	}
});

W.TourOrderDetailCollection = W.ApiCollection.extend({
    model: W.ApiModel,
    
    app: 'tour',
    
    args: {
        
    },
    
    initialize: function(attrs, options) {
        if(attrs.args) {
            this.args = attrs.args;
        }
    },
    
    url: function() {
        return this.getApiUrl('orders', this.args);
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
        return resp.items || [];
    }
});

W.RiceOrderDetailCollection = W.ApiCollection.extend({
	model: W.ApiModel,

	app: 'rice',

	args: {

	},

	initialize: function(attrs, options) {
		if(attrs.args) {
			this.args = attrs.args;
		}
	},

	url: function() {
		return this.getApiUrl('orders', this.args);
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
		return resp.items || [];
	}
});