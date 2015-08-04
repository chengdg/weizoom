/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.weapp.dialog.AddWorkspaceDialog');
W.weapp.dialog.AddWorkspaceDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-add-workspace-dialog-tmpl-src').template('manager-add-workspace-dialog-tmpl');
        return "manager-add-workspace-dialog-tmpl";
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);        
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var $nameInput = this.$dialog.find('input[name="name"]');
        var name = $.trim($nameInput.val());
        if (!name) {
            alert('请输入项目名');
            return false;
        }

        var $innerNameInput = this.$dialog.find('input[name="inner_name"]');
        var innerName = $.trim($innerNameInput.val());
        if (!innerName) {
            alert('请输入内部名');
            return false;
        }

        $nameInput.val('');
        $innerNameInput.val('');
        return {
            name: name,
            innerName: innerName
        };
    }
});