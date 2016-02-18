/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 已发送消息概况悬浮框
 * 
 * author: duhao
 */
ensureNS('W.view.message');
W.view.message.MassSentMessageView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#massSentMessage-view').template('massSentMessage-view-dialog-tmpl');
        return "massSentMessage-view-dialog-tmpl";
    },

    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},
    
    showPrivate: function(options) {
        this.total = options.total;
        this.succ = options.succ;
        this.fail = options.fail;
        this.$content.html($.tmpl(this.getTemplate(),{
            total:this.total,
            succ:this.succ,
            fail:this.fail
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


W.getMassSentMessageView = function(options) {
	var dialog = W.registry['W.view.message.MassSentMessageView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.message.MassSentMessageView');
		dialog = new W.view.message.MassSentMessageView(options);
		W.registry['W.view.message.MassSentMessageView'] = dialog;
	}
	return dialog;
};