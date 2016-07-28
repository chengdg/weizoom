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
        this.sendApi();
    },

    sendApi: function() {
        var _this = this;
        var product_ids = this.componentModel['items'];
        console.log(product_ids);
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'page_products/get',
                product_ids: product_ids
            },
            success: function(data) {
                _this.render(data);
            },
            error: function(data) {

            }
        });
    },

    render: function(data) {
        var _this = this;
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
        this.$el.html(sub_component_htmls.join(''));
    },

    addSubComponetRender: function(component) {
        // TODO: 使用handlebar-template 渲染 
        return "<div>"+component.name+"</div>"
    }
});

$(function() {
    $('div[data-ui-role="async-component"]').each(function() {
        var $div = $(this);
        var componentType = $div.attr('data-type');
        var componentModel = $.parseJSON($div.attr('data-model') || '{}');
        var asyncComponent = new AsyncComponentLoadView({
            el: $div[0],
            componentType: componentType,
            componentModel: componentModel,
        });
        // asyncComponent.render();

        $div.data('view', asyncComponent);
    });
})

})(W);
