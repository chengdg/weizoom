/**
 * 一个product group的总价计算器
    1. 限时抢购：抢购价（不用计算）
    2. 满减：减后价（不用计算）
    3. 积分应用：（需要计算）
    4. 买赠：不影响价格
    5. 无促销商品：不用计算
 */



W.common.ProductGroupPriceCalculator = BackboneLite.View.extend({
    initialize: function(options) {
    },

    has_promotion: function(user_member_grade_id, promotion_member_grade_id){
            if(promotion_member_grade_id == '0'){return true;}
            if(promotion_member_grade_id == user_member_grade_id){
                return true;
            }else{
                return false;
            }
    },

    promotion_price: function(member_grade_id, product){
        // 非会员
        if(!member_grade_id){return product.original_price};

        // 商品促销与否
        is_product_promotion = !($.isEmptyObject(product.promotion));
        if(is_product_promotion){
            // 促销是否对用户开放
            var use_has_promotion = has_promotion(member_grade_id, product.promotion.member_grade_id);
            if(user_has_promotion){
                // 限时抢购
                if(product.promotion.detail.promotion_price){
                    return product.promotion.detail.promotion_price;

                }
            }
        }

        if(product.is_member_product){
            return product.price;
        }
        return product.original_price
    },

    calculate: function(productGroups) {
        var productPrice = 0.0;
        var promotionedPrice = 0.0;
        var integralMoney = 0;
        var totalCount = 0;
        for (var i = 0; i < productGroups.length; ++i) {
            var productGroup = productGroups[i];

            if (productGroup.can_use_promotion && productGroup.promotion_type === 'flash_sale') {
                // 限时抢购
                var product = productGroup.products[0];
                if (product.isSelect) {
                    productPrice += product.price * product.count;
                    promotionedPrice += product.price * product.count;
                    totalCount += product.count;
                }
            } else if (productGroup.can_use_promotion && productGroup.promotion_type === 'price_cut') {
                // 满减
                for(var j = 0; j < productGroup.products.length; ++j) {
                    var product = productGroup.products[j];
                    if (product.isSelect) {
                        productPrice += product.price * product.count;
                        totalCount += product.count;
                    }
                }

                xlog(productGroup.promotion_result);
                if (productGroup.promotion_result.originalSubtotal) {
                    promotionedPrice += productGroup.promotion_result.originalSubtotal;
                } else {
                    promotionedPrice += productGroup.promotion_result.subtotal;
                }
            } else if (productGroup.can_use_promotion && productGroup.promotion_type === 'premium_sale') {
                // 买赠
                for (var j = 0; j < productGroup.products.length; ++j) {
                    var product = productGroup.products[j];
                    if (product.isSelect) {
                       productPrice += product.price * product.count;
                        promotionedPrice += product.price * product.count;
                        totalCount += product.count;
                    }
                }
            } else {
                // 普通商品
                for(var j=0; j < productGroup.products.length; ++j){
                    var product = productGroup.products[j];
                    if (product.isSelect) {
                        productPrice += product.price * product.count;
                        promotionedPrice += product.price * product.count;
                        totalCount += product.count;
                    }
                }
            }

            //累加积分金额
            if (productGroup.promotion_result && productGroup.promotion_result.integralMoney) {
                integralMoney += productGroup.promotion_result.integralMoney;
            }
        }
        return {
            productPrice: productPrice,
            promotionedPrice: promotionedPrice,
            integralMoney: integralMoney,
            totalCount: totalCount
        }
    }
});


/**
 * PremiumSaleView: 买赠应用View
 */
W.common.PremiumSaleView = BackboneLite.View.extend({
    initialize: function(options) {
        this.$el = $(this.el);

        this.productGroups = options.productGroups;
        this.integralManager = options.integralManager;
    },

    render: function() {
        var $productGroup = this.$el;
        var productGroupId = parseInt($productGroup.data('productGroupId'));
        var productGroup = _.findWhere(this.productGroups, {"id": productGroupId});

        var totalCount = 0;
        var totalPrice = 0.0;
        for (var i = 0; i < productGroup.products.length; ++i) {
            var product = productGroup.products[i];
            totalCount += product.count;
            totalPrice += product.price * product.count;
        }

        if (productGroup.can_use_promotion) {
            var premiumProducts = productGroup.promotion.detail.premium_products;
            for (var i = 0; i < premiumProducts.length; i++ ) {
                var premiumProduct = premiumProducts[i];
                totalCount += premiumProduct.premium_count;
            }
        }

        productGroup.totalCount = totalCount;
        console.log('premium sale totalCount', totalCount);
        $productGroup.find('.xa-promotion-info').html('共<span class="xt-subtotalCount">'+totalCount+'</span>件商品，');
        $productGroup.find('.xa-subtotal').text(totalPrice.toFixed(2));
    }
});
