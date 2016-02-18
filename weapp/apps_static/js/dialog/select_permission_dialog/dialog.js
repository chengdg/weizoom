/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单支付弹出框
 * 
 * author: robert
 */
ensureNS('W.dialog.auth');

W.dialog.auth.SelectPermissionDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#auth-select-permission-dialog-tmpl-src').template('auth-select-permission-dialog-tmpl');
        return "auth-select-permission-dialog-tmpl";
    },

    getPermissionsTemplate: function() {
        $('#auth-select-permission-dialog-permissions-tmpl-src').template('auth-select-permission-dialog-permissions-tmpl');
        return "auth-select-permission-dialog-permissions-tmpl";
    },

    events: _.extend({
        'click input[type="checkbox"]': 'onClickPermission',
        'click .xa-close':'onClickDialogHide'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.permissionsTemplate = this.getPermissionsTemplate();
    },

    beforeShow: function(options) {
        this.$('.modal-body').empty();
    },

    onShow: function(options) {
        this.roleId = options.roleId;
        this.userId = options.userId;
        this.checkedRoleIds = options.checkedRoleIds;
        this.checkedUserPermissionIds = options.checkedUserPermissionIds;
    },

    afterShow: function(options) {
        var args = {type: 'action'};
        if (this.roleId) {
            var api = 'role_permissions/get';
            args.id = this.roleId;
        } else {
            var api = 'account_permissions/get';
            args.id = this.userId;
            if (this.checkedRoleIds) {
                args['specific_role_ids'] = this.checkedRoleIds;
            }
            if (this.checkedUserPermissionIds) {
                args['specific_user_permission_ids'] = this.checkedUserPermissionIds;
            }
        }
        W.getApi().call({
            app: 'auth',
            api: api,
            args: args,
            scope: this,
            success: function(data) {
                //var $node = $.tmpl(this.permissionsTemplate, {permissions:data});
                var html = data
                this.$('.modal-body').append(html);
            },
            error: function(resp) {
                W.showHint('error', '加载角色权限失败!')
            }
        })
    },
    onClickDialogHide:function(event){
        this.$dialog.modal('hide');
    },
    onClickPermission: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');

        if (!$checkbox.data('isLeaf')) {
            var isChecked = $checkbox.is(':checked');
            $checkbox.parents('.xa-node').eq(0).find('input').each(function() {
                var $checkbox = $(this);
                if (!$checkbox.is(':disabled')) {
                    $checkbox.prop('checked', isChecked);
                }
            });
        } 
        
        if (!isChecked) {
            //检查是否有上级非叶节点需要取消选中
            $checkbox.parents('.xa-node').each(function() {
                var $node = $(this);
                $node.find('input[data-is-leaf="false"]').eq(0).prop('checked', false);
            });
        } else {
            //检查是否有上级非叶节点需要选中
            $checkbox.parents('.xa-node').each(function() {
                var $node = $(this);
                var $checkboxs = $node.find('input[data-is-leaf="true"]');
                var checkboxCount = $checkboxs.length;
                for (var i = 0; i < checkboxCount; ++i) {
                    var $checkbox = $checkboxs.eq(i);
                    if (!$checkbox.is(':checked')) {
                        //有一个未选中的checkbox，退出
                        return;
                    }
                }

                $node.find('input[data-is-leaf="false"]').eq(0).prop('checked', true);
            });
        }
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var ids = [];
        this.$('input[type="checkbox"]:checked').each(function() {
            var $checkbox = $(this);
            if ($checkbox.is(':disabled')) {
                return;
            }

            ids.push($checkbox.data('id'));
        });

        return ids;
    }
});