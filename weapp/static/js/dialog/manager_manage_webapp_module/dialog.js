/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.weapp.dialog.ManageModuleDialog');
W.weapp.dialog.ManageModuleDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-manage-webapp-module-dialog-tmpl-src').template('manager-manage-webapp-module-dialog-tmpl');
        return "manager-manage-webapp-module-dialog-tmpl";
    },

    makeCheckboxes: function(options, installedModuleIdSet) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            if (installedModuleIdSet[option.value]) {
                buf.push('<label class="checkbox"><input type="checkbox" checked="checked" value="' + option.value + '"/>' + option.name + '</label>');
            } else {
                buf.push('<label class="checkbox"><input type="checkbox" value="' + option.value + '"/>' + option.name + '</label>');
            }
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
    },

    beforeShow: function() {
        this.$dialog.find('.modal-body').empty();
    },

    onShow: function(options) {
        var installedModuleIdSet = {};
        _.each(options.installedModuleIds, function(id) {
            installedModuleIdSet[id] = true;
        });
        xwarn(installedModuleIdSet);
        W.getApi().call({
            app: 'webapp',
            api: 'installed_modules/get',
            args: {},
            scope: this,
            success: function(data) {
                this.$dialog.find('.modal-body').append(this.makeCheckboxes(data, installedModuleIdSet));
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
        this.$dialog.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            if ($checkbox.is(":checked")) {
                data.push(parseInt($checkbox.val()));
            }
        });

        return JSON.stringify(data);
    }
});