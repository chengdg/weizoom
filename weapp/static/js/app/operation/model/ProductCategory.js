/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 商品类别
 * @constructor
 */
W.mall.ProductCategory = Backbone.Model.extend({
    initialize: function() {
        this.products = null;
    },

    flushProducts: function() {
        if (!this.products) {
            return;
        }

        _.each(this.products, function(product) {
            if (product.id < 0) {
                product.id = 0-product.id;
            }
        });
    },

    renewProducts: function() {
        if (!this.products) {
            return;
        }

        _.each(this.products, function(product) {
            if (product.id > 0) {
                product.id = 0-product.id;
            }
        });
    },
	// 注意isrenew是后加的
    getProducts: function(callback, scope, isrenew) {
        if (!this.products) {
            W.getLoadingView().show();
            xlog('get products for category ' + this.get('id'));
            W.getApi().call({
                app: 'mall2',
                api: 'product_list',
                args: {
                    category_id: this.get('id')
                },
                success: function(data) {
                    this.products = data;
	                if(isrenew){
		                this.renewProducts();
	                }
                    callback.call(scope, this.products);
                    W.getLoadingView().hide();
                },
                error: function(response) {
                    alert('获取商品列表失败');
                    W.getLoadingView().hide();
                },
                scope: this
            });
        } else {
            xlog('use cached products');
            callback.call(scope, this.products);

        }
    }
});
