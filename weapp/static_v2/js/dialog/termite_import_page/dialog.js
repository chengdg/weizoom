/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.termite');
W.dialog.termite.ImportPageDialog = W.dialog.Dialog.extend({
    templates: {
        dialogTmpl: "#termite-import-page-dialog-tmpl-src"
    },

    onInitialize: function(options) {
        var $fileUploader = this.$dialog.find('.xa-uploader').eq(0);
        $fileUploader.uploadify({
            swf: '/static/uploadify.swf',
            multi: false,
            removeCompleted: true,
            uploader: '/termite2/api/project/',
            cancelImg: '/static/img/cancel.png',
            buttonText: '选择工程ZIP...',
            fileTypeDesc: '工程Zip文件',
            fileTypeExts: '*.zip',
            method: 'post',
            formData: {
                field: 'page_content_from_zip',
                id: W.projectId
            },
            removeTimeout: 0.0,
            onUploadSuccess: function(file, path, response) {
                window.location.reload();
            },
            onUploadComplete: function() {},
            onUploadError: function(file, errorCode, errorMsg, errorString) {
                xlog(errorCode);
                xlog(errorMsg);
                xlog(errorString);
            }
        });
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        return {success:true};
    }
});