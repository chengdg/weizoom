ensureNS('W.view.mall');
W.view.mall.ProductsPoolFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-products-pool-filter-view-tmpl-src').template('mall-products-pool-filter-view-tmpl');
        return 'mall-products-pool-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton',
        'change #firstClassification': 'onChangeEvent'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        // this.filter_value = '';
        // this.bind('clickStatusBox', this.clickStatusBox);
    },

    render: function() {
        W.resource.mall2.ProductClassification.get({
            scope: this,
            data: {'level': 1},
            success: function(data) {
                var classifications = data.items;
                var html = $.tmpl(this.getTemplate(), {
                    classifications: classifications
                });
                this.$el.append(html);
            },
            error: function() {
                alert('加载失败！请刷新页面重试！');
            }
        })
    },

    onClickSearchButton: function(){
        var data = this.getFilterData();
    },

    onClickResetButton: function(){
        $('#productCode').val('');
        $('#name').val('');
        $('#supplier').val('');
        $('#firstClassification').val('-1');
        $('#secondaryClassification').val('-1');
    },

    onChangeEvent: function() {
        var $target = $(event.target);
        var father_id = $target.val();
        W.resource.mall2.ProductClassification.get({
            scope: this,
            data: {'level': 2, 'father_id': father_id},
            success: function(data) {
                console.log(data);

            },
            error: function() {
                alert('加载失败！请刷新页面重试！');
            }
        })
    },

    // 获取条件数据
    getFilterData: function(){
        //商品编号
        var productCode = $.trim(this.$('#productCode').val());

        //商品名
        var name = $.trim(this.$('#name').val());

        //供货商
        var supplier = $.trim(this.$('#supplier').val());

        //一级分类
        var firstClassification = this.$('#firstClassification').val();
        //二级分类
        var secondaryClassification = this.$('#secondaryClassification').val();

        var data = {
            product_code: productCode,
            name: name,
            supplier: supplier,
            first_classification: firstClassification,
            secondary_classification: secondaryClassification
        }
        this.trigger('search', data);
    },
});
