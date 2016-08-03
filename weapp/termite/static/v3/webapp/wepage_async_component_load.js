/**
 * wepage异步组件加载
 * author：liupeiyu
 */
(function() {
/**
 * AsyncComponentLoadView: 异步组件加载View
 */
var AsyncComponentLoadView = BackboneLite.View.extend({
    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.componentType = options.componentType;
        this.componentModel = options.componentModel;
        this.componentModel.is_itemname_hidden = '';
        this.componentModel.is_price_hidden = '';
        // 判断价格和商品名称是否显示
        if (this.componentModel.type != '3' && 
            this.componentModel.card_type != '1' &&
            this.componentModel.itemname == false ) {
                this.componentModel.is_itemname_hidden = ' style=display:none ';
        }
        if (this.componentModel.type != '3' &&
            this.componentModel.price == false ) {
                this.componentModel.is_price_hidden = ' style=display:none ';
        }
        this.component = {
            component: {
                model: options.componentModel,
                type: options.componentType
            }
        };
        //this.handlebarTmpl = $("#componentTemplates").html();
        /*
        var productListTemplate = '\
            <div class="xa-products-box wui-product wui-productTitle"> \
                <ul class="wui-block-type{{component.model.type}} wui-card-type-{{component.model.card_type}}"> \
                    {{#each component.components}} \
                        <li data-component-cid="{{component.cid}}" \
                          data-index="{{component.model.index}}"> \
                              <a class="wui-inner-box{{index}}{{#if product.is_member_product}} xa-member-product{{/if}} wa-item-product" \
                                  href="{{this.link_url}}" \
                                  data-handlebar-data=\'{ "index":"{{index}}", "product":{"thumbnails_url":"{{this.thumbnails_url}}", "name":"{{this.name}}", "display_price":"{{this.display_price}}"} }\' data-product-promotion="{{this.promotion_js}}" data-product-price="{{this.display_price}}"> \
                                <div class="wui-inner-pic"> <img data-url="{{this.thumbnails_url}}" /></div> \
                                 <div class="wui-inner-titleAndprice"> \
                                    <p class="wa-inner-title xui-inner-title" {{this.is_itemname_hidden}}> \
                                        {{this.name}}</p> \
                                    <p class="wa-inner-price xui-inner-price" {{this.is_price_hidden}}> \
                                        <span>¥</span>{{this.display_price}}</p> \
                              </div> \
                            </a> \
                        </li> \
                    {{/each}} \
                </ul> \
            </div>\
        ';
        //this.template = Handlebars.compile(this.handlebarTmpl);
        this.template = Handlebars.compile(productListTemplate);
         * */
        var deferred = $.Deferred();
        this.sendApi(deferred);
        var _this = this;
        $.when(deferred).done(function(data){
            // 根据商品数量填补component对象
            _this.component['component']['valid_product_count'] = data['products'].length;
            _this.component['component']['components'] = [];
            // 将产品子数据，放到component.components中
            // 并把是否显示价格和名字的开关也放进去
            data.products.map(function(product){
                product['is_itemname_hidden'] = _this.component['component'].model['is_itemname_hidden'];
                product['is_price_hidden'] = _this.component['component'].model['is_price_hidden'];
                product['link_url'] = W.H5_HOST+"/mall/product/?woid="+W.webappOwnerId+"&product_id="+product['id']+"&referrer=weapp_product_list";
                _this.component['component']['components'].push(product);
            });
            console.log('>>>>>>>>>>>>>>>>>> product: ', data, W);
            var orgHtml = _this.renderComponent(_this.component, data);
            //var orgHtml = _this.template(_this.component);
            _this.$el.html(orgHtml);
            $lazyImgs = $('[data-ui-role="async-component"] a img');
            lazyloadImg($lazyImgs, {
                threshold: 0,
                effect : "fadeIn",
                placeholder: "/static_v2/img/webapp/mall/info_placeholder.png"
            });
            // 停止渲染子组件
            //var $eleUl = _this.$el.find('ul');
            //_this.renderSub($eleUl, data);
        });
    },

    sendApi: function(deferred) {
        var _this = this;
        var product_ids = this.componentModel['items'];
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            cache: true,
            async: true,
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'page_products/get',
                product_ids: product_ids
            },
            success: function(data) {
                deferred.resolve(data);
            },
            error: function(data) {
            }
        });
    },

    // 渲染主标签
    renderComponent: function (component, subData) {
        var html = templateProductList(component);
        return html;
    },

    // 渲染子标签
    /*
    renderSub: function($el, data) {
        var _this = this;
        var product_ids = this.componentModel['items'];
        var products = data['products'];
        var sub_component_htmls = [];
        product_ids.forEach(function(product_id) {
            var product = _.find(products, function(item){return item.id === product_id});
            // TODO: 将该html加入到sub_component中的html属性中
            var sub_component_html = _this.addSubComponetRender(product);
            sub_component_htmls.push(sub_component_html);
        });

        // TODO: 使用handlebar-template 渲染 
        $el.html(sub_component_htmls.join(''));

    },

    addSubComponetRender: function(product) {
        // TODO: 使用handlebar-template 渲染 
        var _this = this;
        var itemComponent = {
            component: {
                type: 'wepage.item',
                runtime_data: {product: product},
                parent_component: _this.component.component
            },
            product: product
        };
        var html = this.renderComponent(itemComponent, {});
        html = html.replace('src=', 'data-url=');
        return html;
    }
     * */
});

var allComponents = [];
var templateProductList = null;
$(function(){
    $('div[data-ui-role="async-component"]').each(function() {
        var $div = $(this);
        $div.append('<div style="text-align:center;"><img src="/static_v2/img/product_list_loading.gif"></div>');
        allComponents.push($div);
    });

    // 关闭所有图片
    /*
    $('img[data-url], img[src]').each(function() {
        var $div = $(this);
        $div.attr('data-url', '');
        $div.attr('src', '');
    });
     * */

    var componentsTmpl = $("#productListTemplate").html();

    // 优先编译好模版
    var productListTemplate = '\
        <div class="xa-products-box wui-product wui-productTitle"> \
            <ul class="wui-block-type{{component.model.type}} wui-card-type-{{component.model.card_type}}"> \
                {{#each component.components}} \
                    <li data-component-cid="{{component.cid}}" \
                      data-index="{{component.model.index}}"> \
                          <a class="wui-inner-box{{index}}{{#if product.is_member_product}} xa-member-product{{/if}} wa-item-product" \
                              href="{{this.link_url}}" \
                              data-handlebar-data=\'{ "index":"{{index}}", "product":{"thumbnails_url":"{{this.thumbnails_url}}", "name":"{{this.name}}", "display_price":"{{this.display_price}}"} }\' data-product-promotion="{{this.promotion_js}}" data-product-price="{{this.display_price}}"> \
                            <div class="wui-inner-pic"> <img data-url="{{this.thumbnails_url}}" /></div> \
                             <div class="wui-inner-titleAndprice"> \
                                <p class="wa-inner-title xui-inner-title" {{this.is_itemname_hidden}}> \
                                    {{this.name}}</p> \
                                <p class="wa-inner-price xui-inner-price" {{this.is_price_hidden}}> \
                                    <span>¥</span>{{this.display_price}}</p> \
                          </div> \
                        </a> \
                    </li> \
                {{/each}} \
            </ul> \
        </div>\
    ';
    templateProductList = Handlebars.compile(productListTemplate);

    // 初始化view    
    var initComponent = function(component, idx){
        var $div = component;
        var componentType = $div.attr('data-type');
        var componentModel = $.parseJSON($div.attr('data-model') || '{}');
        var asyncComponent = new AsyncComponentLoadView({
            el: $div[0],
            componentType: componentType,
            componentModel: componentModel,
        });

        $div.data('view', asyncComponent);
    };

    allComponents.map(function(component, idx){
        initComponent(component, idx);
    });
});

})(W);

