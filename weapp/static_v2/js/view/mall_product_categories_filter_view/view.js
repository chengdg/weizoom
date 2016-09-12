ensureNS('W.view.mall');
W.view.mall.ProductCategoriesFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-product-categories-filter-view-tmpl-src').template('mall-product-categories-filter-view-tmpl');
        return 'mall-product-categories-filter-view-tmpl';
    },
    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.filter_value = '';
    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {});
        this.$el.append(html);
        this.table = $('#categories-list-view').data('view');
    },

    onClickSearchButton: function(){
        var data = this.getFilterData();
        this.table.reload(data);
    },

    onClickResetButton: function(){
        $('#product_name').val('');
        $('#category_name').val('');
    },

    // 获取条件数据
    getFilterData: function(){
        var data = {
            product_name: $('#product_name').val(),
            category_name:$('#category_name').val()
        };
        console.log('onClickSearchButton>>>>filter_value>>>',JSON.stringify(data));
        return data;
    },

});
