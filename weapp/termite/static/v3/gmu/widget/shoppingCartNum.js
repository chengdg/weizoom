/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 购物车角标数量
 * author: liupeiyu
 * 
 * 使用示例;
 * 计算商品促销价或会员价
 * CalculProductMemberPriceOrPromotionPrice
 * $('.xui-products-original').setShoppingCartNum({
        webappUserId: webappUserId,
        updateShoppingCartNum: function(event, data){
            data.count;
        }
    });
 */
(function($, undefined) {
	gmu.define('SetShoppingCartNum', {
		options: {
		},

		_init: function(options){
			this.webappUserId = options.webappUserId;
		},

		_create: function() {
			// 当页面中有 购物车脚本 时，才去取购物车数量信息
			if (this.$el.length > 0) {
				this.getShoppingCartNum();				
			};
		},

		getShoppingCartNum: function(){
			var _this = this;				
			W.getApi().call({
				app: 'webapp',
				api: 'project_api/call',
				method: 'get',
				args: {
					webapp_user_id: _this.webappUserId,
					module: 'mall',
					target_api: 'shopping_cart_count/get'
				},
				success: function(data) {
					_this.trigger('updateShoppingCartNum', data);
				},
				error: function(data) {

				}
			});
		}
	});

})( Zepto );