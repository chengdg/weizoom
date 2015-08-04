/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.weixin');
W.dialog.weixin.SelectMaterialDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#weixin-select-material-dialog-tmpl-src').template('weixin-select-material-dialog-tmpl');
        return "weixin-select-material-dialog-tmpl";
    },

    getOneNewsTemplate: function() {
        $('#weixin-select-material-dialog-one-news-tmpl-src').template('weixin-select-material-dialog-one-news-tmpl');
        return 'weixin-select-material-dialog-one-news-tmpl-src';
    },

    onInitialize: function(options) {
        var newsesView = new W.view.weixin.MaterialListView({
            el: '#selectMaterialDialog-materials',
            enableEdit: false
        });
        newsesView.render();

        this.selectableBehavior = new W.view.common.SelectableBehavior({
            el: '#selectMaterialDialog-materials',
            isRadio: true
        });
    },

    onShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var data = [];
        this.selectableBehavior.getSelectedItems().each(function() {
            var $selectedItem = $(this);
            data.push($selectedItem.attr('data-id'));
        });
        
        return data;
    }
});