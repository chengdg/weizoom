/**
 * wepage异步组件加载
 * author：liupeiyu, liugenbin
 */
(function() {
/**
 * AsyncComponentView: 异步组件加载View
 * 目前只针对“商品模块”进行处理
 */
W.AllComponentsView = BackboneLite.View.extend({
    events: {},

    initialize: function(options) {
        var _this = this;
        this.allComponents = options.el;
        this.allComponentsData = [];
        this.objProducts = {};

        options.el.map(function(ele){
            var $cmp = $(ele[0]);
            var componentType = $cmp.attr('data-type');
            if (componentType !== 'wepage.item_group') return ;

            // 获取由服务端写入标签的component属性json值
            var componentModel = $.parseJSON($cmp.attr('data-model') || '{}');

            componentModel.is_itemname_hidden = '';
            componentModel.is_price_hidden = '';

            // 判断价格和商品名称是否显示
            // 逻辑来自原系统服务端生成的handlebar模版
            if (componentModel.type != '3' && 
                componentModel.itemname == false ) {
                    componentModel.is_itemname_hidden = ' style=display:none ';
            }
            if (componentModel.type != '3' && 
                componentModel.card_type != '1' &&
                componentModel.itemname == true ) {
                    componentModel.is_border_show = ' xui-border ';
            }
            if (componentModel.type != '3' &&
                componentModel.price == false ) {
                    componentModel.is_price_hidden = ' style=display:none ';
            }

            var datum = {
                components: componentModel.components,
                model: componentModel,
                type: componentType
            };
            _this.allComponentsData.push(datum);
        });

        var deferred = $.Deferred();
        this.__asyncFetchAllData(deferred, this.allComponentsData);

        $.when(deferred).done(function(allProductData){
            // 获取完所有商品模块中的所有数据后，开始渲染模块
            // 生成商品对象库
            _this.objProducts =  _this.productsAryToObj(allProductData);
            // 开始渲染
            _this.render();
        });
    },

    // 生成所有商品的对象
    productsAryToObj: function(allProductData) {
        if (!allProductData || !allProductData.products) {return {}}

        var objComponents = {};
        allProductData.products.map(function(product){
            objComponents[product.id] = product;
        });
        return  objComponents;
    },

    // 渲染所有组件
    render: function(){
        var allComponentsData = this.allComponentsData;
        var allComponents = this.allComponents;
        var objProducts = this.objProducts;

        console.log('新view渲染初始值：', allComponentsData);

        allComponents.map(function(component){
            var param = {
                el: component,
                model: objProducts
            };
            var asyncComponentView = new W.AsyncComponentView(param);
            asyncComponentView.render();
        });
    },

    // 异步获取所有商品信息
    __asyncFetchAllData: function(deferred, allComponentsData) {
        if (typeof(allComponentsData) === 'undefined') return;
        var _this = this;
        var allProductIds = [];

        allComponentsData.map(function(datum){
            allProductIds = _.union(allProductIds, datum['model']['items']);
        });
        var productIds = allProductIds.join(',');

        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            cache: false,
            async: true,
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'page_products/get',
                product_ids: productIds
            },
            success: function(data) {
                // 放入回调队列，解决在ios系统下卡顿问题
                console.log('异步获取商品模块所有id：%o, %o, %o', allProductIds, productIds, data);
                data.products = _this.__duplicatedProduct(data.products, productIds);
                deferred.resolve(data);
            },
            error: function(data) {
                console.log('取商品模块异步数据异常：', data);
            }
        });
    },

    // 重新整理返回的商品对象，防止请求的ids和返回的商品不一致的问题
    // 检查异步前的所有id，去除没有取得的商品，生成没有缺陷的对象数组
    __duplicatedProduct: function (products, productIds) {
        var objProducts = {};
        if (products) {
            products.map(function(product){
                objProducts[product.id] = product;
            });
        }

        var newProducts = [];
        if (productIds) {
            productIds.split(',').map(function(productId){
                if (objProducts[productId]) {
                    newProducts.push(objProducts[productId]);
                }
            });
        }

        return newProducts;
    },
                
});

/**
 * 模块View, 目前只处理商品模块
 */
W.AsyncComponentView = BackboneLite.View.extend({
    events: {
    },

    // 改写了原系统的handlebar模版，原模版渲染速度慢
    getTemplate: function(componentType) {
        // 只返回商品模块的已编译模版
        if (componentType !== 'wepage.item_group') return;
        var itemGroupTemplate = '\
            <div class="xa-products-box wui-product wui-productTitle" \
                data-component-cid="{{model.cid}}" \
                data-index="{{model.index}}" \
            > \
                <ul class="wui-block-type{{model.type}} wui-card-type-{{model.card_type}}"> \
                    {{#each components}} \
                        <li data-component-cid="{{this.cid}}" \
                            data-index="{{this.index}}"   \
                        > \
                            <a class="wui-inner-box{{index}}{{#if product.is_member_product}} xa-member-product{{/if}} wa-item-product" \
                                href="{{this.link_url}}" \
                                data-handlebar-data=\'{ "index":"{{index}}", "product":{"thumbnails_url":"{{this.thumbnails_url}}", "name":"{{this.name}}", "display_price":"{{this.display_price}}"} }\' \
                                data-product-promotion="{{this.promotion_js}}" \
                                data-product-price="{{this.display_price}}"> \
                                <div class="wui-inner-pic"> \
                                    <img data-url="{{this.thumbnails_url}}" /> \
                                </div> \
                                <div class="wui-inner-titleAndprice"> \
                                    <p class="wa-inner-title xui-inner-title" {{this.is_itemname_hidden}}> \
                                        {{this.name}}</p> \
                                    <p class="wa-inner-price xui-inner-price {{this.is_border_show}}" {{this.is_price_hidden}}> \
                                        <span>¥</span>{{this.display_price}} \
                                    </p> \
                                </div> \
                            </a> \
                        </li> \
                    {{/each}} \
                </ul> \
            </div>\
        ';
        return Handlebars.compile(itemGroupTemplate);
    },

    // 初始化当前组件的两个主要变量
    // this.datum: 包含本页面所有商品模块信息，当前模块信息，当前模块类型
    // this.products: 包含当前商品模块的所有商品数据
    initialize: function(options) {
        var _this = this;
        var ele = options.el;

        var $cmp = $(ele[0]);
        var componentType = $cmp.attr('data-type');
        if (componentType !== 'wepage.item_group') return ;

        // 获取由服务端写入标签的component属性json值
        var componentModel = $.parseJSON($cmp.attr('data-model') || '{}');

        componentModel.is_itemname_hidden = '';
        componentModel.is_price_hidden = '';

        // 判断价格和商品名称是否显示
        // 逻辑来自原系统服务端生成的handlebar模版
        // 不放在模版中处理
        if (componentModel.type != '3' && 
            componentModel.itemname == false ) {
                componentModel.is_itemname_hidden = ' style=display:none ';
        }
        if (componentModel.type != '3' && 
            componentModel.card_type != '1' &&
            componentModel.itemname == true ) {
                componentModel.is_border_show = ' xui-border ';
        }
        if (componentModel.type != '3' &&
            componentModel.price == false ) {
                componentModel.is_price_hidden = ' style=display:none ';
        }

        // 当前商品组件的组件信息
        this.datum = {
            components: componentModel.components,
            model: componentModel,
            type: componentType
        };

        // 当前商品组件的商品信息，提取于异步接口中获得的所有商品信息
        this.products = [];
        this.datum.model.items.map(function(productId){
            _this.products.push(options.model[productId]);
        });
    },

    // 渲染组件节点
    render: function () {
        var _this = this;
        var products = this.products; 

        // 将产品子数据，放到component.components中
        // 并把是否显示价格和名字的开关也放进去
        products.map(function(product, idx){
            // 若是又拍云图片，则压缩成list所用的大小, 
            var upaiyunKey = /upaiyun\.com/;
            var imgSrc = product['thumbnails_url'];
            if (upaiyunKey.test(imgSrc)) {
                // 清理upaiyun链接里的特殊符号
                if (imgSrc.indexOf('!') > 0) {
                    imgSrc = imgSrc.substring(0, imgSrc.indexOf('!'))
                }
                // 增加‘!list’参数
                product['thumbnails_url'] = imgSrc + '!list';
            }

            product['is_itemname_hidden'] = _this.datum['model']['is_itemname_hidden'];
            product['is_price_hidden'] = _this.datum['model']['is_price_hidden'];
            product['is_border_show'] = _this.datum['model']['is_border_show'];
            product['link_url'] = W.H5_HOST+"/mall/product/?woid="+W.webappOwnerId+"&product_id="+product['id']+"&referrer=weapp_product_list";

            _.extend(_this.datum['components'][idx], product);
        });

        // 渲染组件
        var compiledTemplate = _this.getTemplate(_this.datum['type']);
        if (compiledTemplate) {
            var html = compiledTemplate(_this.datum);
            _this.$el.html(html);

            // 异步渲染完成后，重新刷新右侧属性框
            _.delay(function(){
                if (W.Broadcaster) {
                    W.Broadcaster.trigger('mobilewidget:select', _this.datum.model.cid, {autoScroll:true, forceUpdatePropertyView:true});
                }
            }, 100);
        }

        // 预览模式下，不能点击超链接
        var isInFrame = (parent !== window);
        if (isInFrame) {
            // 装修／预览模式下
            if (parent.setWebappPageTitle) {
                parent.setWebappPageTitle(W.pageTitle);
            }

            //修改a，禁止点击
            $('a', _this.el).each(function() {
                var $link = $(this);
                $link.attr('href', 'javascript:void(0);');
            })

            // 不延迟加载图片
            $('a img', _this.el).each(function() {
                var $itemImg = $(this);
                var srcImg = $itemImg.attr('data-url');
                $itemImg.attr('src', srcImg);
            })
            
        } else {
            // 手机模式下
            // 重新定义图片延迟加载, W.lazyloadImg已由页面定义
            W.lazyloadImg($('a img', _this.$el), {
                threshold: 0,
                effect : "fadeIn",
                placeholder: "/static_v2/img/webapp/mall/info_placeholder.png"
            });
        }


        // });
    }


});
//END of W.AsyncComponentView

W.initAsyncComponent = function(cid) {
    // 初始化view, 目前只针对商品模块
    var allComponents = [];
    if (cid) {
        $('div.xa-componentContainer[data-contained-cid="'+cid+'"]').find('div[data-ui-role="async-component"]').each(function() {
            var $node = $(this);
            $node.append('<div style="text-align:center;"><img src="/static_v2/img/product_list_loading.gif"></div>');
            allComponents.push($node);
        });
    } else {
        $('div[data-ui-role="async-component"]').each(function() {
            var $node = $(this);
            $node.append('<div style="text-align:center;"><img src="/static_v2/img/product_list_loading.gif"></div>');
            allComponents.push($node);
        });
    }

    // 获得所有商品id
    // 异步获取所有商品信息, 并渲染相关组件
    var allComponentsView = new W.AllComponentsView({el: allComponents});

}
$(function(){
    W.initAsyncComponent();
});

})(W);

