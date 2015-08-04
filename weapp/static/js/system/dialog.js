/*
Copyright (c) 2011-2013 Weizoom Inc
*/
ensureNS('W.dialog');

//<name, dialog>缓存
W.dialog.NAME2DIALOG = {};


W.dialog.Dialog = Backbone.View.extend({
    events: {
        'click .btn-success': 'onClickSubmitButton'
    },

    getTemplate: function() {
        throw "Please implement dialog's \"getTemplate\" function in your own dialog"; 
    },

    onInitialize: function(options) {
    },

    beforeShow: function(options) {
    },

    onShow: function(options) {

    },

    afterShow: function(options) {
    },

    onGetData: function() {

    },

    onGetDataAsync: function() {

    },

    __getFormData: function() {
        var s = 'http://a.com/?' + this.$dialog.find('form').serialize();
        return parseUrl(s)['query'];
    },

    initialize: function(options) {
        options = options || {};
        this.$el = $(this.el);

        this.template = this.getTemplate();
        var $node = $.tmpl(this.template, options);

        $('body').append($node);
        this.el = $node.get(0);
        this.$el = $(this.el);

        this.successCallback = null;
        this.$dialog = this.$el;

        this.$el.on('shown', this.afterShow);
        this.onInitialize(options);
    },

    render: function() {
    },

    show: function(options) {
        this.successCallback = options.success;
        
        this.beforeShow(options);
        
        this.$dialog.modal('show');

        this.onShow(options);
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var data = this.onGetData(event);

        if (data) {
            this.$dialog.modal('hide');
            console.log(this.successCallback);
            if (this.successCallback) {
                //调用success callback
                var _this = this;
                var task = new W.DelayedTask(function() {
                    _this.successCallback(data);
                    _this.successCallback = null;
                });
              
                task.delay(100);
            }
        }
    }
});

/**
 * showDialog: 显示dialogName指定的dialog
 */
W.dialog.showDialog = function(dialogName, options) {
    var dialog = W.dialog.NAME2DIALOG[dialogName];
    if (dialog) {
        dialog.show(options);
        return;
    }

    //没有dialog，创建之
    xlog('create new dialog: ' + dialogName);
    var obj = window;
    var items = dialogName.split('.');
    var itemCount = items.length;
    for (var i = 0; i < itemCount; ++i) {
        var item = items[i];
        if (obj.hasOwnProperty(item)) {
            obj = obj[item];
        } else {
            obj = [];
            break;
        }
    }

    xlog(obj);
    if (obj !== null) {
        var dialog = new obj(options);
        W.dialog.NAME2DIALOG[dialogName] = dialog;
        dialog.show(options);
    }
}


/**
 * initDialog: 初始化dialogName指定的dialog
 */
W.dialog.initDialog = function(dialogName, options) {
	var dialog = W.dialog.NAME2DIALOG[dialogName];
	if (dialog) {
		return;
	}

	//没有dialog，创建之
	xlog('create new dialog: ' + dialogName);
	var obj = window;
    var items = dialogName.split('.');
    var itemCount = items.length;
    for (var i = 0; i < itemCount; ++i) {
        var item = items[i];
        if (obj.hasOwnProperty(item)) {
            obj = obj[item];
        } else {
            obj = [];
            break;
        }
    }

    xlog(obj);
    if (obj !== null) {
    	var dialog = new obj(options);
    	W.dialog.NAME2DIALOG[dialogName] = dialog;
    }
}