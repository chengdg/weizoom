/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 发货的对话框
 * 
 * author: liupeiyu
 */
ensureNS('W.view.mall');
W.view.mall.MallOrderCostomerMessageView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#costomerMessage-view').template('costomerMessage-view-dialog-tmpl');
        return "costomerMessage-view-dialog-tmpl";
    },

    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},
    
    showPrivate: function(options) {
        this.messageContent = options.messageContent;
        this.$content.html($.tmpl(this.getTemplate(),{messageContent:this.messageContent}));
	},
    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.isArrow = options.isArrow;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    }

});


W.getMallOrderCostomerMessageView = function(options) {
	var dialog = W.registry['W.view.mall.MallOrderCostomerMessageView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.MallOrderCostomerMessageView');
		dialog = new W.view.mall.MallOrderCostomerMessageView(options);
		W.registry['W.view.mall.MallOrderCostomerMessageView'] = dialog;
	}
	return dialog;
};