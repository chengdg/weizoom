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
        this.component = {
            component: {
                model: options.componentModel,
                type: options.componentType
            }
        };
        console.log('>>>>>>>>>> options: ', options, this.component);
        //this.handlebarTmpl = $("#componentTemplates").html();
        var productListTemplate = '\
            <div class="xa-products-box wui-product wui-productTitle"> \
                <ul class="wui-block-type{{component.model.type}} wui-card-type-{{component.model.card_type}}"> \
                    {{#each component.components}} \
                        <li data-component-cid="{{component.cid}}" \
                          data-index="{{component.model.index}}"> \
                              <a class="wui-inner-box xa-member-product wa-item-product" href="javascript:void(0);" data-handlebar-data=\'{ "index":"{{index}}", "product":{"thumbnails_url":"{{this.thumbnails_url}}", "name":"{{this.name}}", "display_price":"{{this.display_price}}"} }\' data-product-promotion="{{this.promotion_js}}" data-product-price="{{this.display_price}}"> \
                                <div class="wui-inner-pic"> <img src="{{this.thumbnails_url}}" /> <p>{{this.name}}</p> </div> \
                            </a> \
                        </li> \
                    {{/each}} \
                </ul> \
            </div>\
        ';
        //this.template = Handlebars.compile(this.handlebarTmpl);
        this.template = Handlebars.compile(productListTemplate);
        var deferred = $.Deferred();
        this.sendApi(deferred);
        var _this = this;
        $.when(deferred).done(function(data){
            // 根据商品数量填补component对象
            _this.component['component']['valid_product_count'] = data['products'].length;
            _this.component['component']['components'] = [];
            data.products.map(function(product){
                _this.component['component']['components'].push(product);
            });
            console.log('>>>>>>>>>>>> 异步获取数据后补充component：', _this.component);
            var orgHtml = _this.renderComponent(_this.component, data);
            //var orgHtml = _this.template(_this.component);
            _this.$el.html(orgHtml);
            // 停止渲染子组件
            //var $eleUl = _this.$el.find('ul');
            //_this.renderSub($eleUl, data);
        });
    },

    sendApi: function(deferred) {
        var _this = this;
        var product_ids = this.componentModel['items'];
        console.log(product_ids);
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
        console.log('渲染主标签：');
        console.log('>>>>>>>>> component: ', component, subData);
        console.log('>>>>>>>>>> renderComponent begin ', component);
        var html = this.template(component);
        console.log('>>>>>>>>>> renderComponent end ', html);
        return html;
    },

    // 渲染子标签
    renderSub: function($el, data) {
        var _this = this;
        console.log('>>>>>>>>> 异步接口: ', data);
        var product_ids = this.componentModel['items'];
        var products = data['products'];
        var sub_component_htmls = [];
        product_ids.forEach(function(product_id) {
            var product = _.find(products, function(item){return item.id === product_id});
            console.log(product_id, product);
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
});

var allComponents = [];
$(function(){
    $('div[data-ui-role="async-component"]').each(function() {
        var $div = $(this);
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

    //var componentsTmpl = $("#componentTemplates").html();
    var componentsTmpl = $("#productListTemplate").html();
    allComponents.map(function(component, idx){
        if (idx < 1) {
            var $div = component;
            var componentType = $div.attr('data-type');
            var componentModel = $.parseJSON($div.attr('data-model') || '{}');
            var asyncComponent = new AsyncComponentLoadView({
                el: $div[0],
                componentType: componentType,
                componentModel: componentModel,
            });

            $div.data('view', asyncComponent);
        }
    });
});

})(W);

