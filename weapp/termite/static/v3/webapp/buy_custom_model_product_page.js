/**
 * Backbone View in Mobile
 */
W.page.BuyProductPage = BackboneLite.View.extend({
    events: {
        // 'click .xa-addCart': 'onClickModelSelectionTrigger',
        'click .xa-slidePanelShow': 'selectionSlide',
        'click .xa-coverV2,.xa-closeModelSelection': 'onCloseModelSelection',
        'click .xa-propertyValue': 'onSelectModelPropertyValue',
        'click .xa-canNotBuyButton': 'onClickCanNotBuyButton',
        'click .xa-addShoppingCartBtn': 'onClickAddShoppingCartButton',
        'click .xa-collectProduct': 'onClickCollectProductButton',
        'click .xa-property':'onClickPropertyPanel'
    },

    initialize: function(options) {
        // jz 2015-10-20
        // xlog(options);
        // this.postageFactor = options.postageFactor;
        // this.usableIntegral = options.usableIntegral;
        // this.enableTestBuy = options.enableTestBuy;
        // this.countPerPurchase = options.countPerPurchase;
        // this.productType = options.productType;
        // this.postageConfigName = options.postageConfigName;
        // this.firstStockModelName = '';
        // this.totalStocks = 0;

        this.productId = options.productId;
        this.models = options.models;
        this.minPrice = options.priceInfo.min_price;
        this.is_member_product = options.is_member_product == 'True';
        this.promotion = options.promotion || null;
        // 限购数量
        if (this.promotion && this.promotion.detail.count_per_purchase){
            this.countPerPurchase = this.promotion.detail.count_per_purchase;
        }else{
            this.countPerPurchase = -1;
        }
        if (this.promotion) {//判断促销是否为限时抢购
            this.isFlashSale = (this.promotion.type === 1)
        }

        this.targetModel = null;
        this.isStandardModelProduct = false;
        this.isSideSlideOpen = false;
        this.maxCount = -1;
        this.productCount = 1;
        //判断商品是否是标准规格商品
        if (this.models.length === 1 && this.models[0]['name'] === 'standard') {
            this.isStandardModelProduct = true;
        }

        this.getProductStock();//更新库存信息
        var _this = this;
        this.stockInterval = setInterval(this.getProductStock, 30*1000, _this);

        //绑定counter widget的count-changed事件
        $('input[data-ui-role="counter"]').bind(
            'count-changed',
            _.bind(this.onChangeProductCount, this)
        ).bind(
            'click-disabledCounter',
            _.bind(this.onClickCanNotBuyButton, this)
        ).bind(
            'reach-max-count',
            _.bind(this.showUnderStock, this)
        );
        var counter = $('input[data-ui-role="counter"]').data('view');
        if(counter.minCount>1)this.updateCountInByLink(counter.minCount)
        this.disableUnselectableModelPropertyValue();

    },



    /**
     * initForStandardModelProduct: 初始化标准规格商品界面
     */
    initForStandardModelProduct: function() {
        // this.updateWeightPostage(1);
        var maxCount = this.getMaxCount(this.targetModel);//调用getMaxCount，判断不同条件，得到可买的最大数量
        //库存
        if (this.targetModel.stock_type === 1) {//判断商品是否设置了库存
            $('.xa-stockCount').text(this.targetModel.stocks);
            $('.xa-stock').show();
        } else {
            $('.xa-stock').hide();
        }
        var counter = $('[data-ui-role="counter"]').data('view');
        counter.setMaxCount(maxCount);
        // 用于处理显示积分抵扣信息 提出单独的方法
        if($('.xa-promotion').data('type')==5){
            var price = this.targetModel.price;
            if(this.discount){
                price = price * this.discount / 100;
            }
            this.updateIntergralInfo(price);
            // var discount = $('.xa-promotion').data('discount-1');
            // if(!discount){
            //     discount = $('.xa-promotion').data('discount'+this.memberGradeId)
            // }
            // var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
            // cut_price = (price * discount / 100).toFixed(2);
            // use_integral = parseInt(cut_price * perYuanOfPerIntegral);
            // cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            // if(this.usableIntegral < use_integral){
            //     use_integral = this.usableIntegral;
            //     cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            // }
            // $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
        }
        if(this.promotion){
            if($('.xa-promotion').data('type')==5 && this.isFlashSale){
                var prodcutPrice = this.promotion.detail.promotion_price;

                this.updateIntergralInfo(prodcutPrice);
                // var discount = $('.xa-promotion').data('discount-1');
                // if(!discount){
                //     discount = $('.xa-promotion').data('discount'+this.memberGradeId)
                // }
                // var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
                // cut_price = (prodcutPrice * discount / 100).toFixed(2);
                // use_integral = parseInt(cut_price * perYuanOfPerIntegral);
                // cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                // if(this.usableIntegral < use_integral){
                //     use_integral = this.usableIntegral;
                //     cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                // }
                // $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
            }
        }
        // end用于处理显示积分抵扣信息 提出单独的方法
        if(maxCount <= 0 || counter.minCount <= maxCount){
            $('.xa-disabledBuyLinks').hide();
            $('.xa-enabledBuyLinks').show();
        }
    },

    updateIntergralInfo: function(price){
        var discount = $('.xa-promotion').data('discount-1');
        if(!discount){
            discount = $('.xa-promotion').data('discount'+this.memberGradeId)
        }
        var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
        cut_price = (price * discount / 100).toFixed(2);
        use_integral = parseInt(cut_price * perYuanOfPerIntegral);
        cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
        if(this.usableIntegral < use_integral){
            use_integral = this.usableIntegral;
            cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
        }
        $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
    },

    /**
     * getMaxCount
     */
    getMaxCount: function(model){
        var maxCount = 0;
        var message = '';

        if (model.stock_type === 1) {
            /* 有限 */
            if (this.countPerPurchase > 0 && this.countPerPurchase < model.stocks) {
                /* 限购数量大于0并且小于库存时 */
                maxCount = this.countPerPurchase;
                message = '限购'+ maxCount +'件';
            }else{
                maxCount = model.stocks;
                message = '库存不足';
            }
        } else {
            /* 无限 */
            if (this.countPerPurchase > 0) {
                /* 限购数量大于0时 */
                maxCount = this.countPerPurchase;
                message = '限购'+ maxCount +'件';
            }else{
                maxCount = -99999;
            }
        }

        this.maxCount = maxCount;
        // 修改提示信息
        $('.xa-understock').text(message);
        return maxCount;
    },

    /**
     * getCustomModelStocks: 获得规格值对应的商品库存
     */
    // getCustomModelStocks:function(model){
    //     // 过滤 默认standard
    //     if (model.name === 'standard') {
    //         return {
    //             isShowStocks:true
    //         }
    //     }


    //     if(parseInt(model.stock_type) == 0){
    //         return {
    //             isShowStocks: false
    //         }
    //     }else{
    //         // this.totalStocks += model.stocks;
    //         return {
    //             isShowStocks:true
    //         }
    //     }
    // },
     /**
     * initForCustomModelProduct: 初始化用户定制规格商品界面
     */
    initForCustomModelProduct: function() {
        $('input[data-ui-role="counter"]').data('view').setMaxCount(0).disable();
        // var stocks = $('.xa-stock');
        // var checkResult = {};
        // for (var i = 0; i < this.models.length; i++) {
        //     var model = this.models[i];
        //     checkResult = this.getCustomModelStocks(model);//计算所有规格的总库存
        //     if (!checkResult.isShowStocks) {
        //         this.totalStocks = 0;
        //         break;
        //         // return false;
        //     }
        // };
        // if (checkResult.isShowStocks) {
            // $('.xa-stockCount').text(this.totalStocks);
        //     stocks.show();
        // }else{
        //     stocks.hide();
        // }


        // 用于处理显示限时抢购信息
        if($('.xa-promotionNormal').data('type')==1){
            var promotionPrice = this.promotion.detail.promotion_price;
            var gapPrice = (this.minPrice - promotionPrice).toFixed(2);
            $('.xa-promotionNormal-info').text('已优惠' + gapPrice + '元')
        }
        // 用于处理显示积分抵扣信息 提出单独的方法
        if($('.xa-promotion').data('type')==5){
            var price = this.minPrice;
            if(this.discount){
                price = price * this.discount / 100;
            }
            this.updateIntergralInfo(price);
            // var discount = $('.xa-promotion').data('discount-1');
            // if(!discount){
            //     discount = $('.xa-promotion').data('discount'+this.memberGradeId)
            // }
            // var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
            // cut_price = (price * discount / 100).toFixed(2);
            // use_integral = parseInt(cut_price * perYuanOfPerIntegral);
            // cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            // if(this.usableIntegral < use_integral){
            //     use_integral = this.usableIntegral;
            //     cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            // }
            // $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
        }
        if(this.promotion){
            if($('.xa-promotion').data('type')==5 && this.isFlashSale){
                var prodcutPrice = this.promotion.detail.promotion_price;
                this.updateIntergralInfo(prodcutPrice);
                // var discount = $('.xa-promotion').data('discount-1');
                // if(!discount){
                //     discount = $('.xa-promotion').data('discount'+this.memberGradeId)
                // }
                // var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
                // cut_price = (prodcutPrice * discount / 100).toFixed(2);
                // use_integral = parseInt(cut_price * perYuanOfPerIntegral);
                // cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                // if(this.usableIntegral < use_integral){
                //     use_integral = this.usableIntegral;
                //     cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                // }
                // $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
            }
        }
        // end用于处理显示积分抵扣信息 提出单独的方法
    },
    /**
    更新models中的商品库存的信息
    */
    getProductStock: function(_this) {
        var isInit = 0;
        if (!_this) {
            isInit = 1;
            _this = this;
        }
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'product_stocks/get',
                product_id: this.productId,
                need_member_info: isInit
            },
            success: function(data){
                //处理规格库存
                var stock_all = 0;
                $.each(_this.models, function(i, n){
                    if(!data[n.id])
                        return;
                    n.stock_type = data[n.id].stock_type;
                    if(n.stock_type == 0){
                        stock_all = 999999;//无限库存
                    }else{
                        stock_all += n.stocks
                    }
                    if(stock_all==0){
                        $('.xa-selloutAlert').show();
                        $('.xa-not_selloutAlert').hide();
                    }else{
                        $('.xa-not_selloutAlert').show();
                        $('.xa-selloutAlert').hide();
                    }
                    n.stocks = data[n.id].stocks;
                    if(n.stock_type == 0){
                        stock_all = 999999;//无限库存
                    }else{
                        stock_all += n.stocks
                    }
                    if(stock_all==0){
                        $('.xa-selloutAlert').show();
                        $('.xa-not_selloutAlert').hide();
                    }else{
                        $('.xa-not_selloutAlert').show();
                        $('.xa-selloutAlert').hide();
                    }
                    if(_this.targetModel && _this.targetModel.id == n.id){
                        //更新库存
                        _this.updateProductStock(n);
                    }
                });

                if(isInit){
                    _this.usableIntegral = data.usable_integral
                    _this.memberGradeId = data.member_grade_id
                    if (_this.isStandardModelProduct) {
                        _this.targetModel = _this.models[0];
                        _this.initForStandardModelProduct();
                    } else {
                        _this.initForCustomModelProduct();
                    }
                    var user_member_grade_id = data.member_grade_id;
                    if(data.is_collect == 'true'){
                        $('.xa-collectProduct').addClass('faved').text('已收藏');
                        $('.xa-collectProduct').attr('data-is-collect', 'true');
                    }
                    if(data.count != 0) {
                        $('.xa-shoppingCartCount').text(data.count).removeClass("hidden");
                    }
                    // 优惠信息标签
                    var msg = '';
                    // 商品原价
                    var price = _this.minPrice;
                    // 存储商品会员价与促销的状态
                    _this.member_or_promotion = '';
                    // 商品有促销
                    var product_promotion = _this.promotion;
                    var is_user_has_promotion = false;
                    if(!($.isEmptyObject(product_promotion))){
                        // 促销是否对此用户开放
                        is_user_has_promotion = product_promotion.member_grade_id == 0 || product_promotion.member_grade_id == user_member_grade_id;

                        // 限时抢购
                        if(is_user_has_promotion && product_promotion.detail.promotion_price){
                            price = (product_promotion.detail.promotion_price).toFixed(2);
                            msg = true;
                            _this.member_or_promotion = 'promotion';
                        }
                        if(!is_user_has_promotion){
                            _this.isFlashSale = false;
                            $('.xt-masterPromotionTile').remove()
                            // 促销不对此用户开发
                            var next_promotions = $('.xa-display-promotion').next('div');
                            if(next_promotions.length==0){
                                // 没有积分应用
                                $('.xa-promotionSection').remove();
                            }else if(next_promotions.length == 1){
                                // 有积分应用
                                $('.xa-display-promotion').html(next_promotions.html()).find('div:first').html('优惠：');
                                next_promotions.remove();
                            }

                        }
                    // 商品无促销
                    }
                    $('.xt-promotionTile:first').show();
                    if(!is_user_has_promotion){
                        // 商品是否折扣
                        has_discount = _this.is_member_product;
                        if(has_discount && data.discount < 100){
                            //促销与会员价格处理
                            _this.discount = data.discount;
                            if(_this.isStandardModelProduct){
                                _this.initForStandardModelProduct()
                            }else{
                                _this.initForCustomModelProduct()
                            }
                            price = ((price * data.discount / 100).toFixed(2));
                            msg = '会员价';
                            _this.member_or_promotion = 'member';

                        }
                        // 对于不开放的促销，不显示广告语
                        // var span = $('.xa-productName').find('span');
                        // if(span){

                        //     span.html('<span class="xui-text-red">'+_this.priceInfo.promotion_title+'</span>');
                        // }
                    }
                    // 处理会员价
                    if (msg === true){
                        var temp = '<span class="xui-vipPrice-num em85">￥<span class="xa-price xa-singlePrice fb em1" data-display-price="'+price+'">'+ price +'</span></span>';
                        $('.xa-priceSection').html(temp);

                    }else if(msg === '会员价'){
                        var orPrice = (_this.minPrice).toFixed(2);
                        var temp = '<span class="xui-memberPriceTag">'+msg+'</span><span class="xui-vipPrice-num em85">￥<span class="xa-price xa-singlePrice fb em1" data-display-price="'+price+'">'+ price +'</span></span><span class="xui-orPrice">原价￥<span class="xa-orPrice" data-orPrice="'+orPrice+'">'+ orPrice +'</span></span>';
                        $('.xa-priceSection').html(temp);
                    }
                    if(data.is_subscribed){
                        $('.xa-collectProduct').show();
                    }else{// 非会员
                        var alertView = $('[data-ui-role="attentionAlert"]').data('view');
                        if(alertView){
                            alertView.render();
                        }
                        $('.xui-productInfoBox').css('margin-right', 0)
                        $($('.xa-globalNav li')[1]).hide();
                        $('.xa-collectProduct').remove();
                    }
                }

            },
            error: function(){
                console.log("error");
            }
        })
    },

    /**
     * selectionSlide: 规格触发器弹出效果
     */
    selectionSlide: function(event){
        var $slidePanel = $('.xa-upSlidePanel');
        if(!this.isSideSlideOpen){
            $slidePanel.css({
                '-webkit-transform':'translateY(0)',
                '-moz-transform':'translateY(0)',
                'transform':'translateY(0)'
            });
            $('.xa-coverV2').removeClass('hidden');
            this.isSideSlideOpen = true;
        }else{
            $slidePanel.css({
                '-webkit-transform':'translateY(110%)',
                '-moz-transform':'translateY(110%)',
                'transform':'translateY(110%)'
            });
            $('.xa-coverV2').addClass('hidden');
            this.isSideSlideOpen = false;

        }
    },
    /**
     * onClickPropertyPanel: 点击详情参数按钮的响应函数
     */
    onClickPropertyPanel:function(event){
        var $arrow = $(event.target).children('span');
        var $panel = $(event.target).siblings('ul');
        flag = $panel.hasClass('hidden');
        if(flag){
            $panel.removeClass('hidden');
            $arrow.addClass('xui-up');
        }else{
            $panel.addClass('hidden');
            $arrow.removeClass('xui-up');
        }

    },
    /**
     * onClickModelSelectionTrigger: 点击选择规格触发器（“购买”，“加入购物车”）按钮的响应函数
     */
    // onClickModelSelectionTrigger: function(event) {
    //     this.selectionSlide();
    //     var actionType = $(event.target).data('type');
    //     var buttonTop = $('.xui-productInfo').height()-28;
    //     if (actionType === 'buy'){
    //         $('.xa-shoppingCartButton').hide();
    //         $('.xa-buyButton').show();
    //     }else{
    //         $('.xa-shoppingCartButton').show();
    //         $('.xa-buyButton').hide();
    //     }

    // },

    /**
     * onCloseModelSelection: 点击关闭规格选择触发器的响应函数
     */
    onCloseModelSelection: function(event) {
        if (this.isSideSlideOpen) {
            this.selectionSlide();
        };
    },
    /**
     * onChangeProductCount: counter widget的count-change event的响应函数
     */
    onChangeProductCount: function(event, value) {
        var $purchaseCount =$(event.target).parents('.xui-page').find('.xa-purchaseCount');
        $purchaseCount.text(value);

        this.updateCountInByLink(value);
        // this.updateWeightPostage(value);
        this.productCount = value;
        this.hideUnderStock(value);
    },

    /**
     * 显示库存vs限购 不足 提示
     */
    showUnderStock: function(){
        $('.xa-understock').show();
    },

    /**
     * 隐藏库存vs限购 不足 提示
     */
    hideUnderStock: function(value){
        $('.xa-understock').hide();
    },

    /**
     * getPostageForWeight: 计算运费
     */
    // getPostageForWeight: function(weight) {
    //     if(!isNaN(weight)){//事实上判断了是否是包邮产品
    //         if (weight <= postageFactor.firstWeight) {//不满首重，则返回首重的价钱
    //             return postageFactor.firstWeightPrice;
    //         }

    //         if (!postageFactor.isEnableAddedWeight) {//无续重，也返回首重的价钱
    //             return postageFactor.firstWeightPrice;
    //         }

    //         weight = weight - postageFactor.firstWeight;//续重的重量
    //         var price = postageFactor.firstWeightPrice;
    //         var addedWeight = parseFloat(postageFactor.addedWeight);

    //         //added by chuter
    //         if (addedWeight == 0) {
    //             return price;
    //         }

    //         var addedCount = 1;
    //         while (true) {
    //             weight = weight - addedWeight;
    //             if (weight <= 0) {
    //                 break;
    //             } else {
    //                 addedCount += 1;
    //             }
    //         }
    //         var addedPrice = addedCount * postageFactor.addedWeightPrice;
    //         return price + addedPrice;
    //     }
    //     return 0;
    // },

    /**
     *updateWeightPostage: 更新重量和邮费
     */
    // updateWeightPostage: function(productCount) {
    //     //更新价钱
    //     var totalPrice = (this.targetModel.price*productCount).toFixed(2);
    //     $('.xa-variablePrice').text(totalPrice);
    // },

    updateProductInfo: function(model) {//更新DOM，使用在选中和释放规格值时
        if (!model) {
            // alert(this.isFlashSale)
            if (!this.promotion || !this.isFlashSale) {
                var min_price = (this.minPrice).toFixed(2);
                alert(min_price)
                if (this.discount){
                    $('.xa-orPrice').text(min_price);
                    min_price = (min_price * this.discount / 100).toFixed(2);
                }
                $('.xa-singlePrice').text(min_price);
            }
            // $('.xa-market-price').text(this.priceInfo['display_market_price']);
            $('.xa-enabledBuyLinks').hide();
            $('.xa-disabledBuyLinks').show();
            $('.xa-disabledIntegralBuyLinks').hide();
            // var items = [];
            // items.push('重量：<span class="xt-weight"> - </span><span class="xt-single-weight" style="display: none"> - </span></span>&nbsp;&nbsp;');
            // items.push('<span class="xt-postageConfigName ml20">'+this.postageConfigName+'</span>');
            // items.push(':<span class="xt-postage"> - </span>');
            // $('.xa-postageContent').html(items.join(''));
            // $('.xa-postage').show();

            //库存
            $('[data-ui-role="counter"]').data('view').setMaxCount(0);
        } else {
            var change_price = 0;
            if (this.promotion && this.isFlashSale) {
                //do nothing
                if (this.promotion.type == 1 && this.member_or_promotion === 'promotion') {
                    change_price = this.promotion.detail.promotion_price.toFixed(2); //无规格时，显示抢购的价钱
                }else if (this.promotion.type == 1 && this.member_or_promotion === 'member') {
                    change_price = model.price.toFixed(2); //无规格时，显示抢购的价钱
                }else{
                    change_price = model.price.toFixed(2);//无规格时，显示抢购的价钱
                }
            } else {
                change_price = model.price.toFixed(2);
            }
            if(this.discount < 100){
                $('.xa-orPrice').text(change_price);
                change_price = (change_price * this.discount / 100).toFixed(2);
            }
            $('.xa-singlePrice').text(change_price);
            this.updateProductStock(model);
        }
    },
    /**
     * 只对targetModel执行
     * @param model
     */
    updateProductStock: function(model){
        if (!this.targetModel) {
            // 如果没有选中规格，则不处理
            return;
        }
        var counter = $('[data-ui-role="counter"]').data('view');
        //库存
        var maxCount = this.getMaxCount(model);
        counter.setMaxCount(maxCount);

        if(counter.maxCount >= 0 && (counter.maxCount < counter.count || counter.maxCount < counter.minCount)){
            this.showUnderStock();
            $('.xa-disabledBuyLinks').show();
            $('.xa-enabledBuyLinks').hide();
        }else{
            this.hideUnderStock();
            $('.xa-disabledBuyLinks').hide();
            $('.xa-enabledBuyLinks').show();
        }
    },

    /**
     * updateModelInBuyLink: 更新购买链接中的商品规格信息
     */
    updateModelInBuyLink: function(model) {//将商品的相关信息放到URL中，传到后台
        if (model === null) {
            return;
        }
        var $buy = $('.xa-buyBtn');
        $('.xa-buyBtn').each(function(){
            $buy = $(this);
            var hrefAttr = $buy.attr('href');
            hrefAttr = hrefAttr.replace(/product_model_name=.*$/, 'product_model_name='+model.name);
            $buy.attr('href', hrefAttr);
        });
    },

    /**
     * updateCountInByLink: 修改“购买”链接中的product_count参数
     */
    updateCountInByLink: function(productCount) {
        var $buy = $('.xa-buyBtn');
        $('.xa-buyBtn').each(function(){
            $buy = $(this);
            var hrefAttr = $buy.attr('href');
            hrefAttr = hrefAttr.replace(/product_count=\d+/, 'product_count='+productCount);
            $buy.attr('href', hrefAttr);
        });
    },

    /**
     * disableUnselectableModelPropertyValue: 禁用不可使用的规格属性值
     */
    disableUnselectableModelPropertyValue: function() {
        // 已被选中的规格值
        var selectedPropertyValues = [];
        $('.xui-inner-selected-tag').each(function() {
            selectedPropertyValues.push($(this).attr('name'));
        });
        // xlog(selectedPropertyValues)
        var _this = this;
        $('.xa-propertyValue').each(function() {// 遍历所有规格值
            var name = $(this).attr('name'), propertyId = name.split(':')[0];
            // 当前规格值需要的检查规格值列表，包括当前规格和其他规格名下已选的规格值
            var checkPropertyValues = [name];
            _.each(selectedPropertyValues, function(selectedPropertyValue){
                if(selectedPropertyValue.split(':')[0] != propertyId)
                    checkPropertyValues.push(selectedPropertyValue)
            })
            // 当前规格值是否可选
            var isCanSelect = false;
            _.each(_this.models, function(model) {
                if(isCanSelect)
                    return
                if(model.stock_type == 1 && model.stocks <= 0)// 库存为零
                    return

                // 有一个可用的(库存无线或者大于0)商品规格，包含所有的检查规格值，当前规格可以选择
                var count = 0;
                _.each(checkPropertyValues, function(checkPropertyValue){
                    if(model.name.indexOf(checkPropertyValue) >= 0)
                        count += 1;
                });
                if(count == checkPropertyValues.length)
                    isCanSelect = true;
            })
            if (isCanSelect) {
                $(this).removeClass('xui-unSelectable');
            } else {
                $(this).removeClass('xui-inner-selected-tag').addClass('xui-unSelectable');
            }
        });
    },

    /**
     * getSelectedModel: 获取选中的有效规格
     */
    getSelectedModel: function() {
        var ids = [];
        $('.xui-inner-selected-tag').each(function() {
            var $propertyValue = $(this);
            var id = $propertyValue.attr('data-property-value-id');
            ids.push(id);
        });

        _.sortBy(ids, function(id) { return id; });
        var name = ids.join('_');
        var targetModel = null;
        _.each(this.models, function(model) {
            if (model.name === name) {
                targetModel = model;
            }
        });
        return targetModel;
    },

    /**
     * onSelectModelPropertyValue: counter widget的count-change event的响应函数
     */
    onSelectModelPropertyValue: function(event) {
        var $propertyValue = $(event.currentTarget);
        if ($propertyValue.hasClass('xui-unSelectable')) {
            return;
        }

        var currentModelPropertyValue = $propertyValue.attr('name');
        var currentModelPropertyValueText =  $propertyValue.text()
        var propertyId = currentModelPropertyValue.split(':')[0];
        var currentModelPropertyValueName = $propertyValue.attr('data-property-value-name');
        var $modelValueText = $('[data-property-id="'+propertyId+'"]');
        // var $selectModelHint = $('.xa-selectedModelHint');

        //增加取消选择
        var isSelectPropertyValue = true;
        if ($propertyValue.hasClass('xui-inner-selected-tag')) {
            $propertyValue.removeClass('xui-inner-selected-tag');
            isSelectPropertyValue = false;
            $modelValueText.text($modelValueText.attr('data-property-name')).removeClass('xui-text-red').show();
        } else {
            $propertyValue.parents('.xui-i-customModel').find('.xui-inner-selected-tag').removeClass('xui-inner-selected-tag');
            $propertyValue.toggleClass('xui-inner-selected-tag');
            $modelValueText.text(currentModelPropertyValueName);
        }

        //根据选择结果更新页面
        var currentModelPropertyValue = $propertyValue.attr('name');

        this.targetModel = this.getSelectedModel();
        if (this.targetModel) {
            //启用counter
            var counter = $('input[data-ui-role="counter"]').data('view').enable();
            $('.xa-purchaseCount').text(1);
            //如果选中了合法的商品规格组合，更新商品信息
            this.disableUnselectableModelPropertyValue();
            this.updateProductInfo(this.targetModel);
            this.updateModelInBuyLink(this.targetModel);
            //显示选中的规格值
            $('.xa-selectedModelPropertyValueName').show();
            counter.reset();
        } else {
            $('input[data-ui-role="counter"]').data('view').disable();
            $('.xa-purchaseCount').text("数量");
            this.updateProductInfo();
            // 显示所有库存数量
            // if (this.totalStocks > 0) {
            //     $('.xa-stockCount').text(this.totalStocks);
            //     $('.xa-stock').show();

            // }
            if (isSelectPropertyValue) {
                this.disableUnselectableModelPropertyValue(currentModelPropertyValue);
            } else {
                this.disableUnselectableModelPropertyValue();
            }
        }
    },

    /**
     * onClickCanNotBuyButton: 点击disable区域的“购买”按钮的响应函数
     */
    onClickCanNotBuyButton: function(event) {
        var counter = $('input[data-ui-role="counter"]').data('view');
        var msg = '';
        if(counter.maxCount>0 && counter.maxCount<counter.count ||counter.maxCount ==counter.count&&counter.count==0&&counter.maxCount<counter.minCount&&this.targetModel){
            msg = '库存不足';
        }else if(!this.isSideSlideOpen){
            this.selectionSlide();
        }else{
            var msg = '请先选择商品规格';
        }
        if(msg != ''){
            $('body').alert({
                isShow: true,
                info: msg,
                isSlide: true,
                speed: 1500
            });
        }
    },

    /**
     * onClickAddShoppingCartButton: 点击"加入购物车"按钮的响应函数
     */
    onClickAddShoppingCartButton: function(event) {
        var _this = this
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'shopping_cart/add',
                count: this.productCount,
                product_id: this.productId,
                product_model_name: this.targetModel.name
            },
            success: function(data) {
                $('body').alert({
                    isShow: true,
                    isSlide: true,
                    info:'加入购物车成功',
                    speed:2000
                });
                if(data.shopping_cart_product_nums) {
                    var $btnCart = $('.xui-shoppingCartBtn .xui-inner-count');
                    $btnCart.css('display', 'inline-block').text(data.shopping_cart_product_nums).removeClass('hidden');
                };

                _this.onCloseModelSelection();
            },
            error: function(resp) {
                var errMsg = '加入购物车失败'
                if (resp.errMsg) {
                    errMsg = resp.errMsg;
                }
                $('body').alert({
                    isShow: true,
                    isSlide: true,
                    info: errMsg,
                    speed: 3000
                });
            }
        });
    },

    onClickCollectProductButton: function(event) {
        var _this = this;
        var is_collect = $('.xa-collectProduct').data('is-collect');
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'wishlist_product/update',
                product_id: this.productId,
                is_collect: is_collect
            },
            success: function(data) {
                if(is_collect){
                    $('.xa-collectProduct').removeClass('faved').text('收藏');
                    $('.xa-collectProduct').attr('data-is-collect','false');
                }else{
                    $('.xa-collectProduct').addClass('faved').text('已收藏');
                    $('.xa-collectProduct').attr('data-is-collect', 'true');
                }
            },
            error: function(resp) {
                var errMsg = '收藏失败'
                if (resp.errMsg) {
                    errMsg = resp.errMsg;
                }
                $('body').alert({
                    isShow: true,
                    isSlide: true,
                    info: errMsg,
                    speed: 3000
                });
            }
        });
    }
});
