/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.AddProductModelPropertyValueDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-add-product-model-property-value-dialog-tmpl-src').template('mall-add-product-model-property-value-dialog-tmpl');
        return "mall-add-product-model-property-value-dialog-tmpl";
    },

    events: _.extend({
        
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.template = this.getTemplate();
        W.createWidgets(this.$dialog);
    },

    beforeShow: function(options) {
        
        // imageView.cleanImage();

        // imageView.showImage("/standard_static/test_resource_img/icon_color/icon_1.png");
        this.$('input[name="name"]').val('');
    },

    onShow: function(options) {
        var $input = this.$('input[name="name"]');
        this.propertyId = options.propertyId || -1;
        this.modelValue = options.modelValue;
        this.picUrl = options.picUrl;
        // console.log(this.picUrl,"=========",this.modelValue);
        var imageView = this.$('input[data-ui-role="image-selector"]').data('view');
        imageView.showImage(this.picUrl);
        $input.val(this.modelValue);
        $input.siblings('.errorHint').hide();
        $input.parent().removeClass('has-error');
    },

    afterShow: function(options) {
        this.$dialog.find('input[type="text"]').eq(0).focus();
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        if (!W.validate(this.$dialog)) {
            return null;
        }

        var name = $.trim(this.$('input[name="name"]').val());
        var picUrl = this.$('input[name="pic_url"]').val();
        return {
            "name": name,
            "picUrl": picUrl
        };
    }
});