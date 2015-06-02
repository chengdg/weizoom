/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.common');
W.dialog.common.CommonViperDialog = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#common-viper-dialog-tmpl-src').template('common-viper-dialog-tmpl');
        return "common-viper-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.projectId = options.projectId;
        this.pageId = options.pageId;
    },

    onShow: function(options) {
        W.getLoadingView().show();
        var _this = this;
        W.getApi().call({
            app: 'workbench',
            api: 'viper_design_page_by_id/create',
            args: {
                project_id: this.projectId,
                page_id: this.pageId
            },
            success: function(data) {
                W.getLoadingView().hide();
                _this.$dialog.find('h3').text(data['title']);
                _this.$dialog.find('.modal-body').html(data['html']);
                _.delay(function() {
                    _this.$dialog.find('input[type="text"]').focus();
                }, 300);
            },
            error: function(resp) {
                W.getLoadingView().hide();
            }
        })
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        var s = 'http://a.com/?' + this.$dialog.find('form').serialize();
        return parseUrl(s)['query'];
    }
});