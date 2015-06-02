/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 微众卡添加账号对话框
 */
ensureNS('W.weapp.dialog.BatchActiveWeizoomCardDialog');
W.weapp.dialog.BatchActiveWeizoomCardDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click li a': 'onChangeMenuItem',
        'click .btn-cancel': 'onClickCancel',
        'keyup input[name="username"]': 'onKeyupUsername'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weizoom-card-batch-active-dialog-tmpl-src').template('weizoom-card-batch-active-dialog-tmpl');
        return "weizoom-card-batch-active-dialog-tmpl";
    },

    onInitialize: function(options) {
    	var checked;
    },
    
    makeOptions: function(options) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            buf.push('<li><a href="javascript:void(0);" account_id="' + option.account_id + '">' + option.nickname + '</a></li>');
        }

        return $(buf.join(''));
    },
    
    getSelectedOptions: function() {
    	checked = []
    	$('input:checkbox:checked').each(function() {
    		if ($(this).attr('name') === 'select-one') {
    			var $tr = $(this).parents('tr');
	    		checked.push($tr.attr('tr-id'));
    		}
        });
    },

    onShow: function(options) {
    	this.getSelectedOptions();
    	this.$dialog.find('.x-count').html(checked.length)
    	
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);        

        W.getApi().call({
            app: 'market_tools/weizoom_card',
            api: 'accounts/get',
            scope: this,
            args: {
                count_per_page: 10000
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
        if (checked.length == 0) {
            alert('请选择待激活微众卡');
            return false;
        }
		
        var $target = this.$dialog.find('input[name="username"]');
        if ($.trim($target.val()).length == 0) {
            alert('请选择目标账号');
            return false;
        }

        data = {
            'card_ids': checked.toString(),
            'target_id': $target.attr('account_id')
        }
        return data;
    },

    /**
     * onChangeMenuItem: 切换账号的响应函数
     */
    onChangeMenuItem: function(event) {
        var $select = $(event.currentTarget);
        var text = $select.html();
        var $input = this.$dialog.find('.x-dropdown-input');
        $input.val(text);
        $input.attr('account_id', $select.attr('account_id'));
    },
    
    /**
     * onClickCancel: 点击取消按钮的响应函数
     */
    onClickCancel: function(event) {
    	this.$dialog.modal('hide');
    },
    
    /**
     * onKeyupUsername: 账号搜索
     */
    onKeyupUsername: function(event) {
    	var $input = $(event.currentTarget);
    	var username = $input.val();
    	W.getApi().call({
            app: 'market_tools/weizoom_card',
            api: 'user_target/filter',
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