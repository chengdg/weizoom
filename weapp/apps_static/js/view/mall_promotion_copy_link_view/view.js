/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 复制链接
 * 
 * author: liupeiyu
 */
ensureNS('W.view.mall');
W.view.mall.PromotionCopyLinkView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#copy-link-view').template('copy-link-view-dialog-tmpl');
        return "copy-link-view-dialog-tmpl";
    },
    
    events:{
     	// 'click .xa-submit': 'submit',
    },

    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
        this.enableEdit = true;
        if (options.hasOwnProperty('enableEdit')) {
            this.enableEdit = options.enableEdit;
        }
    },
    
    validate: function() {
    	
    },
    
    render: function() {
        var context = {enableEdit: this.enableEdit};
    	this.$content.html($.tmpl(this.getTemplate(), context));
	},

    onShow: function(options) {
        var context = {enableEdit: this.enableEdit};
        this.$content.html($.tmpl(this.getTemplate(), context));
        this.position = options.position;
        this.urlLink = options.urlLink;
        
    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0'
    	})

    },
    
    showPrivate: function(options) {
        this.urlLink = options.urlLink;
        var context = {enableEdit: this.enableEdit};
        this.$content.html($.tmpl(this.getTemplate(), context));

        var host = window.location.host;
        $('input[name="link"]').attr('value', 'http://'+host+this.urlLink);

        var _this = this;
        // 定义一个新的复制对象
        var clip = new ZeroClipboard(document.getElementById("xa-copy-btu"), {
          moviePath: "/static_v2/zero_clipboard.swf"
        });

        // 复制内容到剪贴板成功后的操作
        clip.on('complete', function(client, args) {
            W.showHint('success', '复制成功');
            _this.close()
        });
	},
    
});


W.getPromotionCopyLinkView = function(options) {
	var dialog = W.registry['W.view.mall.PromotionCopyLinkView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.PromotionCopyLinkView');
		dialog = new W.view.mall.PromotionCopyLinkView(options);
		W.registry['W.view.mall.PromotionCopyLinkView'] = dialog;
	}
	return dialog;
};