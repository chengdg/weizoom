/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.ShopRuleDialog = W.Dialog.extend({
    SUBMIT_SUCCESS_EVENT: 'submit',

    events: _.extend({
        'click .tx_cancel': 'close',
        'click .tx_submit': 'onSubmit'
    }, W.Dialog.prototype.events),

    getTemplate: function(name) {
        if(name){
            $(name).template('rule-dialog-view-tmpl');
            return 'rule-dialog-view-tmpl';
        }else{
            $('#dialog-view-product-tmpl-src').template('dialog-view-product-tmpl');
            return 'dialog-view-product-tmpl';
        }
    },

    initializeDialog: function() {
        this.render();
    },

    renderDialog: function() {
        var html = $.tmpl(this.getTemplate(), {});
        this.$contentEl.html(html);
    },

    showDialog: function(options) {
        if(options.template){
            var html = $.tmpl(this.getTemplate(options.template), {});
            this.$contentEl.html(html);
        }
    },

    onSubmit: function() {
        this.trigger(this.SUBMIT_SUCCESS_EVENT);
    },

    afterClose: function() {
        this.unbind();
    }
});

/**
 * 获得ShopDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getShopRuleDialog = function(options) {
    var dialog = W.registry['ShopDialog'];
    if (!options) {
        options = {};
    }
    options.width = options.width || 250;
    options.height = options.height || 140;
    if (!dialog) {
        //创建dialog
        xlog('create W.ShopRuleDialog');
        dialog = new W.ShopRuleDialog(options);
        W.registry['ShopRuleDialog'] = dialog;
    }
    return dialog;
};