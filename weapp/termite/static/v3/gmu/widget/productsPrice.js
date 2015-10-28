  /*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 使用示例;
 * 计算商品促销价或会员价
 * CalculProductMemberPriceOrPromotionPrice
 * $('.xui-products-original').calculProductPrice({
        fmt: $('body').data('value'),
        updateProductPrice: function(event, data){
            var _this = this;
            $(".xa-product").each(function(){
                // 商品原价
                var price = $(this).data('product-price').toFixed(2);
                // 商品有促销
                var productPromotion = $(this).data('product-promotion');
                var isMemberProduct = $(this).hasClass('xa-member-product');
                // 计算价钱                
                price = _this.calculPrice({
                    price: price,
                    productPromotion: productPromotion,
                    isMemberProduct: isMemberProduct
                });
                // 设置显示价格
                $(this).find('.xt-productPrice').text('￥'+price);
            });
        }
    });
 */
(function($, undefined) {
	gmu.define('CalculProductMemberPriceOrPromotionPrice', {
		options: {
		},

		_init: function(){
			// console.log('init calculProductMemberPriceOrPromotionPrice')
		},

		_create: function() {
			// console.log('create calculProductMemberPriceOrPromotionPrice')
			this.getMemberProductInfo();
		},

		getMemberProductInfo: function(){
			var _this = this;			
			W.getApi().call({
				app: 'webapp',
				api: 'project_api/call',
				method: 'get',
				args: {
					woid: W.webappOwnerId,
					module: 'mall',
					target_api: 'member_product_info/get'
				},
				success: function(data) {
					_this.memberInfoData = data;
					var alertView = $('[data-ui-role="attentionAlert"]').data('view');
					if(data.member_grade_id < 0 && alertView){
						alertView.render();
					}
					_this.trigger('updateProductPrice', data);
				},
				error: function(data) {

				}
			});
		},

		userHasPromotion: function(promotion_member_grade_id){
			if(promotion_member_grade_id == '0'){
				return true;
			}
			if(promotion_member_grade_id == this.memberInfoData.user_member_grade_id){
				return true;
			}else{
				return false;
			}

		},

		/**
		 * [calculPrice description]
		 * @param  {
                    price: price,
                    productPromotion: productPromotion,
                    isMemberProduct: isMemberProduct
            }
		 * @return {[type]}      [description]
		 */
		calculPrice: function(args){
			var price = args.price;	
			var isUserHasPromotion = false;
			if(args.productPromotion){
				// 促销是否对此用户开发
				isUserHasPromotion = this.userHasPromotion(args.productPromotion.member_grade_id);
				if(isUserHasPromotion && args.productPromotion.detail.promotion_price){
					price = (args.productPromotion.detail.promotion_price).toFixed(2);
				}
			}
			if(!isUserHasPromotion){
				// 商品是否折扣
				if(args.isMemberProduct){
					price = ((price * this.memberInfoData.discount / 100).toFixed(2));
				}
			}
			return price;
		}
	});

})( Zepto );