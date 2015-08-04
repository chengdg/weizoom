/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * QrcodeOrderAdvancedTable: 继承AdvancedTable，实现arterLoad函数
 * auther: duhao
 */
ensureNS('W.view.stats');

W.view.stats.ManageSummaryBaseDataAdvancedTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        var repeat_buying_member_rate = 0;
        var member_recommend_rate = 0;
        var repeat_buying_product_rate = 0;
        var product_recommend_rate = 0;
        var transaction_money = 0;
        var transaction_orders = 0;
        var buyer_count = 0;
        var vis_price = 0;
        var ori_qrcode_member_count = 0;
        var member_from_qrcode_count = 0;
        var share_url_member_count = 0;
        var member_from_share_url_count = 0;

        this.items.each(function(item){
            repeat_buying_member_rate = item.get('repeat_buying_member_rate');
            member_recommend_rate = item.get('member_recommend_rate');
            repeat_buying_product_rate = item.get('repeat_buying_product_rate');
            product_recommend_rate = item.get('product_recommend_rate');
            transaction_money = item.get('transaction_money');
            transaction_orders = item.get('transaction_orders');
            buyer_count = item.get('buyer_count');
            vis_price = item.get('vis_price');
            ori_qrcode_member_count = item.get('ori_qrcode_member_count');
            member_from_qrcode_count = item.get('member_from_qrcode_count');
            share_url_member_count = item.get('share_url_member_count');
            member_from_share_url_count = item.get('member_from_share_url_count');
        });

        $('#repeat_buying_member_rate').text(repeat_buying_member_rate);
        $('#member_recommend_rate').text(member_recommend_rate);
        $('#repeat_buying_product_rate').text(repeat_buying_product_rate);
        $('#product_recommend_rate').text(product_recommend_rate);
        $('#transaction_money').text(transaction_money);
        $('#transaction_orders').text(transaction_orders);
        $('#buyer_count').text(buyer_count);
        $('#vis_price').text(vis_price);
        $('#ori_qrcode_member_count').text(ori_qrcode_member_count);
        $('#member_from_qrcode_count').text(member_from_qrcode_count);
        $('#share_url_member_count').text(share_url_member_count);
        $('#member_from_share_url_count').text(member_from_share_url_count);
    }
})

W.registerUIRole('div[data-ui-role="manage-summary-base-data-advanced-table"]', function() {
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

    var advancedTable = new W.view.stats.ManageSummaryBaseDataAdvancedTable({
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
