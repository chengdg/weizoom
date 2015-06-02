/*
Copyright (c) 2011-2012 Weizoom Inc
*/
__STRIPPER_TAG__
__STRIPPER_TAG__
/**
 * 对话框
 */
ensureNS('W.dialog.app.{{dialog_name}}');
W.dialog.app.{{dialog_name}}.{{dialog_js_name}} = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),
__STRIPPER_TAG__
    getTemplate: function() {
        $('#app-{{dialog_name}}-dialog-tmpl-src').template('app-{{dialog_name}}-dialog-tmpl');
        return "app-{{dialog_name}}-dialog-tmpl";
    },
__STRIPPER_TAG__
    onInitialize: function(options) {
    },
__STRIPPER_TAG__
    onShow: function(options) {
        var _this = this;
        _.delay(function() {
            _this.$dialog.find('input[type="text"]').focus();
        }, 300);
    },
__STRIPPER_TAG__
    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        return this.__getFormData();
    }
});