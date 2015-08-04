/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.termite');
W.dialog.termite.SetTemplateCoverDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-preview': 'onClickPreview'
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#termite-manager-set-template-cover-dialog-tmpl-src'
    },

    onInitialize: function(options) {
    },

    showImage: function(coverName) {
        var imgSrc = '/static_v2/img/termite2/cover/' + coverName;
        this.$dialog.find('.xa-previewText').hide();
        this.$dialog.find('.xa-previewImage').attr('src', imgSrc).show();
    },

    showPreviewText: function(coverName) {
        this.$dialog.find('.xa-previewImage').hide().attr('src', '');
        this.$dialog.find('.xa-previewText').show();
    },

    onShow: function(options) {
        if (options.coverName) {
            var items = options.coverName.split('/');
            var coverName = items[items.length-1];
            this.$dialog.find('[name="coverName"]').val(coverName);
            this.showImage(coverName);
        } else {
            this.$dialog.find('[name="coverName"]').val('');
            this.showPreviewText();
        }
    },

    afterShow: function(options) {
        this.$dialog.find('[name="coverName"]').focus();
    },

    onClickPreview: function(event) {
        var $input = this.$dialog.find('[name="coverName"]');
        var coverName = $.trim($input.val());
        if (coverName.length === 0) {
            return;
        }

        this.showImage(coverName);
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        var $input = this.$dialog.find('[name="coverName"]');
        var coverName = $.trim($input.val());
        var url = '/static_v2/img/termite2/cover/' + coverName;
        return {coverName:coverName, url:url};
    }
});