/**
 * wepage异步组件加载
 * author：liupeiyu, liugenbin
 */
(function() {
/**
 * AsyncComponentLoadView: 异步组件加载View
 * 目前只针对“商品模块”进行处理
 */
W.AsyncComponentLoadView = BackboneLite.View.extend({
    events: {
    },

    // 改写了原系统的handlebar模版，原模版导致渲染速度慢
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

    initialize: function(options) {
        this.$el = $(this.el);

        var componentType = this.$el.attr('data-type');
        if (componentType !== 'wepage.item_group') return ;

        // 获取由服务端写入标签的component属性json值
        var componentModel = $.parseJSON(this.$el.attr('data-model') || '{}');

        // 给每个组件一个属性索引, 解决排序问题
        var componentIndex = componentModel['index'];
        if (componentIndex > -1) {
            this.$el.attr('component-index', componentIndex);
        }

        componentModel.is_itemname_hidden = '';
        componentModel.is_price_hidden = '';

        // 判断价格和商品名称是否显示
        // 来自原系统服务端生成的handlebar模版
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

        this.data = {
            components: componentModel.components,
            model: componentModel,
            type: componentType
        };
    },

    sortByIds: function(products, ids) {
        var objIds = {};
        ids.map(function(id, idx){
            objIds[id] = idx;
        });
        products.map(function(product){
            product['index'] = objIds[product['id']];
        });
        return _.sortBy(products, 'index');
    },

    __sendApi: function(deferred, componentData) {
        if (typeof(componentData) === 'undefined') return;
        
        var _this = this;
        var product_ids = componentData['model']['items'];
        var componentIndex = componentData['model']['index'];
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
                product_ids: product_ids
            },
            success: function(data) {
                data.products = _this.sortByIds(data.products, product_ids);
                data['componentIndex'] = componentIndex;
                deferred.resolve(data);
            },
            error: function(data) {
                console.log('取商品模块异步数据异常：', data);
            }
        });
    },

    // 渲染组件节点
    render: function () {
        // 开始异步，获取组件“商品模块”中的商品信息
        var _this = this;
        var deferred = $.Deferred();
        _this.__sendApi(deferred, _this.data);

        // 完成异步接口后
        $.when(deferred).done(function(data){
            //补充component数据
            var componentIndex = data['componentIndex'];
            // 根据商品数量填补component对象
            _this.data['valid_product_count'] = data['products'].length;
            //_this.component['component']['components'] = [];

            // 将产品子数据，放到component.components中
            // 并把是否显示价格和名字的开关也放进去
            data.products.map(function(product, idx){
                // 若是又拍云图片，则压缩成list所用的大小
                var upaiyunKey = /upaiyun\.com/;
                if (upaiyunKey.test(product['thumbnails_url'])) {
                    product['thumbnails_url'] = product['thumbnails_url'] + '!list';
                }


                product['is_itemname_hidden'] = _this.data['model']['is_itemname_hidden'];
                product['is_price_hidden'] = _this.data['model']['is_price_hidden'];
                product['is_border_show'] = _this.data['model']['is_border_show'];
                product['link_url'] = W.H5_HOST+"/mall/product/?woid="+W.webappOwnerId+"&product_id="+product['id']+"&referrer=weapp_product_list";

                _.extend(_this.data['components'][idx], product);
            });

            // 渲染组件
            var compiledTemplate = _this.getTemplate(_this.data['type']);
            if (compiledTemplate) {
                var html = compiledTemplate(_this.data);
                _this.$el.html(html);

                // 异步渲染完成后，重新刷新右侧属性框
                _.delay(function(){
                    W.Broadcaster.trigger('mobilewidget:select', _this.data.model.cid);
                }, 100);
            }

            var isInFrame = (parent !== window);
            if (isInFrame) {
                // 预览模式下禁止点击
                if (parent.setWebappPageTitle) {
                    parent.setWebappPageTitle(W.pageTitle);
                }

                //在预览模式下，修改a，禁止点击
                $('a').each(function() {
                    var $link = $(this);
                    $link.attr('href', 'javascript:void(0);');
                })

                // 装修／预览模式下，不延迟加载图片
                $('a img', _this.el).each(function() {
                    var $itemImg = $(this);
                    var srcImg = $itemImg.attr('data-url');
                    $itemImg.attr('src', srcImg);
                })
                
            } else {
                // 手机模式下
                // 重新定义图片延迟加载, lazyloadImg已由页面定义
                W.lazyloadImg($('a img', _this.$el), {
                    threshold: 0,
                    effect : "fadeIn",
                    placeholder: "/static_v2/img/webapp/mall/info_placeholder.png"
                });
            }


        });
    }


});
//END of W.AsyncComponentLoadView

W.initAsyncComponent = function() {
    // 初始化view, 目前只针对商品模块
    var allComponents = [];
    $('div[data-ui-role="async-component"]').each(function() {
        var $node = $(this);
        $node.append('<div style="text-align:center;"><img src="/static_v2/img/product_list_loading.gif"></div>');
        allComponents.push($node);
    });

    allComponents.map(function($component){
        var asyncComponentView = new W.AsyncComponentLoadView({el: $component[0]});
        asyncComponentView.render();
    });
}
$(function(){
    W.initAsyncComponent();
});

})(W);

