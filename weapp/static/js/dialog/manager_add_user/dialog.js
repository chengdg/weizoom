/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.weapp.dialog.AddUserDialog');
W.weapp.dialog.AddUserDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-add-user-dialog-tmpl-src').template('manager-add-user-dialog-tmpl');
        return "manager-add-user-dialog-tmpl";
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
        var name = $.trim(this.$dialog.find('input[name="name"]').val());
        if (name.length == 0) {
            alert('请输入用户名');
            return false;
        }

        var password = $.trim(this.$dialog.find('input[name="password"]').val());
        if (password.length == 0) {
            alert('请输入用户密码');
            return false;
        }

        if (event.alreadyCheckDuplicate) {
            return {
                name: name,
                password: password
            };
        } else {
            W.getApi().call({
                app: 'account',
                api: 'new_username/check',
                args: {
                    name: name
                },
                scope: this,
                success: function(data) {
                    event.alreadyCheckDuplicate = true;
                    this.onClickSubmitButton(event);
                },
                error: function(resp) {
                    alert('用户名"'+name+'"已被使用，请重新输入');
                }
            });
            return false;
        }
    }
});