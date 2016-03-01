/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择促销商品对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.OffShelfProductsListDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-search': 'onClickSearch'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-offshelf-products-list-dialog-tmpl-src').template('mall-offshelf-products-list-dialog-tmpl');
        return "mall-offshelf-products-list-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function() {
        this.table.reset();
        this.$('#start_date').val("");
        this.$('#end_date').val("");
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
        this.table.reload({
            start_date:"",
            endDate: ""
        });
    },
    onClickSearch:function(){
        var startDate = $.trim(this.$('#start_date').val());
        var endDate = $.trim(this.$('#end_date').val());
        if(startDate == "" || endDate == ""){
            this.$dialog.modal('hide');
        }else{
            var data = {
                startDate: startDate,
                endDate: endDate,
            }
            this.table.reload(data, {
                emptyDataHint: '没有符合条件的商品'
            }); 
        }
    },
});
