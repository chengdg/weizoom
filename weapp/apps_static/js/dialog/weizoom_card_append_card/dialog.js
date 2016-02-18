/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 微众卡追加对话框
 */
ensureNS('W.weapp.dialog.AppendWeizoomCardDialog');
W.weapp.dialog.AppendWeizoomCardDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .btn-cancel': 'onClickCancel'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weizoom-card-append-card-dialog-tmpl-src').template('weizoom-card-append-card-dialog-tmpl');
        return "weizoom-card-append-card-dialog-tmpl";
    },

    onInitialize: function(options) {

    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).val('').focus();    
        }, this);
        task.delay(300);
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var cardnum = $.trim(this.$dialog.find('input[name="cardnum"]').val());
        if (cardnum.length == 0) {
            alert('请输入追加数量');
            return false;
        }
        var ex = /^\d+$/;
        if (!ex.test(cardnum)) {
            alert('请输入整数');
            return false;
        }
        data = {
            'rule_id': $('#appendBtn').attr('rule-id'),
            'card_num': cardnum
        }
        return data;
    },
    
    /**
     * onClickCancel: 点击取消按钮的响应函数
     */
    onClickCancel: function(event) {
        this.$dialog.modal('hide');
    }
});