/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择限定区域对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.EditProductLimitedAreaTemplateDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-edit-product-limited-area-template-tmpl-src').template('mall-edit-product-limited-area-template-tmpl');
        return "mall-edit-product-limited-area-template-tmpl";
    },
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.templateId = options.templateId;
        this.templateName = options.templateName;
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.templateId = options.templateId;
    },

    onShow: function(options) {
        
    },

    afterShow: function(options) {
         this.table.reload({id: this.templateId})
    },

    onGetData: function(event) {
    }
});