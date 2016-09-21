/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单列表页面, 申请退款提示框
 * 
 * author: liugenbin
 */
ensureNS('W.view.mall');
W.view.mall.RefundingHintView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#refundingHint-view').template('refundingHint-view-dialog-tmpl');
        return "refundingHint-view-dialog-tmpl";
    },

    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},
    
    showPrivate: function(options) {
        this.cash = options.cash*1;
        this.weizoomCardMoney = options.card*1;
        this.couponMoney = options.coupon*1;
        this.integral = options.integral*1;
        this.total = parseFloat(this.cash) + parseFloat(this.weizoomCardMoney) + parseFloat(this.integral) + parseFloat(this.couponMoney);

        var numbers = [this.cash, this.weizoomCardMoney, this.couponMoney, this.integral];
        var noZero = _.filter(numbers, function(number){
            return number != 0;
        });
        var isShowTotal = 0;
        if (noZero.length > 1) {
            isShowTotal = 1;
        }

        this.$content.html($.tmpl(this.getTemplate(),{
            cash: this.cash,
            weizoomCardMoney:this.weizoomCardMoney,
            couponMoney:this.couponMoney,
            integral:this.integral,
            isShowTotal: isShowTotal,
            total: this.total
        }));
	},

    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.isArrow = options.isArrow;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    }

});


W.getRefundingHintView = function(options) {
	var dialog = W.registry['W.view.mall.RefundingHintView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.RefundingHintView');
		dialog = new W.view.mall.RefundingHintView(options);
		W.registry['W.view.mall.RefundingHintView'] = dialog;
	}
	return dialog;
};