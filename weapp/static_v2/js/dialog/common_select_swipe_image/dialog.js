/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.common');

W.dialog.common.SelectSwipeImageDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#common-select-swipe-image-dialog-tmpl-src').template('common-select-swipe-image-dialog-tmpl');
        return "common-select-swipe-image-dialog-tmpl";
    },

    onInitialize: function(options) {
        var $imageInput = this.$('[name="pic_url"]');
        var imageWidth = options.imageWidth;
        var imageHeight = options.imageHeight;
        var $imageView = this.$dialog.find('#commonSelectSwipeImagesDialog-imageView');
        var isMulti = options.isMulti || false;
        this.maxCount = options.imgCount || -1;
        this.imageView = new W.view.common.ImageView({
            el: $imageView.get(),
            height: imageHeight,
            width: imageWidth,
            autoShowHelp: true,
            isMulti: isMulti
        });
        this.imageView.bind('upload-image-success', function(path) {
            var value = $imageInput.val();
            if (value.length > 0) {
                value += ','+ path;
            }else{
                value = path;
            }
            $imageInput.val(value);
        });
        this.imageView.bind('delete-image', function(path) {
            if(isMulti){
                $imageInput.val(path);
            }else{
                $imageInput.val('');
            }          

        });
        this.imageView.render();
    },

    onShow: function(options) {
        this.maxCount = options.imgCount || -1;
    },

    afterShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        var url = this.$('[name="pic_url"]').val();
        if (this.maxCount > 0 && url.split(',').length > this.maxCount) {
             W.getErrorHintView().show('系统只允许添加'+this.maxCount+'张图片');
             return '';
        }
        if (!W.validate($('#commonSelectSwipeImageDialog'))) {
            return '';
        }

        this.imageView.cleanImage();

        return url;
    }
});