/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择批量发货的对话框
 *
 * author: robert
 */
ensureNS('W.dialog.common');

W.dialog.common.OrderBatchDeliverDialog = W.dialog.Dialog.extend({

    getTemplate: function() {
        $('#common-order-batch-deliver-dialog-tmpl-src').template('common-order-batch-deliver-dialog-tmpl');
        return "common-order-batch-deliver-dialog-tmpl";
    },

    onInitialize: function(options) {
        var $imageInput = this.$('[name="file_url"]');
        var imageWidth = options.imageWidth;
        var imageHeight = options.imageHeight;
        var $csvView = this.$dialog.find('#commonSelectCSVFileDialog-fileView');
        var isMulti = options.isMulti || false;
        this.maxCount = options.imgCount || -1;
        this.csvView = new W.view.common.CVSView({
            el: $csvView.get(),
            height: imageHeight,
            width: 84,
            autoShowHelp: true,
            isMulti: isMulti
        });
        this.csvView.bind('upload-file-success', function(path) {
            var value = $imageInput.val();
            if (value.length > 0) {
                value += ','+ path;
            }else{
                value = path;
            }
            $imageInput.val(value);
            if (!W.validate($('[name="file_url"]'))) {
                return false;
            }
        });
        this.csvView.bind('delete-file', function(path) {
            $imageInput.val('');

        });
        this.csvView.render();
    },

    onShow: function(options) {
        this.maxCount = options.imgCount || -1;
    },

    afterShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“批量发货”按钮后的响应函数
     */
    onGetData: function(event) {
        xlog('in get data...');
        var url = this.$('[name="file_url"]').val();
        if (!W.validate($('[name="file_url"]'))) {
            return false;
        }
        this.csvView.cleanImage();
        return url;
    }
});