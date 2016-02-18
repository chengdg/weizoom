ensureNS('W.view.auth');
W.view.auth.DepartmentList = Backbone.View.extend({

    events:  {
        'click .xa-addDepartment': 'onClickAddDepartmentButton',
        'keypress .xa-departmentNameInput': 'onKeyPressInDepartmentNameInput',
        'blur .xa-departmentNameInput': 'onLeaveDepartmentNameInput',
        'click .xa-config': 'onClickConfigButton',
        'click .xa-department': 'onClickDepartment',
        'click .xa-createAccount': 'onClickCreateAccountButton',
        'click .xa-inactive': 'onClickInactiveAccountLink',
        'click .xa-active': 'onClickActiveAccountLink',
        'click .xa-delete': 'onClickDeleteAccountLink'
    },
    
    initialize: function(options) {
        this.template = _.template(
            '<li data-id="<%= id %>">\
                <a href="javascript:void(0)" class="xa-department xui-i-department xui-i-activeDepartment">\
                    <span class="caret"></span>\
                    <span class="xui-name xa-name"><%= name %></span>\
                    <input type="text" class="form-control xui-i-input xa-departmentNameInput" style="display: none"/>\
                    <span class="glyphicon glyphicon-cog xui-i-config xa-config"></span>\
                </a>\
            </li>'
        );

        this.$menu = $('.xa-departmentActionMenu').eq(0);
        this.isShowMenu = false;
        this.actionDepartmentId = null;

        var _this = this;
        $document = $(document);
        $document.delegate('.xa-renameDepartment', 'click', _.bind(this.onClickRenameDepartmentButton, this));
        $document.delegate('.xa-deleteDepartment', 'click', _.bind(this.onClickDeleteDepartmentButton, this));
        $document.click(function() {
            _this.hideActionMenu();
        });

        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.focusDepartmentId = options.focusDepartmentId || 0;
    },

    render: function() {
        if (this.$('.xa-departmentList li').length == 0) {
            return;
        } else {
            this.$('.xa-departmentList li[data-id="'+this.focusDepartmentId+'"] a').addClass('xui-i-activeDepartment');
            this.loadDepartmentUsers(this.focusDepartmentId);
        }
    },

    createDepartment: function($department) {
        var departmentName = $.trim($department.find('.xa-departmentNameInput').val());
        if (!departmentName) {
            W.showHint('error', '部门名不能为空');
            return;
        }

        W.getApi().call({
            method: 'post',
            app: 'auth',
            api: 'department/create',
            args: {
                name: departmentName
            },
            scope: this,
            success: function(data) {
                var departmentId = data.id;
                this.$('.xa-departmentList li').eq(0).remove();
                var $node = $(this.template(data));
                $node.addClass('.xui-i-activeDepartment');
                this.$('.xui-i-activeDepartment').removeClass('xui-i-activeDepartment');
                this.$('.xa-departmentList').prepend($node);

                this.loadDepartmentUsers(departmentId);
            },
            error: function(resp) {
                if(resp.data.msg)
                    W.showHint('error', resp.data.msg);
                else
                    W.showHint('error', '创建部门失败!');
            }
        })
    },

    updateDepartment: function($department, departmentId) {
        var departmentName = $.trim($department.find('.xa-departmentNameInput').val());
        if (!departmentName) {
            W.showHint('error', '部门名不能为空');
            return;
        }

        W.getApi().call({
            method: 'post',
            app: 'auth',
            api: 'department/update',
            args: {
                id: departmentId,
                name: departmentName
            },
            scope: this,
            success: function(data) {
                $department.find('.xa-departmentNameInput').hide();
                $department.find('.xa-name').text(departmentName).show();
                $department.find('.xa-config').show();                
            },
            error: function(resp) {
                if(resp.data.msg)
                    W.showHint('error', resp.data.msg);
                else
                    W.showHint('error', '更新部门失败!');
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
            this.actionDepartmentId = null;
        }
    },

    loadDepartmentUsers: function(departmentId) {
        this.table.addFrozenArgs({
            id: departmentId
        });
        this.table.reload();
    },

    onClickAddDepartmentButton: function(event) {
        if($('.xa-departmentList input:visible').length > 0){
            return
        }
        var $departmentList = this.$('.xa-departmentList');
        $departmentList.prepend('<li data-id="-1"><a href="javascript:void(0);" class="xui-i-department"><input type="text" class="form-control xui-i-input xa-departmentNameInput" placeholder="新部门"/></a></li>');
        $departmentList.find('input[type="text"]').focus();
    },

    onKeyPressInDepartmentNameInput: function(event) {
        if (event.which === 13) {
            var $input = $(event.currentTarget);
            $input.blur();
        }
    },

    onLeaveDepartmentNameInput: function(event) {
        var $department = $(event.currentTarget).parents('li');
        var departmentId = parseInt($department.data('id'));
        if (departmentId === -1) {
            //创建Department
            xlog('create by blur');
            this.createDepartment($department);
        } else {
            //更新Department
            this.updateDepartment($department, departmentId);
        }
    },

    onClickConfigButton: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var $icon = $(event.currentTarget);
        this.showActionMenu($icon);

        this.actionDepartmentId = $icon.parents('li').data('id');
    },

    onClickRenameDepartmentButton: function(event) {
        var departmentId = this.actionDepartmentId;
        var $department = this.$('[data-id="'+departmentId+'"]');
        var $name = $department.find('.xa-name');
        $name.hide();
        $department.find('.xa-config').hide();
        var name = $.trim($name.text());
        $department.find('.xa-departmentNameInput').val('').show().focus().val(name);
        this.hideActionMenu();
    },

    onClickDeleteDepartmentButton: function(event) {
        var departmentId = this.actionDepartmentId;
        var $department = this.$('[data-id="'+departmentId+'"]');
        this.hideActionMenu();

        if (this.$('.xa-departmentUsers .xa-user').length > 0) {
            W.showHint('error', '请将部门内所有员工删除后再删除部门');
            return;
        }

        if (departmentId) {
            W.getApi().call({
                method: 'post',
                app: 'auth',
                api: 'department/delete',
                args: {
                    id: departmentId
                },
                success: function() {
                    $department.remove();
                }
            })
        }
    },

    onClickDepartment: function(event) {
        var $department = $(event.currentTarget);
        this.$('.xui-i-activeDepartment').removeClass('xui-i-activeDepartment');
        $department.addClass('xui-i-activeDepartment');

        var departmentId = $department.parent('li').data('id');
        this.loadDepartmentUsers(departmentId);
    },

    onClickCreateAccountButton: function(event) {
        if (this.$('.xa-department').length == 0) {
            W.showHint('error', '请先创建部门再新建员工');
            return;
        }
        window.location.href = '/auth/account/create/';
    },

    updateAccountStatus: function(accountId, status) {
        W.getApi().call({
            method: 'post',
            app: 'auth',
            api: 'account_status/update',
            args: {
                id: accountId,
                status: status
            },
            scope: this,
            success: function(data) {
                this.table.reload();
            },
            error: function(resp) {

            }
        })
    },

    onClickInactiveAccountLink: function(event) {
        var $link = $(event.currentTarget)
        var id = $link.parents('tr').data('id');
        var _this = this;
        W.requireConfirm({
            $el: $link,
            show_icon: false,
            width:360,
            position:'top',
            isTitle: false,
            msg: '确认停用该员工？',
            confirm: function() {
                _this.updateAccountStatus(id, 'inactive');
            }
        });
    },

    onClickActiveAccountLink: function(event) {
        var id = $(event.currentTarget).parents('tr').data('id');
        this.updateAccountStatus(id, 'active');
    },

    onClickDeleteAccountLink: function(event) {
        var $link = $(event.currentTarget)
        var id = $link.parents('tr').data('id');
        var _this = this;
        W.requireConfirm({
            $el: $link,
            show_icon: false,
            width:360,
            position:'top',
            isTitle: false,
            msg: '确认删除该员工？',
            confirm: function() {
                _this.updateAccountStatus(id, 'delete');
            }
        });
    }
});