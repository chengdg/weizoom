/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 微众卡添加账号对话框
 */
ensureNS('W.weapp.dialog.AddWeizoomCardUserDialog');
W.weapp.dialog.AddWeizoomCardUserDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click li a': 'onChangeMenuItem',
        'keyup input[name="username"]': 'onKeyupUsername'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weizoom-card-add-user-dialog-tmpl-src').template('weizoom-card-add-user-dialog-tmpl');
        return "weizoom-card-add-user-dialog-tmpl";
    },

    onInitialize: function(options) {
    },
    
    makeOptions: function(options) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            buf.push('<li><a href="javascript:void(0);">' + option.name + '</a></li>');
        }

        return $(buf.join(''));
    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);        

        W.getApi().call({
            app: 'market_tools/weizoom_card/account',
            api: 'user_all/get',
            scope: this,
            args: {
                count: 10000
            },
            success: function(data) {
                var $node = this.makeOptions(data.items);
                this.$dialog.find('.x-dropdown-menu').empty().append($node);
            },
            error: function(resp) {
                alert('获取账号失败');
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var nickname = $.trim(this.$dialog.find('input[name="nickname"]').val());
        if (nickname.length == 0) {
            alert('请输入名称');
            return false;
        }

        var username = $.trim(this.$dialog.find('input[name="username"]').val());
        if (username.length == 0) {
            alert('请输入账号');
            return false;
        }

        data = {
            'nickname': nickname,
            'username': username
        }
        return data;
    },

    /**
     * onChangeMenuItem: 切换账号的响应函数
     */
    onChangeMenuItem: function(event) {
        var $select = $(event.currentTarget);
        var text = $select.html();
        this.$dialog.find('.x-dropdown-input').val(text);
    },
    
    /**
     * onKeyupUsername: 账号搜索
     */
    onKeyupUsername: function(event) {
    	var $input = $(event.currentTarget);
    	var username = $input.val();
    	W.getApi().call({
            app: 'market_tools/weizoom_card',
            api: 'user_all/filter',
            scope: this,
            args: {
                username: username
            },
            success: function(data) {
                var $node = this.makeOptions(data.items);
                this.$dialog.find('.x-dropdown-menu').empty().append($node);
                this.$dialog.find('.btn-group').addClass('open');
            },
            error: function(resp) {
                alert('获取账号失败');
            }
        });
    }
    
});