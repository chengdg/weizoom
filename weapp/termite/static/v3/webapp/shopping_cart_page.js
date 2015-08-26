/**
 * Backbone View in Mobile
 */
(function() {
/**
 * PriceCutView: 满减View
 */
var PriceCutView = BackboneLite.View.extend({
    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.productGroup = options.productGroup;
    },

    render: function() {
        this.doPromotion();
    },

    doPromotion: function() {
        var totalPrice = 0.0;
        var products = this.productGroup.products;
        for (var i = 0; i < products.length; ++i) {
            var product = products[i];
            if (product.isSelect) {
                totalPrice += product.price * product.count;
            }
        }

        var priceCut = this.productGroup.promotion.detail;
        if (totalPrice >= priceCut.price_threshold) {
            this.productGroup.can_use_promotion = true;
            var count = 1;
            if (priceCut.is_enable_cycle_mode) {
                // 循环满减
                count = Math.floor(totalPrice / priceCut.price_threshold);
            }
            var price = count * priceCut.price_threshold;
            var cutMoney = count * priceCut.cut_money;
            this.productGroup.promotion_result.subtotal = totalPrice - cutMoney;
            this.$('.xa-notSatisfyPriceCut').hide();
            this.$('.xa-priceCut-cutMoney').text(cutMoney);
            this.$('.xa-priceCut-price').text(price);
            this.$('.xa-satisfyPriceCut').show();
        } else {
            this.$('.xa-satisfyPriceCut').hide();
            this.$('.xa-notSatisfyPriceCut').show();
            this.productGroup.promotion_result.subtotal = totalPrice;
        }

        this.$('.xa-subtotal-price').text('￥'+this.productGroup.promotion_result.subtotal.toFixed(2));
    },

    doSelectProduct: function() {

    }
});


/**
 * PremiumSaleView: 买赠View
 */
var PremiumSaleView = BackboneLite.View.extend({
    events: {
    },

    initialize: function(options) {
        xlog('create premium sale view');
        this.$el = $(this.el);

        this.productGroup = options.productGroup;
        this.$el.bind('count-changed', _.bind(this.onChangeCount, this));
    },

    render: function() {
        this.doPromotion();
    },

    doPromotion: function() {

    },

    onChangeCount: function(event, count) {
        var detail = this.productGroup['promotion']['detail'];

        // 主商品总数量
        var products = this.productGroup['products'];
        var totalCount = 0;
        for (var i = products.length - 1; i >= 0; i--) {
            if (products[i]['isSelect']) {
                totalCount += products[i]['count'];
            }
        }

        if (totalCount < detail['count']) {
            this.$('.xa-premiumProducts').hide();
        } else {
            this.$('.xa-premiumProducts').show();
        }
        
        // 循环买赠，修改赠品数量
        if (detail['is_enable_cycle_mode']) {
            var variable = Math.floor(totalCount / detail['count']);
            var $productGroup = this.$el;
            var premiumProducts = detail['premium_products']
            for (var i = 0; i < premiumProducts.length; i++ ) {
                var premiumProduct = premiumProducts[i];
                var premiumCount = premiumProduct['premium_count'];
                if (premiumProduct['original_premium_count']) {
                    premiumCount = premiumProduct['original_premium_count'];
                }
                var premiumProductCount = variable*premiumCount;
                // console.log('premiumProductCount', premiumProductCount, variable, '*', premiumCount, 'totalCount',totalCount, "detail['count']", detail['count'])
                // console.log($productGroup, $productGroup.find('.xa-premiumProduct-'+premiumProduct['id']))
                $productGroup.find('.xa-premiumProduct-'+premiumProduct['id']).find('.xt-count').text(premiumProductCount)
            }
        }
    },

    doSelectProduct: function() {
        this.onChangeCount(this, 0)
    }
});


W.page.ShoppingCartPage = W.page.InputablePage.extend({
    events: _.extend({
        // 最近浏览
        'click .xa-showFooterprint': 'onClickShowFooterprint',
        // 全选商品
        'click .xa-checkAll': 'onClickCheckAll',
        // 选择单个商品
        'click label[name="checkbox-cart"]': 'onClickSelectProduct',
        // 清空失效商品
        // 'click .xa-cleanValidProduct': 'onClickClean',
        // 删除商品
        'click .xa-deleteBtn': 'onClickDeleteProduct',
        // 结算购物车
        'click #submit-order': 'onSubmitShopCart'
    }, W.page.InputablePage.prototype.events),
    
    initialize: function(options) {
        xlog('in ShoppingCartPage');
        // 最近浏览
        this.initFooterprintFlag();
        this.footerprintFlag = false;

        this.productGroups = options.productGroups;
        this.productGroupPriceCalculator = new W.common.ProductGroupPriceCalculator({
            el: this.el
        });


        //构建<id, product>
        this.id2product = {};
        _.each(this.productGroups, function(productGroup) {
            for(var i = 0; i < productGroup.products.length; ++i) {
                var product = productGroup.products[i];
                product.isSelect = true;
                // 以页面的count value为准
                var count = $('[data-ui-role-id="'+product.id +'-'+ product.model+'"]').val();
                product.count = parseInt(count);

                var id = productGroup.id + '-' + product.id + '-' + product.model;
                this.id2product[id] = product;
            }    
        }, this);

        // 调整数量
        this.initCounter();

        // 为price cut创建view
        var _this = this;
        this.priceCutViews = [];
        this.$('.xa-promotion-price_cut').each(function() {
            var productGroupId = parseInt($(this).data('id'));
            var productGroup = _.findWhere(_this.productGroups, {id:productGroupId})
            var view = new PriceCutView({
                el: this,
                productGroup: productGroup
            });
            view.render();
            $(this).data('view', view);
            _this.priceCutViews.push(view);
        });

        //为premium sale创建view
        this.premiumSaleViews = []
        this.$('.xa-promotion-premium_sale').each(function(){
            var productGroupId = parseInt($(this).data('id'));
            var productGroup = _.findWhere(_this.productGroups, {id:productGroupId});
            var view = new PremiumSaleView({
                el: this,
                productGroup: productGroup
            });
            view.render();
            view.onChangeCount(view, 0);
            $(this).data('view', view);
            _this.premiumSaleViews.push(view);
        });
        
        this.onClickCheckAll();
    },

    selectProduct: function($product) {
        var $productGroup = $product.parents('.xa-productGroup');
        //满减的isSelect管理已在PriceCutView中完成，这里不再需要
        var productId = $product.data('id');
        var productGroupId = $productGroup.data('id');
        var productModel = $product.data('modelName');
        var id = productGroupId + '-' + productId + '-' + productModel;
        this.id2product[id].isSelect = true;
    },

    unselectProduct: function($product) {
        var $productGroup = $product.parents('.xa-productGroup');
        //满减的isSelect管理已在PriceCutView中完成，这里不再需要
        var productId = $product.data('id');
        var productGroupId = $productGroup.data('id');
        var productModel = $product.data('modelName');
        var id = productGroupId + '-' + productId + '-' + productModel;
        this.id2product[id].isSelect = false;
    },

    initCounter: function(){
        var $counterEl = $('[data-ui-role="counter"]');
        var _this = this;
        // 多规格限购
        // var productCount = {};
        // $counterEl.each(function(i,n){
        //     if(!productCount[$(n).data('product-id')]){
        //         productCount[$(n).data('product-id')]=0;
        //     }
        //     productCount[$(n).data('product-id')]+=$(n).data('view').count;
        // });
        //库存大于购物车数量时显示库存不足
        $counterEl.each(function() {
            var $counter = $(this);
            var $product = $counter.parents('.xa-product')
            var stocks = $product.data('stocks');
            var purchase = $product.data('count-per-purchase');
            var count = $counter.val();
            if($counter.data('view').minCount>count){
                count = $counter.data('view').minCount
                $counter.val(count)
            }
            var $stockTip = $counter.parents('.xa-product').find('.xa-stockTip');
            var $check = $product.find('.xa-check');
            // 仅剩X件 提示
            if(stocks != null && stocks > 0 && (stocks < 5 || stocks < count)){
                $stockTip.html('仅剩'+stocks+'件').show();
            }else{
                $stockTip.hide();
            }

            // 库存不足提示
            var understock_msg = '';
            if(stocks != null && stocks > 0 && (stocks < 5 || stocks < count)){
                if(stocks < count){
                    $check.removeClass('xui-checkCart').addClass('xui-disabled-radio');
                    understock_msg = '库存不足'
                    _this.unselectProduct($product);
                }else{
                    $check.removeClass('xui-disabled-radio');
                }
            }
            // 限购提示
            if(purchase && purchase < count){
                $check.removeClass('xui-checkCart').addClass('xui-disabled-radio');
                understock_msg = '限购' + purchase +'件 ' + understock_msg
                _this.unselectProduct($product);
            }
            if(understock_msg){
                $product.find('.xui-understock').html(understock_msg).show();
            }else{
                $product.find('.xui-understock').hide();
            }
            $counter.bind('count-changed', _.bind(_this.onChangCounter, _this));
        });
    },

    initFooterprintFlag: function(event){
        new Swiper('.wui-swiper-container', {
            slidesPerView: 4,
            freeMode: true
        });
    },

    /**
    * onChangCounter: 调整商品数量后重新计算运费
    */
    onChangCounter: function(event){
        var $currentTarget = $(event.currentTarget)
        var counterCount = $currentTarget.val();

        var $product = $currentTarget.parents('.xa-product');
        var $productGroup = $currentTarget.parents('.xa-productGroup');        
        var stocks = $currentTarget.attr('data-max-count');
        var $stockTip = $currentTarget.parents('.xa-product').find('.xa-stockTip');
        /*
        if(stocks != null){
            if(counterCount <= stocks){
                $stockTip.addClass('hidden');
            }
        }*/

        //改变product中的count
        var productId = $product.data('id');
        var productGroupId = $productGroup.data('id');
        var productModel = $product.data('model-name');
        var id = productGroupId + '-' + productId + '-' + productModel;
        this.id2product[id].count = parseInt(counterCount);

        var priceCutView = $productGroup.data('view');
        if (priceCutView) {
            priceCutView.doPromotion();
        }

        this.calculatePrice();
    },

    /**
    * onClickShowFooterprint: 点击‘最近浏览’箭头
    */
    onClickShowFooterprint: function(event){
        if(!this.footerprintFlag){
            $(event.currentTarget).parent().css('bottom', '0px');
            this.footerprintFlag = true;
        }else{
            $(event.currentTarget).parent().css('bottom', '-145px');
            this.footerprintFlag = false;
        }
        $('.xa-arrow').toggleClass('xui-down');
    },

    /*
    * calculatePrice: 计算价格
    */
    calculatePrice: function() {
        _.each(this.priceCutViews, function(priceCutView) {
            priceCutView.doPromotion();
        });

        _.each(this.premiumSaleViews, function(premiumSaleView) {
            // 修改赠品显示数量
            premiumSaleView.doSelectProduct();
        });

        // console.log('aaaaa', this.productGroups);
        var productGroupPriceInfo = this.productGroupPriceCalculator.calculate(this.productGroups)
        var totalPrice = productGroupPriceInfo.promotionedPrice;
        var totalCount = productGroupPriceInfo.totalCount;

        //更新页面元素
        $('.xa-totalPrice').text(totalPrice.toFixed(2));
        $('.xa-total-count').text(totalCount);
    },

    /*
    * onClickCheckAll 全选响应函数
    */
    onClickCheckAll: function(){       
        var $this = $("#checkbox-cart-all");
        var $parent = $this.parent();
        var isSelect = $this.hasClass('xui-checkCart');
        if (!isSelect && $('.xa-product').length !== 0) {
            $this.addClass('xui-checkCart');
            // couldDel();
        }else{
            $this.removeClass('xui-checkCart');
            // couldNotDel();
        };

        var _this = this;
        $('label[name="checkbox-cart"]').children().each(function() {
            var $checkbox = $(this);
            var $product = $checkbox.parents('.xa-product');
            var stocks = $product.attr('data-stocks');
            if (stocks !== '-1') {
                var view = $product.find('[data-ui-role="counter"]').data('view');
                var currentCount = view.count;
                if (currentCount > stocks) {
                    return;
                }
            }

            var $product = $checkbox.parents('.xa-product');
            if (isSelect || $checkbox.hasClass('xui-disabled-radio')) {
                // 全部不选中，或者 该商品不可选择
                $checkbox.removeClass('xui-checkCart');
                _this.unselectProduct($product);
            } else {
                $checkbox.addClass('xui-checkCart');
                _this.selectProduct($product);
            }
        });

        this.calculatePrice();
    },

    /*
    * onClickSelectProduct: 选择单个商品
    */
    onClickSelectProduct: function(event){
        var $label = $(event.currentTarget);
        if ($label.children().hasClass('xui-disabled-radio')) {
            // 不可勾选的 直接跳过
            return false;
        }

        var $product = $label.parents('.xa-product');
        var stocks = $product.attr('data-stocks');
        if (stocks !== '-1') {
            var view = $product.find('[data-ui-role="counter"]').data('view');
            var currentCount = view.count;
            if (currentCount > stocks) {
                return;
            }
        }

        event.stopPropagation();
        var $product = $label.parents('.xa-product');
        var isSelect = $(event.currentTarget).children().hasClass('xui-checkCart');
        if (!isSelect) {
            $label.children().addClass('xui-checkCart');
            this.selectProduct($product);
        }else{
            $label.children().removeClass('xui-checkCart');
            this.unselectProduct($product);
        };

        var productCount = $('.xa-productContainer .xa-product').length - $('.xa-productContainer .xa-product .xui-disabled-radio').length;
        var checkedCount = $('.xa-productContainer .xui-checkCart').length;
        if (productCount == checkedCount) {
            $("#checkbox-cart-all").addClass('xui-checkCart');
        }else{
            $("#checkbox-cart-all").removeClass('xui-checkCart');           
        }

        this.calculatePrice();
    },

    /*
    * onClickDeleteProduct: 删除商品
    */
    onClickDeleteProduct: function(event){
        /*if($('.xa-productContainer').children().length == 0){            
            return;
        }*/

        var $product = $(event.currentTarget).parents('.xa-product');
        var isInvalidProduct = false;
        if ($product.length === 0) {
            $product = $(event.currentTarget).parents('.xa-invalidProduct');
            isInvalidProduct = true;
        };
        var shoppingCartItemIds = $product.data('shoppingCartId');
        var _this = this;
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            scope: this,
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'shopping_cart/delete',
                shopping_cart_item_ids: shoppingCartItemIds
            },
            success: function(data) {
                if (!isInvalidProduct) {
                    /**
                     * 普通商品
                     */
                    _this.unselectProduct($product);
                    var $productGroup = $product.parents('.xa-productGroup');

                    //删除product
                    $product.remove();
                    //如果一个group中的product都被删除，也要删除group
                    if ($productGroup.find('.xa-product').length === 0) {
                        // $productGroup.hide();
                        location.reload();
                    }
                }else{
                    /**
                     * 失效商品
                     */
                    var $invalidProductGroup = $product.parents('.xa-invalidProductInfo');
                    //删除product
                    $product.remove();
                    if ($invalidProductGroup.find('.xa-invalidProduct').length === 0) {
                        $invalidProductGroup.remove();
                    }
                }

                if($('.xa-product').length === 0 ){            
                    window.location.reload();
                } else {
                    _this.calculatePrice();
                }
            },
            error: function(data) {
                var attrDisabled = $(this).attr('disabled');
                if(attrDisabled == "disabled"){
                    $('body').alert({
                        isShow: true,
                        isError: true,
                        info: '请选择要删除的商品',
                        speed:1000
                    });
                    isSubmit = false;
                }else{
                    $('body').alert({
                        isShow: true,
                        isError: true,
                        info: '删除失败',
                        speed:1000
                    });
                    isSubmit = false;
                }
             }
        });
    },

    /*
    * onSubmitShopCart: 购物车结算
    */
    onSubmitShopCart: function(event){        
        var productIds = [];
        var productCounts = [];
        var productModelNames = [];
        $('[data-ui-role="counter"]').each(function() {
            var $counter = $(this);
            //var isCheckbox = true;
            xlog($counter);
            xlog($counter.parents('.xa-product').find('.xa-check').hasClass('xui-checkCart'));
            var isCheckbox = $counter.parents('.xa-product').find('.xa-check').hasClass('xui-checkCart');
            if (isCheckbox) {
                productIds.push($counter.attr('data-product-id'));
                productModelNames.push($counter.attr('data-product-model-name'));
                productCounts.push($counter.val());
            }
        });
        
        if(productIds.length === 0) {
            $('body').alert({
                isShow: true,
                isError: true,
                info:'请选择结算的商品',
                speed: 2000
            });
            return false;
        }

        productIds = productIds.join('_');
        productCounts = productCounts.join('_');
        productModelNames = productModelNames.join('$')
        var url = './?woid='+W.webappOwnerId+'&module=mall&model=shopping_cart_order&action=edit&product_ids='+productIds+'&product_counts='+productCounts+'&product_model_names='+productModelNames;
        window.location.href = url;
    }
});

})(W);
