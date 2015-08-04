/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 系统用户账号信息对话框
 * 
 * author: chuter
 */
ensureNS('W.weapp.dialog.SystemAccountDialog');

W.weapp.dialog.SystemAccountDialog = W.dialog.Dialog.extend({

    getTemplate: function() {
        $('#system-account-dialog-tmpl-src').template('system-account-dialog-tmpl');
        return "system-account-dialog-tmpl";
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
        $('#old_password').val('');
        $('#new_password').val('');
        $('#repeat_new_password').val('');

        $('#old_password').focus().select();

        $(document).keypress(function(e) {
            if(e.which !== 13) {
                return;
            }

            var $focused = $(':focus');
            if ($focused.attr('name') == 'old_password') {
                $('#new_password').focus().select();
            } else if ($focused.attr('name') == 'new_password') {
                $('#repeat_new_password').focus().select();
            } else if ($focused.attr('name') == 'repeat_new_password') {
                $('#change_password').trigger('click');
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        $('#old_password').focus().select();

        if (!W.validate($('#change_password_dialog'))) {
            return false;
        }

        $('#change_password').attr('disabled','disabled');
        W.getLoadingView().show();

        var _this = this;

        this.onGetDataAsync(event, function(data) {
            _this.$dialog.modal('hide');
            if (_this.successCallback) {
                //调用success callback
                var task = new W.DelayedTask(function() {
                    _this.successCallback(data);
                    _this.successCallback = null;
                });
              
                task.delay(100);
            }
        }, function() {
            W.getLoadingView().hide();
            $('#change_password').removeAttr('disabled');
        });
    },

    onGetDataAsync: function(event, success_callback, failed_callback) {
        // W.getLoadingView().show();
        var oldPassword = $.trim(this.$dialog.find('input[name="old_password"]').val());
        var newPassword = $.trim(this.$dialog.find('input[name="new_password"]').val());
        var repeatNewPassword = $.trim(this.$dialog.find('input[name="repeat_new_password"]').val());

        if (newPassword != repeatNewPassword) {
            W.getErrorHintView().show('两次输入的密码不同，请重新填写！');
            failed_callback();
            return false;
        }

        //校验是否完成绑定
        W.getApi().call({
            method: 'post',
            app: 'account',
            api: 'user/update',
            async: false,
            args: {
                old_password: oldPassword,
                new_password: newPassword,
            },
            scope: this,
            success: function(data) {
                success_callback(data);
            },
            error: function(resp) {
                //TODO 进行错误通知
                W.getErrorHintView().show('修改失败: ' + resp.errMsg);
                failed_callback();
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
    }
});