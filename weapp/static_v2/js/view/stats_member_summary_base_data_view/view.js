/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * QrcodeOrderAdvancedTable: 继承AdvancedTable，实现arterLoad函数
 * auther: duhao
 */
ensureNS('W.view.stats');

W.view.stats.MemberSummaryBaseDataAdvancedTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        var total_member_count = 0;
        var subscribed_member_count = 0;
        var new_member_count = 0;
        var binding_phone_member_count = 0;
        var bought_member_count = 0;
        var repeat_buying_member_rate = 0;
        var ori_qrcode_member_count = 0;
        var share_url_member_count = 0;
        var member_from_qrcode_count = 0;
        var self_follow_member_count = 0;
        var member_from_share_url_count = 0;
        var member_recommend_rate = 0;

        this.items.each(function(item){
            total_member_count = item.get('total_member_count');
            subscribed_member_count = item.get('subscribed_member_count');
            new_member_count = item.get('new_member_count');
            binding_phone_member_count = item.get('binding_phone_member_count');
            bought_member_count = item.get('bought_member_count');
            repeat_buying_member_rate = item.get('repeat_buying_member_rate');
            ori_qrcode_member_count = item.get('ori_qrcode_member_count');
            share_url_member_count = item.get('share_url_member_count');
            member_from_qrcode_count = item.get('member_from_qrcode_count');
            self_follow_member_count = item.get('self_follow_member_count');
            member_from_share_url_count = item.get('member_from_share_url_count');
            member_recommend_rate = item.get('member_recommend_rate');
        });

        
        if(total_member_count > 0) {
            $('#total_member_count').text('');
            $('#total_member_count').append('<a href="/member/members/get/" target="_blank">' + total_member_count + '</a>');
        } else {
            $('#total_member_count').text(total_member_count);
        }
        if(subscribed_member_count > 0) {
            $('#subscribed_member_count').text('');
            $('#subscribed_member_count').append('<a href="/member/members/get/?status=1" target="_blank">' + subscribed_member_count + '</a>');
        } else{
            $('#subscribed_member_count').text(subscribed_member_count);
        }
        $('#new_member_count').text(new_member_count);
        $('#binding_phone_member_count').text(binding_phone_member_count);
        $('#bought_member_count').text(bought_member_count);
        $('#repeat_buying_member_rate').text(repeat_buying_member_rate);
        $('#ori_qrcode_member_count').text(ori_qrcode_member_count);
        $('#share_url_member_count').text(share_url_member_count);
        $('#member_from_qrcode_count').text(member_from_qrcode_count);
        $('#self_follow_member_count').text(self_follow_member_count);
        $('#member_from_share_url_count').text(member_from_share_url_count);
        $('#member_recommend_rate').text(member_recommend_rate);
    }
})

W.registerUIRole('div[data-ui-role="member-summary-base-data-advanced-table"]', function() {
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

    var advancedTable = new W.view.stats.MemberSummaryBaseDataAdvancedTable({
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
