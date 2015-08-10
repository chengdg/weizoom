/**
 * Backbone View in Mobile
 */
W.page.BuyProductPage = BackboneLite.View.extend({
    events: {
        'click .xa-addCart': 'onClickModelSelectionTrigger',
        'click .xa-slidePanelShow': 'selectionSlide',
        'click .xa-coverV2,.xa-closeModelSelection': 'onCloseModelSelection',
        'click .xa-propertyValue': 'onSelectModelPropertyValue',
        'click .xa-canNotBuyButton': 'onClickCanNotBuyButton',
        'click .xa-addShoppingCartBtn': 'onClickAddShoppingCartButton',
        'click .xa-collectProduct': 'onClickCollectProductButton',
        'click .xa-property':'onClickPropertyPanel'
    },

    initialize: function(options) {
        xlog(options);
        this.postageFactor = options.postageFactor;
        this.usableIntegral = options.usableIntegral;
        this.enableTestBuy = options.enableTestBuy;

        // 限购数量
        this.countPerPurchase = options.countPerPurchase;

        this.totalStocks = 0;
        this.firstStockModelName = '';
        this.productId = options.productId;
        this.productType = options.productType;
        this.postageConfigName = options.postageConfigName;
        this.models = options.models;
        this.isStandardModelProduct = false;
        this.priceInfo = options.priceInfo;
        this.targetModel = null;
        this.isSideSlideOpen = false;
        this.maxCount = -1;
        this.promotion = options.promotion || null;
        this.is_member_product = options.is_member_product == 'True'

        if (this.promotion) {//判断促销是否为限时抢购
            this.promotion.isFlashSalePromotion = (this.promotion.type === 1)
        }

        this.productCount = 1;
        //判断商品是否是标准规格商品
        if (this.models.length === 1 && this.models[0]['name'] === 'standard') {
            this.isStandardModelProduct = true;
        }

        this.getProductStock();//更新库存信息

        var _this = this;
        this.stockInterval = setInterval(this.getProductStock, 60*1000, _this);

        //设置规格选择区域的最大高度
        // var boxHeight = window.document.body.clientHeight * 0.75;
        // var buttonTop = $('.xui-productInfo-box').height();
        // console.log($('.xui-productInfo').height(),111)
        // $('.xui-productInfo-box').css('max-height', boxHeight);
        // 关闭按钮兼容不同手机定位
        // if (/ipad|iphone|mac/i.test(navigator.userAgent)){
        //     $('.xa-closeModelSelection').css({'position':'absolute','top':5});
        // }else{
        //     $('.xa-closeModelSelection').css({'position':'fixed','bottom':boxHeight-28});
        // }

        // this.initStickyActionBar();

        //启用"测试购买"的情况下，增加"价格区域"的padding-bottom
        if (this.enableTestBuy) {
            $('.xa-priceSection').css('padding-bottom', '115px');
        }

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

        //隐藏商品信息区域
        // var screenHeight = screen.height;

        // $('.xui-applyBox').css({
        //     top: screenHeight
        // });
        // if (this.promotion && this.promotion.isFlashSalePromotion) {
        //     W.getApi().call({
        //         app: 'webapp',
        //         api: 'project_api/call',
        //         method: 'get',
        //         args: {
        //             woid: W.webappOwnerId,
        //             module: 'mall',
        //             target_api: 'shopping_cart_product_ids/get'
        //         },
        //         success: function(data) {
        //             xlog(data);
        //             xlog(productId);
        //         },
        //         error: function(resp) {

        //         }
        //     });
        // }
    },



    /**
     * initForStandardModelProduct: 初始化标准规格商品界面
     */
    initForStandardModelProduct: function() {
        this.updateWeightPostage(1);
        var maxCount = this.getMaxCount(this.targetModel);//调用getMaxCount，判断不同条件，得到可买的最大数量
        xlog('set max count to ' + maxCount);
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
            var discount = $('.xa-promotion').data('discount').replace('%', '')/ 100;
            var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
            cut_price = (this.targetModel.price * discount).toFixed(2);
            use_integral = parseInt(cut_price * perYuanOfPerIntegral);
            cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            if(this.usableIntegral < use_integral){
                use_integral = this.usableIntegral;
                cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            }
            $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
        }
        if(this.promotion){
            if($('.xa-promotion').data('type')==5 && this.promotion.isFlashSalePromotion){
                var prodcutPrice = this.promotion.detail.promotion_price;
                var discount = $('.xa-promotion').data('discount').replace('%', '')/ 100;
                var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
                cut_price = (prodcutPrice * discount).toFixed(2);
                use_integral = parseInt(cut_price * perYuanOfPerIntegral);
                cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                if(this.usableIntegral < use_integral){
                    use_integral = this.usableIntegral;
                    cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                }
                $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
            }
        }
        // end用于处理显示积分抵扣信息 提出单独的方法
        if(maxCount <= 0 || counter.minCount <= maxCount){
            $('.xa-disabledBuyLinks').hide();
            $('.xa-enabledBuyLinks').show();
        }
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
        // console.log('getMaxCount', maxCount, message);
        return maxCount;
    },

    /**
     * getCustomModelStocks: 获得规格值对应的商品库存
     */
    getCustomModelStocks:function(model){
        // 过滤 默认standard
        if (model.name === 'standard') {
            return {
                isShowStocks:true
            }
        }

        // 第一个有库存的 规格商品
        // if ((model.stock_type === 0 || model.stocks > 0) && this.firstStockModelName == '') {
        //     this.firstStockModelName = model.name;
        // }

        if(parseInt(model.stock_type) == 0){
            return {
                isShowStocks: false
            }
        }else{
            this.totalStocks += model.stocks;
            return {
                isShowStocks:true
            }
        }
    },
     /**
     * initForCustomModelProduct: 初始化用户定制规格商品界面
     */
    initForCustomModelProduct: function() {
        $('input[data-ui-role="counter"]').data('view').setMaxCount(0).disable();
        //console.log($('.xa-wrapper'));
        var stocks = $('.xa-stock');
        var checkResult = {};
        for (var i = 0; i < this.models.length; i++) {
            var model = this.models[i];
            checkResult = this.getCustomModelStocks(model);/*计算所有规格的总库存*/
            if (!checkResult.isShowStocks) {
                this.totalStocks = 0;
                break;
                // return false;
            }
        };
        if (checkResult.isShowStocks) {
            $('.xa-stockCount').text(this.totalStocks);
            stocks.show();
        }else{
            stocks.hide();
        }

        // 默认选中第一个有效规格
        // var modelNames = this.firstStockModelName.split('_');
        // for (var i = 0; i < modelNames.length; i++) {
        //     var $el = $('a[data-property-value-id="'+modelNames[i]+'"]');
        //     $el.click(_.bind(this.onSelectModelPropertyValue, this)).trigger("click");
        //     $el.unbind("click");
        // };

        // 用于处理显示限时抢购信息
        if($('.xa-promotionNormal').data('type')==1){
            var minPrice = this.priceInfo.min_price;
            var promotionPrice = this.promotion.detail.promotion_price;
            var gapPrice = (minPrice - promotionPrice).toFixed(2);
            $('.xa-promotionNormal-info').text('已优惠' + gapPrice + '元')
        }
        // 用于处理显示积分抵扣信息 提出单独的方法
        if($('.xa-promotion').data('type')==5){
            var discount = $('.xa-promotion').data('discount').replace('%', '')/ 100;
            var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
            cut_price = (this.priceInfo.min_price * discount).toFixed(2);
            use_integral = parseInt(cut_price * perYuanOfPerIntegral);
            cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            if(this.usableIntegral < use_integral){
                use_integral = this.usableIntegral;
                cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
            }
            $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
        }
        if(this.promotion){
            if($('.xa-promotion').data('type')==5 && this.promotion.isFlashSalePromotion){
                var prodcutPrice = this.promotion.detail.promotion_price;
                var discount = $('.xa-promotion').data('discount').replace('%', '')/ 100;
                var perYuanOfPerIntegral = $('.xa-promotion').data('per-yuan');
                cut_price = (prodcutPrice * discount).toFixed(2);
                use_integral = parseInt(cut_price * perYuanOfPerIntegral);
                cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                if(this.usableIntegral < use_integral){
                    use_integral = this.usableIntegral;
                    cut_price = (use_integral / perYuanOfPerIntegral).toFixed(2);
                }
                $('.xa-promotion').parents('.xa-promotionSection').find('.xa-intergralInfo').text('最多可使用'+ use_integral +'积分，抵扣'+ cut_price +'元');
            }
        }
        // end用于处理显示积分抵扣信息 提出单独的方法
    },
    /**
    更新models中的商品库存的信息
    */
    getProductStock: function(_this) {
        var isInit = 0;
        if (_this) {
        }else {
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
            },
            success: function(data){
                if (_this.isStandardModelProduct) {
                    _this.models[0].stock_type = data.stock_type;
                    _this.models[0].stocks = data.stocks;
                    _this.targetModel = _this.models[0];
                    _this.initForStandardModelProduct();
                    // _this.getMaxCount(_this.models[0]); 多余操作 initForStandardModelProduct 已经执行过
                } else {
                    for(var i = 0; i < _this.models.length; i++){
                        _this.models[i].stock_type = data[_this.models[i].id].stock_type;
                        _this.models[i].stocks = data[_this.models[i].id].stocks;
                        if(!isInit){
                            _this.updateProductInfo(_this.models[i]);
                        }
                    }
                    if (isInit){
                        _this.initForCustomModelProduct();
                    }
                }
                // var counter = $('input[data-ui-role="counter"]').data('view');
                // if(counter.count > 1){
                //     counter.changeCountTo(counter.count);
                // }
            },
            error: function(){
                console.log("error");
            }
        })
    },
    /**
     * initStickyActionBar: 初始化粘性action bar
     */
    initStickyActionBar: function() {
        // var $wxTab= $('.xa-tab');
        // var wxTab = $wxTab[0];
        // var wxTabOffsetTop = wxTab.offsetTop;
        // var isTabFixed = $wxTab.hasClass('.xui-tab-fixed');
        // $(document).on('touchmove scroll', function () {
        //     if (window.scrollY > wxTabOffsetTop) {
        //         if (!isTabFixed) {
        //             $wxTab.addClass('xui-tab-fixed');
        //             isTabFixed = true;
        //         }
        //     } else {
        //         if (isTabFixed) {
        //             $wxTab.removeClass('xui-tab-fixed');
        //             isTabFixed = false;
        //         }
        //     }
        // });
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
            //释放选中规格
            // if (this.isStandardModelProduct == false) {
            //     var _this = this;
            //     $('.xa-propertyValue').removeClass('xui-inner-selected-tag').removeClass('xui-unSelectable');
            //     // $('.xa-selectedModelHint').text('请选择');
            //     $('.xa-selectedModelPropertyValueName').each(function() {
            //         var $span = $(this);
            //         $span.text($span.attr('data-property-name')).removeClass('xui-text-red').show();
            //     })
            //     _this.updateProductInfo();
            // };
            this.isSideSlideOpen = false;
            // $('[data-ui-role="counter"]').data('view').setMaxCount(0);
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
    onClickModelSelectionTrigger: function(event) {
        this.selectionSlide();
        var actionType = $(event.target).data('type');
        var buttonTop = $('.xui-productInfo').height()-28;
        if (actionType === 'buy'){
            $('.xa-shoppingCartButton').hide();
            $('.xa-buyButton').show();
        }else{
            $('.xa-shoppingCartButton').show();
            $('.xa-buyButton').hide();
        }

        // if (/ipad|iphone|mac/i.test(navigator.userAgent)){
        //     $('.xa-closeModelSelection').css({'position':'absolute','top':5});
        // }else{
        //     $('.xa-closeModelSelection').css({'position':'fixed','bottom':buttonTop});
        // }
    },

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
        this.updateWeightPostage(value);
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
    getPostageForWeight: function(weight) {
        if(!isNaN(weight)){//事实上判断了是否是包邮产品
            if (weight <= postageFactor.firstWeight) {//不满首重，则返回首重的价钱
                return postageFactor.firstWeightPrice;
            }

            if (!postageFactor.isEnableAddedWeight) {//无续重，也返回首重的价钱
                return postageFactor.firstWeightPrice;
            }

            weight = weight - postageFactor.firstWeight;//续重的重量
            var price = postageFactor.firstWeightPrice;
            var addedWeight = parseFloat(postageFactor.addedWeight);

            //added by chuter
            if (addedWeight == 0) {
                return price;
            }

            var addedCount = 1;
            while (true) {
                weight = weight - addedWeight;
                if (weight <= 0) {
                    break;
                } else {
                    addedCount += 1;
                }
            }
            var addedPrice = addedCount * postageFactor.addedWeightPrice;
            return price + addedPrice;
        }
        return 0;
    },

    /**
     *updateWeightPostage: 更新重量和邮费
     */
    updateWeightPostage: function(productCount) {
        //更新重量
        var weight = (productCount*this.targetModel.weight).toFixed(2);
        $('.xt-weight').text(weight);

        //更新邮费
        // if ($('.xt-postage')) {
        //     var postage = this.getPostageForWeight(weight);
        //     if (postage == 0) {
        //         $('.xt-postage').text('-');
        //     } else {
        //         $('.xt-postage').text(postage.toFixed(2));
        //     }
        // }

        //更新价钱
        var totalPrice = (this.targetModel.price*productCount).toFixed(2);
        $('.xa-variablePrice').text(totalPrice);
        // if('integral' == this.productType){
        //     if (totalPrice > this.usableIntegral) {
        //         $('.xa-disabledIntegralBuyLinks').show();
        //         $('.xa-disabledBuyLinks').hide();
        //         $('.xa-enabledBuyLinks').hide();
        //     }else{
        //         $('.xa-disabledIntegralBuyLinks').hide();
        //         $('.xa-disabledBuyLinks').hide();
        //         $('.xa-enabledBuyLinks').show();
        //     }
        // }
    },

    updateProductInfo: function(model) {//更新DOM，使用在选中和释放规格值时
        if (!model) {
            $('.xa-variablePrice').text(this.priceInfo['min_price']);
            if (this.promotion && this.promotion.isFlashSalePromotion) {
                //do nothing
            } else {
                var min_price = this.priceInfo['min_price']
                if (this.discount){
                    min_price = (min_price * this.discount / 100).toFixed(2)
                }
                $('.xa-singlePrice').text(min_price);
            }
            // $('.xa-market-price').text(this.priceInfo['display_market_price']);
            $('.xa-enabledBuyLinks').hide();
            $('.xa-disabledBuyLinks').show();
            $('.xa-disabledIntegralBuyLinks').hide();
            //运费
            //$('.xa-postage').hide();
            var items = [];
            items.push('重量：<span class="xt-weight"> - </span><span class="xt-single-weight" style="display: none"> - </span></span>&nbsp;&nbsp;');
            items.push('<span class="xt-postageConfigName ml20">'+this.postageConfigName+'</span>');
            items.push(':<span class="xt-postage"> - </span>');
            $('.xa-postageContent').html(items.join(''));
            $('.xa-postage').show();

            //库存
            $('[data-ui-role="counter"]').data('view').setMaxCount(0);
            $('.xa-stock').hide();
        } else {
            if(this.targetModel){
                if (this.promotion && this.promotion.isFlashSalePromotion) {
                    //do nothing
                    if (this.promotion.type == 1) {
                        $('.xa-singlePrice').text(this.promotion.detail.promotion_price.toFixed(2));//无规格时，显示抢购的价钱
                    }
                } else {
                    $('.xa-singlePrice').text(model.price.toFixed(2));
                }
                $('.xa-variablePrice').text(model.price);

                // $('.xa-market-price').text(model.market_price);
                // if ('object' == '{{product.type}}'){
                //     alert(1)
                //     $('.xa-disabledBuyLinks').hide();
                //     $('.xa-enabledBuyLinks').show();
                // }else if (this.useIntegral < model.price) {
                //     alert(2)
                //     $('.xa-disabledIntegralBuyLinks').show();
                //     $('.xa-disabledBuyLinks').hide();
                //     $('.xa-enabledBuyLinks').hide();
                // }else{
                var counter = $('[data-ui-role="counter"]').data('view');
                // }
                //运费
                var items = [];
                if (model.weight !== 0) {
                    items.push('重量：<span class="xt-weight">'+model.weight.toFixed(2)+'</span><span class="xt-single-weight" style="display: none">' + model.weight.toFixed(2) + '</span>公斤</span>&nbsp;&nbsp;');
                }
                items.push('<span class="xt-postageConfigName ml20">'+this.postageConfigName+'</span>');
                if (model.postage >0) {
                    items.push(':￥<span class="xt-postage">'+model.postage.toFixed(2)+'</span>');
                }
                $('.xa-postageContent').html(items.join(''));
                $('.xa-postage').show();
                if((model.stock_type === 1 && model.stocks > 0)||model.stock_type === 0){
                    //库存
                    var maxCount = this.getMaxCount(this.targetModel);
                    if (model.stock_type === 1) {
                        $('.xa-stockCount').text(model.stocks);
                        $('.xa-stock').show();
                    } else {
                        $('.xa-stock').hide();
                    }
                    counter.setMaxCount(maxCount);
                }
                if(counter.maxCount>0 && counter.maxCount<counter.minCount){
                    $('.xa-disabledBuyLinks').show();
                    $('.xa-enabledBuyLinks').hide();
                }else{
                    $('.xa-disabledBuyLinks').hide();
                    $('.xa-enabledBuyLinks').show();
                }
            }
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
        // if (currentModelPropertyValue) {
        //     var items = currentModelPropertyValue.split(':');
        //     var currentPropertyId = items[0];
        //     var currentValueId = items[1];
        // } else {
        //     var currentPropertyId = -1;
        //     var currentValueId = -1;
        // }

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

        /**
         * 同一[规格名]下的[规格值]和其他[规格名]下已选[规格值]，组合出的可以选择[商品规格]
         * usefulModels = {
         *      model.id: [productModel.name]
         * }
         */
        // var usefulModels = {};
        // _.each(this.models, function(model) {
        //     if(model.stock_type == 1 && model.stocks <= 0)// 库存为零不可选择
        //         return
        //     _.each(model.name.split('_'), function(name) {
        //         var t = name.split(':')[0], flag = true; // [规格值]对应的[规格名]
        //         _.each(selectedPropertyValues, function(value_name){
        //             if(value_name.split(':')[0] == t)
        //                 return
        //             if(model.name.indexOf(value_name) < 0)// 在其他[规格名]下已选[规格值],不在[商品规格]中 不可选择
        //                 flag = false;
        //         })
        //         if(!flag)
        //             return
        //         if(!usefulModels.hasOwnProperty(t))
        //             usefulModels[t] = []
        //         usefulModels[t].push(model.name)
        //     })
        // })
        // xlog(usefulModels)
        // $('.xa-propertyValue').each(function() {
        //     if($(this).hasClass('xui-inner-selected-tag'))
        //         return
        //     var name = $(this).attr('name');
        //     var curUsefulModels = usefulModels[name.split(':')[0]];
        //     var flag = false;
        //     _.each(curUsefulModels, function(models){
        //         if(models.indexOf(name) >= 0){
        //             flag = true
        //         }
        //     })
        //     if (flag) {
        //         $(this).removeClass('xui-unSelectable');
        //     } else {
        //         $(this).removeClass('xui-inner-selected-tag').addClass('xui-unSelectable');
        //     }
        // })


        // if (selectedPropertyValues.length === 1 && currentPropertyId === -1) {
        //     //当前只有一个规格属性，不用禁用任何规格属性值
        //     return;
        // }

        // //判断一个model是否是selectedPropertyValues的候选model
        // //当model的所有property value包含全部selected property value时，它是一个候选model
        // function checkCandidate(model) {
        //     if (model.stock_type === 1 && model.stocks === 0) {
        //         //如果model无库存，直接返回
        //         return {
        //             isCandidate: false,
        //             selectablePropertyValues: {}
        //         }
        //     }

        //     var modelName = model.name;
        //     var modelPropertyValues = modelName.split('_');
        //     // var modelPropertyValueSet = _.object(modelPropertyValues, []);
        //     // for (var i = 0; i < selectedPropertyValues.length; ++i) {
        //     //     var selectedPropertyValue = selectedPropertyValues[i];
        //     //     if (!modelPropertyValueSet.hasOwnProperty(selectedPropertyValue)) {
        //     //         return {
        //     //             isCandidate: false,
        //     //             selectablePropertyValues: {}
        //     //         };
        //     //     }
        //     // }

        //     //收集candidate model中没有被选中的property value，这些property value就是还可以被操作的property value
        //     //其他的property value都将被disable
        //     var selectablePropertyValues = {};
        //     for (var i = 0; i < modelPropertyValues.length; ++i) {
        //         var modelPropertyValue = modelPropertyValues[i];
        //         if (!selectedPropertyValueSet.hasOwnProperty(modelPropertyValue)) {
        //             selectablePropertyValues[modelPropertyValue] = 1;
        //         }
        //     }
        //     return {
        //         isCandidate: true,
        //         selectablePropertyValues: selectablePropertyValues
        //     };
        // }

        // //遍历model
        // var selectablePropertyValues = {};
        // _.each(this.models, function(model) {
        //     var checkResult = checkCandidate(model);
        //     if (checkResult.isCandidate) {
        //         _.extend(selectablePropertyValues, checkResult.selectablePropertyValues);
        //     }
        // });

        // //检查所有的property value，禁用un-selectable的property value
        // //如果：
        // //1. property value在selectablePropertyValues
        // //2. property value的property为currentPropertyId
        // //两个条件都不满足，则该property value是un-seletable的
        // $('.xa-propertyValue').each(function() {
        //     var $propertyValue = $(this);
        //     var propertyValue = $propertyValue.attr('name');
        //     var items = propertyValue.split(':');
        //     var propertyId = items[0];
        //     if ((propertyId !== currentPropertyId)
        //         && !(selectablePropertyValues.hasOwnProperty(propertyValue))
        //         && !(selectedPropertyValueSet.hasOwnProperty(propertyValue))) {
        //         $propertyValue.removeClass('xui-inner-selected-tag').addClass('xui-unSelectable');
        //     } else {
        //         $propertyValue.removeClass('xui-unSelectable');
        //     }
        // })
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
            xlog('can not select');
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
            // $propertyValue.find('.xui-selectedIcon').removeClass('hidden');
            isSelectPropertyValue = false;
            // if ($selectModelHint.text() === '选中') {
            //     $('.xa-selectedModelPropertyValueName').hide();
            //     $selectModelHint.text('请选择');
            // }
            $modelValueText.text($modelValueText.attr('data-property-name')).removeClass('xui-text-red').show();
        } else {
            $propertyValue.parents('.xui-i-customModel').find('.xui-inner-selected-tag').removeClass('xui-inner-selected-tag');
            $propertyValue.toggleClass('xui-inner-selected-tag');
            // $propertyValue.find('.xa-selectedIcon').toggleClass('xui-selectedIcon');
            // $propertyValue.siblings().find('.xui-selectedIcon').addClass('hidden');
            // console.log($propertyValue,890)
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
            // $selectModelHint.text('选中');
            $('.xa-selectedModelPropertyValueName').show();
            counter.reset();
        } else {
            $('input[data-ui-role="counter"]').data('view').disable();
            $('.xa-purchaseCount').text("数量");
            this.updateProductInfo();
            // 显示所有库存数量
            if (this.totalStocks > 0) {
                $('.xa-stockCount').text(this.totalStocks);
                $('.xa-stock').show();

            }
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
        if(counter.maxCount>0 && counter.maxCount<counter.minCount){
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
        var is_collect = $('.xa-collectProduct').attr('data-is-collect');
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
                if(is_collect == 'true'){
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
