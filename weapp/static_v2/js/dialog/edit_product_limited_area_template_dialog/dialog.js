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
        'click .xa-edit': 'onClickEdit'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.templateId = options.templateId;
        this.templateName = options.templateName;
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.templateId = options.templateId;
        this.table.reload({template_id: this.templateId})
        console.log('~~~~~~~~~~',this.templateId)
    },
    onClickEdit: function(options){
        window.location.href="/mall2/product_limit_zone_template/?template_id=" + this.templateId;
    },
    onShow: function(options) {
        this.templateName = options.templateName;
        $('.xui-limited-area-template-dialog').find('.modal-title').text(this.templateName)
    },

    afterShow: function(options) {
    },

    onGetData: function(event) {
    }
});