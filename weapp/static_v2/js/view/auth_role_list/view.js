ensureNS('W.view.auth');
W.view.auth.RoleList = Backbone.View.extend({
    getPermissionListTemplate:function() {
        $('#auth-role-list-view-permission-tmpl-src').template('auth-role-list-view-role-info-tmpl');
        return 'auth-role-list-view-role-info-tmpl';
    },

    events:  {
        'click .xa-addRole': 'onClickAddRoleButton',
        'click .xa-addPermission': 'onClickAddPermissionButton',
        'keypress .xa-roleNameInput': 'onKeyPressInRoleNameInput',
        'blur .xa-roleNameInput': 'onLeaveRoleNameInput',
        'click .xa-config': 'onClickConfigButton',
        'click .xa-role': 'onClickRole'
    },
    
    initialize: function(options) {
        this.template = _.template(
            '<li data-id="<%= id %>">\
                <a href="javascript:void(0)" class="xui-i-role xui-i-activeRole xa-role">\
                    <span class="caret"></span>\
                    <span class="xui-name xa-name"><%= name %></span>\
                    <input type="text" class="form-control xui-i-input xa-roleNameInput" style="display: none"/>\
                    <span class="glyphicon glyphicon-cog xui-i-config xa-config"></span>\
                </a>\
            </li>'
        );

        this.$menu = $('.xa-roleActionMenu').eq(0);
        this.isShowMenu = false;
        this.actionRoleId = null;

        var _this = this;
        $document = $(document);
        $document.delegate('.xa-renameRole', 'click', _.bind(this.onClickRenameRoleButton, this));
        $document.delegate('.xa-deleteRole', 'click', _.bind(this.onClickDeleteRoleButton, this));
        $document.click(function() {
            _this.hideActionMenu();
        });

        this.permissionListTemplate = this.getPermissionListTemplate();
    },

    render: function() {
        var roleId = this.$('.xui-i-activeRole').parents('li').data('id');
        if (roleId) {
            this.loadRolePermissions(roleId);
        }
    },

    createRole: function($role) {
        var roleName = $.trim($role.find('.xa-roleNameInput').val());
        if (!roleName) {
            W.showHint('error', '角色名不能为空');
            return;
        }

        W.getApi().call({
            method: 'post',
            app: 'auth',
            api: 'role/create',
            args: {
                name: roleName
            },
            scope: this,
            success: function(data) {
                var roleId = data;
                this.$('.xa-roleList li').eq(0).remove();
                var $node = $(this.template(data));
                $node.addClass('.xui-i-activeRole');
                this.$('.xui-i-activeRole').removeClass('xui-i-activeRole');
                this.$('.xa-roleList').prepend($node);

                this.loadRolePermissions(roleId, true);
            },
            error: function(resp) {
                if(resp.data.msg)
                    W.showHint('error', resp.data.msg);
                else
                    W.showHint('error', '创建角色失败!');
            }
        })
    },

    updateRole: function($role, roleId) {
        var roleName = $.trim($role.find('.xa-roleNameInput').val());
        if (!roleName) {
            W.showHint('error', '角色名不能为空');
            return;
        }

        W.getApi().call({
            method: 'post',
            app: 'auth',
            api: 'role/update',
            args: {
                id: roleId,
                name: roleName
            },
            scope: this,
            success: function(data) {
                $role.find('.xa-roleNameInput').hide();
                $role.find('.xa-name').text(roleName).show();
                $role.find('.xa-config').show();                
            },
            error: function(resp) {
                if(resp.data.msg)
                    W.showHint('error', resp.data.msg);
                else
                    W.showHint('error', '更新角色失败!');
            }
        })
    },

    showActionMenu: function($icon) {
        var offset = $icon.offset();
        this.$menu.css({
            top: offset.top+18+'px',
            left: offset.left+5+'px'
        });
        this.$menu.show();
        this.isShowMenu = true;
    },

    hideActionMenu: function() {
        if (this.isShowMenu) {
            this.$menu.hide();
            this.isShowMenu = false;
            this.actionRoleId = null;
        }
    },

    loadRolePermissions: function(roleId, isNewRole) {
        var $permissions = this.$('.xa-rolePermissions');
        if (isNewRole) {
            var $node = $.tmpl(this.permissionListTemplate, {permissions:[]});
            $permissions.empty().append($node);
        } else {
            W.getApi().call({
                app: 'auth',
                api: 'role_permissions/get',
                args: {
                    id: roleId,
                    type: 'view'
                },
                scope: this,
                success: function(data) {
                    xlog(data);
                    var $node = $.tmpl(this.permissionListTemplate, {htmlContent:data});
                    $permissions.empty().append($node);
                },
                error: function(resp) {
                    W.showHint('error', '加载角色权限失败!')
                }
            })
        }
    },

    onClickAddRoleButton: function(event) {
        if(this.$('input:visible').length > 0)
            return
        var $roleList = this.$('.xa-roleList');
        $roleList.prepend('<li data-id="-1"><a href="javascript:void(0);" class="xui-i-role"><input type="text" class="form-control xui-i-input xa-roleNameInput"  placeholder="新角色"/></a></li>');
        $roleList.find('input[type="text"]').focus();
    },

    onClickAddPermissionButton: function(event) {
        var _this = this;
        var roleId = $('.xui-i-activeRole').parent().data('id');
        W.dialog.showDialog('W.dialog.auth.SelectPermissionDialog', {
            roleId: roleId,
            success: function(data) {
                var ids = data;
                W.getApi().call({
                    method: 'post',
                    app: 'auth',
                    api: 'role_permissions/update',
                    args: {
                        role_id: roleId,
                        permission_ids: ids
                    },
                    success: function(data) {
                        _this.loadRolePermissions(roleId);
                    },
                    error: function(resp) {
                        W.showHint('error', '添加权限失败!')
                    }
                })
            }
        })
    },

    onKeyPressInRoleNameInput: function(event) {
        if (event.which === 13) {
            var $input = $(event.currentTarget);
            $input.blur();
        }
    },

    onLeaveRoleNameInput: function(event) {
        var $role = $(event.currentTarget).parents('li');
        var roleId = parseInt($role.data('id'));
        if (roleId === -1) {
            //创建role
            this.createRole($role);
        } else {
            //更新role
            this.updateRole($role, roleId);
        }
    },

    onClickConfigButton: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var $icon = $(event.currentTarget);
        this.showActionMenu($icon);

        this.actionRoleId = $icon.parents('li').data('id');
    },

    onClickRenameRoleButton: function(event) {
        var roleId = this.actionRoleId;
        var $role = this.$('[data-id="'+roleId+'"]');
        var $name = $role.find('.xa-name');
        $name.hide();
        $role.find('.xa-config').hide();
        var name = $.trim($name.text());
        $role.find('.xa-roleNameInput').val('').show().focus().val(name);
        this.hideActionMenu();
    },

    onClickDeleteRoleButton: function(event) {
        if(confirm('确认要删除角色吗？')){
            var roleId = this.actionRoleId;
            var $role = this.$('[data-id="'+roleId+'"]');
            this.hideActionMenu();

            if (roleId) {
                W.getApi().call({
                    method: 'post',
                    app: 'auth',
                    api: 'role/delete',
                    args: {
                        id: roleId
                    },
                    success: function() {
                        $role.remove();
                    }
                })
            }
        }
    },

    onClickRole: function(event) {
        var $role = $(event.currentTarget);
        this.$('.xui-i-activeRole').removeClass('xui-i-activeRole');
        $role.addClass('xui-i-activeRole');

        var roleId = $role.parent('li').data('id');
        this.loadRolePermissions(roleId);
    }
});