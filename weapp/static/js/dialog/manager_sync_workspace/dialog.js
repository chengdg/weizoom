/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.weapp.dialog');
W.weapp.dialog.SyncWorkspaceDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-sync-workspace-dialog-tmpl-src').template('manager-sync-workspace-dialog-tmpl');
        return "manager-sync-workspace-dialog-tmpl";
    },

    makeCheckboxes: function(options) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            buf.push('<label class="checkbox"><input type="checkbox" value="' + option.value + '"/>' + option.name + '</label>');
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        W.getApi().call({
            app: 'webapp',
            api: 'modules/get',
            args: {},
            scope: this,
            success: function(data) {
                console.log(data);
                console.log("\n\n\n\n\niiiiiii");
                var $dialogBody = this.$dialog.find('#syncWorkspaceDialog-workspaces').append(this.makeCheckboxes(data));
            },
            error: function(resp) {
                alert('获得module集合失败');
            }
        })
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var data = [];
        this.$dialog.find('#syncWorkspaceDialog-workspaces input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            if ($checkbox.is(":checked")) {
                data.push($checkbox.val());
            }
        });
        this.$dialog.find('#syncWorkspaceDialog-workspaces').empty();

        var $notAllowUpdateCheckbox = this.$dialog.find('input[name="notAllowUpdate"]');
        var allowUpdate = !$notAllowUpdateCheckbox.is(':checked');
        $notAllowUpdateCheckbox.attr('checked', 'checked');

        return JSON.stringify({'modules':data, 'allow_update':allowUpdate});
    }
});