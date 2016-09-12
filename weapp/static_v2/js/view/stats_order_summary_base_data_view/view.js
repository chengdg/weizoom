/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * QrcodeOrderAdvancedTable: 继承AdvancedTable，实现arterLoad函数
 * auther: nanxuezhi
 */
ensureNS('W.view.stats');

W.view.stats.OrderSummaryBaseDataAdvancedTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        var order_num = 0;
        var paid_amount = 0.0;
        var unit_price = 0.0;
        var product_num = 0;
        var discount_amount = 0.0;

        this.items.each(function(item){
            order_num = item.get('order_num');
            paid_amount = item.get('paid_amount').toFixed(2);
            product_num = item.get('product_num');
            discount_amount = item.get('discount_amount').toFixed(2);
        });
        if (order_num > 0) {
            unit_price = (paid_amount / order_num).toFixed(2);
        }

        $('#order_num').text(order_num);
        $('#paid_amount').text("￥"+ paid_amount);
        $('#unit_price').text("￥"+ unit_price);
        $('#product_num').text(product_num);
        $('#discount_amount').text("￥"+ discount_amount);
    }
})

W.registerUIRole('div[data-ui-role="order-summary-base-data-advanced-table"]', function() {
    var $div = $(this);
    var app = $div.attr('data-app');
    var api = $div.attr('data-api');
    var resource = $div.attr('data-resource');
    if (resource) {
        api = resource;
    }
    var args = $div.attr('data-args');
    var template = $div.attr('data-template-id');
    var initSort = $div.attr('data-init-sort');
    var enablePaginator = $div.data('enablePaginator');
    var enableSort = !!($div.attr('data-enable-sort') === 'true');
    var enableSelect = !!($div.attr('data-selectable') === 'true');
    var disableHeaderSelect = !!($div.attr('data-disable-header-select') === 'true');
    var selectableTrSelector = $div.data('selecttableTr');
    //var onlyShowFrontSelect = !!($div.attr('data-only-show-front-select') === 'true');
    var sortApi = $div.attr('data-sort-api');
    var itemCountPerPage = $div.attr('data-item-count-per-page');
    var userWebappId = $div.attr('data-user-webapp-id');
    var outerSelecter = $div.attr('data-outer-selecter');

    var autoLoad = $div.data('autoLoad');
    if (autoLoad !== false) {
        autoLoad = true;
    }

    if (itemCountPerPage) {
        itemCountPerPage = parseInt(itemCountPerPage);
    } else {
        itemCountPerPage = 15;
    }

    var advancedTable = new W.view.stats.OrderSummaryBaseDataAdvancedTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
        initSort: initSort,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        enableSelect: enableSelect,
        disableHeaderSelect: disableHeaderSelect,
        //onlyShowFrontSelect: onlyShowFrontSelect,
        selectableTrSelector: selectableTrSelector,
        sortApi: sortApi,
        userWebappId: userWebappId,
        autoLoad: autoLoad,
        outerSelecter: outerSelecter
    });
    advancedTable.render();

    $div.data('view', advancedTable);
});
