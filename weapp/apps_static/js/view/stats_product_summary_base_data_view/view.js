/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * QrcodeOrderAdvancedTable: 继承AdvancedTable，实现arterLoad函数
 * auther: duhao
 */
ensureNS('W.view.weixin');

W.view.weixin.ProductSummaryBaseDataAdvancedTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        $('#buy_num_help').popover({
            content : "<div class='xui-i-alert'>购买商品的总人数</div>",
            trigger : "hover",
            html : true,
            placement : "bottom"
        });

        $('#order_count_help').popover({
            content : "<div class='xui-i-alert'>当前所选时段内该店铺已发货、待发货、已完成的订单数之和</div>",
            trigger : "hover",
            html : true,
            placement : "bottom"
        });

        $('#deal_product_count_help').popover({
            content : "<div class='xui-i-alert'>当前所选时段内所有成交订单内商品总件数</div>",
            trigger : "hover",
            html : true,
            placement : "bottom"
        });
    }
})

W.registerUIRole('div[data-ui-role="product-summary-base-data-advanced-table"]', function() {
    xlog("registed product-summary-base-data-advance-table");
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

    var advancedTable = new W.view.weixin.ProductSummaryBaseDataAdvancedTable({
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
