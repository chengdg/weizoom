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
        this.cash = options.cash;
        this.card = options.card;
        this.integral = options.integral;
        this.coupon = options.coupon;
        this.total = parseFloat(this.cash) + parseFloat(this.card) + parseFloat(this.integral) + parseFloat(this.coupon);

        this.$content.html($.tmpl(this.getTemplate(),{
            cash: this.cash,
            card:this.card,
            integral:this.integral,
            conpon:this.conpon,
            total: this.total.toFixed(2)
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