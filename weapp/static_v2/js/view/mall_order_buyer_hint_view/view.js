/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单列表页面买家信息悬浮框
 * 
 * author: duhao
 */
ensureNS('W.view.mall');
W.view.mall.BuyerHintView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#buyerHint-view').template('buyerHint-view-dialog-tmpl');
        return "buyerHint-view-dialog-tmpl";
    },

    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},
    
    showPrivate: function(options) {
        this.delivery_time = options.delivery_time;
        this.addr = options.addr;
        this.tel = options.tel;
        this.bill_type = options.bill_type;
        this.bill = options.bill;
        this.$content.html($.tmpl(this.getTemplate(),{
            delivery_time:this.delivery_time,
            addr:this.addr,
            tel:this.tel,
            bill_type:this.bill_type,
            bill:this.bill
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


W.getBuyerHintView = function(options) {
	var dialog = W.registry['W.view.mall.BuyerHintView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.BuyerHintView');
		dialog = new W.view.mall.BuyerHintView(options);
		W.registry['W.view.mall.BuyerHintView'] = dialog;
	}
	return dialog;
};