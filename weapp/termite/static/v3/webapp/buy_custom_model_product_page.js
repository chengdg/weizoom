/**
 * Backbone View in Mobile
 */
W.page.BuyProductPage = BackboneLite.View.extend({
    events: {
        'click .xa-slidePanelShow': 'selectionSlide',
        'click .xa-coverV2,.xa-closeModelSelection': 'onCloseModelSelection',
        'click .xa-propertyValue': 'onSelectModelPropertyValue',
        'click .xa-canNotBuyButton': 'onClickCanNotBuyButton',
        'click .xa-addShoppingCartBtn': 'onClickAddShoppingCartButton',
        'click .xa-collectProduct': 'onClickCollectProductButton',
        'click .xa-property':'onClickPropertyPanel'
    },

    initialize: function(options) {
        this.productId = options.productId;
        this.models = options.models;
        this.minPrice = options.priceInfo.min_price;
        this.is_member_product = options.is_member_product == 'True';
        this.promotion = options.promotion || null;
        // 限购数量
        if (this.promotion && this.promotion.type == 1){
            this.countPerPurchase = this.promotion.detail.count_per_purchase;
            this.isFlashSale = true;
        }else{
            this.countPerPurchase = -1;
        }
        //买赠
        if (this.promotion && this.promotion.type == 2){
            this.isPremium = true;
        }else{
            this.isPremium = false;
        }
        this.targetModel = null;
        this.isStandardModelProduct = false;
        this.isSideSlideOpen = false;
        this.maxCount = -1;
        this.productCount = 1;
        //判断商品是否是标准规格商品
        if (this.models.length === 1 && this.models[0]['name'] === 'standard') {
            this.isStandardModelProduct = true;
        }else{
            new iScroll('xa-wrapper',{hScrollbar:false,bounce:false});
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
        this.counter = $('input[data-ui-role="counter"]').data('view');
        if(this.counter.minCount>1)this.updateCountInByLink(this.counter.minCount)
        // 处理懒加载图片
        $('[data-url]').lazyload({
            data_attribute:"url",
            effect : "fadeIn",
            placeholder: options.cdn_host+"/static_v2/img/webapp/mall/info_placeholder.png"
        });
        // 处理评价会员昵称
        $(".xa-memberName").each(function(i,n){
            var str = $(n).text().trim();
            var str_name = str.substring(0,1)+"**"+str[str.length-1];
            $(n).html(str_name);
        });
    },
    /**
     * initProductModel: 初始化标准规格商品界面
     */
    initProductModel: function(maxCount) {
        this.counter.setMaxCount(maxCount);
        if(maxCount < 1){
            this.counter.disable();
        }else if(maxCount = -99999 || this.counter.minCount <= maxCount){
            $('.xa-disabledBuyLinks').hide();
            $('.xa-enabledBuyLinks').show();
        }
        // 用于处理更新促销信息
        this.updatePromotionInfo();
    },
    /**
     * 更新积分广告语
     */
    updatePromotionInfo: function(){
        var price, oPrice = 0;
        if(this.targetModel){
            oPrice = this.targetModel.price;
        }else{
            oPrice = this.minPrice;
        }
        if(this.isFlashSale){
            price = this.promotion.detail.promotion_price;
        }else if(this.discount){// 会员价
            price = oPrice * this.discount / 100;
        }else{
            price = oPrice;
        }
        if(this.isFlashSale){// 有限时抢购
            $('.xa-promotionNormal-info').text('已优惠' + (oPrice - price).toFixed(2) + '元');
        }
        if($('.xa-promotion').data('type')==5){// 有积分优惠
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
        }
    },
    /**
     * getMaxCount 获取指定规格最大购买数量
     */
    getMaxCount: function(model){
        var maxCount = 0;
        var message = '';

        if (model.stock_type === 1) {// 有限库存
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
                maxCount = 99999;
            }
        }

        this.maxCount = maxCount;
        // 修改提示信息
        $('.xa-understock').text(message);
        return maxCount;
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
                    n.stocks = data[n.id].stocks;
                    if(n.stock_type == 0){
                        stock_all = 999999;//无限库存
                    }else{
                        stock_all += n.stocks
                    }
                    if(_this.targetModel && _this.targetModel.id == n.id){
                        //更新库存
                        _this.updateProductStock(n);
                    }
                });
                if(stock_all==0){
                    $('.xa-selloutAlert').show();
                    $('.xa-not_selloutAlert').hide();
                }else{
                    $('.xa-not_selloutAlert').show();
                    $('.xa-selloutAlert').hide();
                }
                _this.disableUnselectableModelPropertyValue();

                if(isInit){
                    if(data.is_collect == 'true'){
                        $('.xa-collectProduct').addClass('faved').text('已收藏');
                        $('.xa-collectProduct').attr('data-is-collect', 'true');
                    }
                    if(data.count != 0) {
                        $('.xa-shoppingCartCount').text(data.count).removeClass("hidden");
                    }
                    _this.usableIntegral = data.usable_integral
                    _this.memberGradeId = data.member_grade_id
                    
                    if(_this.promotion){// 商品有促销
                        if(_this.promotion.member_grade_id != 0 && _this.promotion.member_grade_id != _this.memberGradeId){
                            // 促销不对此用户等级开放
                            $('.xt-masterPromotionTile').remove()
                            var next_promotions = $('.xa-display-promotion').next('div');
                            if(next_promotions.length==0){
                                // 没有积分应用
                                $('.xa-promotionSection').remove();
                            }else if(next_promotions.length == 1){
                                // 有积分应用
                                $('.xa-display-promotion').html(next_promotions.html()).find('div:first').html('优惠：');
                                next_promotions.remove();
                            }
                            if(_this.isFlashSale){
                                _this.isFlashSale = false;
                            }
                            if(_this.isPremium){
                                _this.isPremium = false;
                            }
                        }
                    }
                    $('.xa-promotionSection').show();
                    $('.xt-promotionTile:first').show();
                    if(!_this.isFlashSale && _this.is_member_product && data.discount < 100 && !_this.isPremium){
                        // 会员价处理
                        _this.discount = data.discount;
                        $('.xa-singlePrice').html((_this.minPrice * data.discount / 100).toFixed(2)).parent().before('<span class="xui-memberPriceTag">会员价</span>');
                        $('.xa-singlePrice').after('<span class="xui-orPrice">原价￥<span class="xa-orPrice">'+_this.minPrice.toFixed(2)+'</span>');
                    }
                    if (_this.isStandardModelProduct) {
                        _this.targetModel = _this.models[0];
                        var maxCount=_this.getMaxCount(_this.targetModel);
                        _this.initProductModel(maxCount);
                    } else {
                        _this.initProductModel(0);
                    }
                    _this.updateProductInfo(_this.targetModel);

                    var token = $.cookie('current_token');
                    if(token){
                        $('[data-ui-role="integralMechanism"]').data('view').setFmt(token.split('____')[1]);
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
     * onCloseModelSelection: 点击关闭规格选择触发器的响应函数
     */
    onCloseModelSelection: function(event) {
        if (this.isSideSlideOpen) {
            this.selectionSlide();
        };
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
     * onChangeProductCount: counter widget的count-change event的响应函数
     */
    onChangeProductCount: function(event, value) {
        $('.xa-purchaseCount').text(value);

        this.updateCountInByLink(value);
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
    /*
     * 更新DOM，使用在选中和释放规格值时
     */
    updateProductInfo: function(model) {
        var singlePrice = 0;
        if (this.isFlashSale) {
            singlePrice = this.promotion.detail.promotion_price;
        }
        if (!model) {
            if(singlePrice == 0){
                singlePrice = this.minPrice;
            }
            $('.xa-enabledBuyLinks').hide();
            $('.xa-disabledBuyLinks').show();
            $('.xa-disabledIntegralBuyLinks').hide();
            //库存
            this.counter.setMaxCount(0);
        } else {
            if(singlePrice == 0) {
                singlePrice = model.price;
            }
            this.updateProductStock(model);
        }
        if (this.discount){
            $('.xa-orPrice').text(singlePrice.toFixed(2));
            singlePrice = singlePrice * this.discount / 100;
        }
        $('.xa-singlePrice').text(singlePrice.toFixed(2));
    },
    /**
     * 只对targetModel执行
     * @param model
     */
    updateProductStock: function(model){
        //库存
        var maxCount = this.getMaxCount(model);
        this.counter.setMaxCount(maxCount);

        if(this.counter.maxCount >= 0 && (this.counter.maxCount < this.counter.count || this.counter.maxCount < this.counter.minCount)){
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
        // if (model === null) {
        //     return;
        // }
        var $buy = $('.xa-buyBtn');
        $('.xa-buyBtn').each(function(){
            $buy = $(this);
            var hrefAttr = $buy.attr('data-href');
            hrefAttr = hrefAttr.replace(/product_model_name=.*$/, 'product_model_name='+model.name);
            $buy.attr('data-href', hrefAttr);
        });
    },

    /**
     * updateCountInByLink: 修改“购买”链接中的product_count参数
     */
    updateCountInByLink: function(productCount) {
        var $buy = $('.xa-buyBtn');
        $('.xa-buyBtn').each(function(){
            $buy = $(this);
            var hrefAttr = $buy.attr('data-href');
            hrefAttr = hrefAttr.replace(/product_count=\d+/, 'product_count='+productCount);
            $buy.attr('data-href', hrefAttr);
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

        //增加取消选择
        var isSelectPropertyValue = true;
        if ($propertyValue.hasClass('xui-inner-selected-tag')) {
            $propertyValue.removeClass('xui-inner-selected-tag');
            isSelectPropertyValue = false;
            $modelValueText.text($modelValueText.data('propertyName')).removeClass('xui-text-red').show();
        } else {
            $propertyValue.parents('.xui-i-customModel').find('.xui-inner-selected-tag').removeClass('xui-inner-selected-tag');
            $propertyValue.toggleClass('xui-inner-selected-tag');
            $modelValueText.text(currentModelPropertyValueName);
        }

        //根据选择结果更新页面
        var currentModelPropertyValue = $propertyValue.attr('name');

        this.targetModel = this.getSelectedModel();
        this.updatePromotionInfo();
        if (this.targetModel) {
            //启用counter
            this.counter.enable();
            //如果选中了合法的商品规格组合，更新商品信息
            this.disableUnselectableModelPropertyValue();
            this.updateProductInfo(this.targetModel);
            this.updateModelInBuyLink(this.targetModel);
            //显示选中的规格值
            this.counter.reset();
        } else {
            this.counter.disable();
            $('.xa-purchaseCount').text("数量");
            this.updateProductInfo();
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
        var msg = '';
        if(this.targetModel){
            // TODO
            if(this.counter.maxCount>0 && this.counter.maxCount<this.counter.count ||this.counter.maxCount ==this.counter.count&&this.counter.count==0&&this.counter.maxCount<this.counter.minCount){
                msg = '库存不足';
            }
        }else if(this.isSideSlideOpen){
            msg = '请先选择商品规格'
        }else{
            this.selectionSlide();
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
