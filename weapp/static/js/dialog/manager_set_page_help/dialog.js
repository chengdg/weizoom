/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.manager');
W.dialog.manager.SetPageHelpDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-set-page-help-dialog-tmpl-src').template('manager-set-page-help-dialog-tmpl');
        return "manager-set-page-help-dialog-tmpl";
    },

    makeRadios: function(options, targetValue) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            
            if (targetValue && (targetValue === option.id)) {
                buf.push('<label class="radio"><input name="document" type="radio" checked="checked" value="' + option.id + '"/>' + option.title + "</label>");
            } else {
                buf.push('<label class="radio"><input name="document" type="radio" value="' + option.id + '"/>' + option.title + "</label>");
            }
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        W.getApi().call({
            app: 'help',
            api: 'document_targets/get',
            args: {
                page_id: options.pageId
            },
            scope: this,
            success: function(data) {
                var links = data.links;
                var pageHelpDocumentId = data.page_help_document_id;
                this.$dialog.find('.modal-body').empty().append(this.makeRadios(links, pageHelpDocumentId));
            },
            error: function(resp) {
                alert('获得帮助文档失败');
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var pageHelpDocumentId = $('input[name="document"]:checked').val();

        return pageHelpDocumentId;
    }
});