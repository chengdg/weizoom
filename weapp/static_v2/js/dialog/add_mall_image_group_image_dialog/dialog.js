/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.AddMallImageGroupImageDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-add-mall-image-group-image-dialog-tmpl-src').template('mall-add-mall-image-group-image-dialog-tmpl');
        return "mall-add-mall-image-group-image-dialog-tmpl";
    },

    getImageTemplate: function() {
        $('#mall-add-mall-image-group-image-dialog-image-tmpl-src').template('mall-add-mall-image-group-image-dialog-image-tmpl');
        return "mall-add-mall-image-group-image-dialog-image-tmpl";
    },

    events: _.extend({
        'click .xa-delete': 'onClickDeleteButton'
    }, W.dialog.Dialog.prototype.events),
  
    onInitialize: function(options) {
        this.imageUploader = new W.view.common.ImageView({
            el: this.$('.xa-imageUploader').get(0),
            height: 640,
            width: 640,
            sizeLimit: 500,
            autoShowHelp: true,
            autoShowImage: false,
            isNeedSizeInfo: true
        });
        this.imageUploader.bind('upload-image-success', _.bind(this.onUploadImageSuccess, this));
        this.imageUploader.render();

        this.imageTemplate = this.getImageTemplate();

        // validate
        var $input = this.$dialog.find('.wui-titleInput');
        $input.attr("placeholder", "输入模板名称");
        $input.attr("maxlength", '18');
        $input.attr("data-validate", "require-string");
        $input.after("<label class='errorHint' data-error-hint='请输入18位以内的字符， 且不为空'></label>");
    },

    onShow: function(options) {
        this.groupId = options.groupId || -1;
        this.reset();
        this.$('.xa-images').empty();

      //  this.$('.xa-images').html('<li     class="pr xui-i-image xa-image" data-image-id="add-image"><img src="/static_v2/img/editor/addimg.png" /></li>');
    },

    afterShow: function(options) {
        if (this.groupId !== -1) {
            W.getApi().call({
                app: 'mall',
                api: 'image_group_images/get',
                args: {
                    id: this.groupId
                },
                scope: this,
                success: function(data) {
                    var buf = [];
                    var images = data;
                    _.each(images, function(image) {
                        var $node = $.tmpl(this.imageTemplate, {image:image});
                        buf.push($node);
                    }, this);
                    
                    this.$('.xa-images').empty().append(buf);
                },
                error: function(resp) {
                    
                }
            });
        }
    },

    extractImageInfo: function(path) {
        var items = path.split(':');
        return {
            width: items[0],
            height: items[1],
            path: _.rest(items, 2).join(':')
        }
    },

    addImage: function(path) {
        var $images = this.$('.xa-images').eq(0);
        var id = 0-$images.length;
        var imageInfo = this.extractImageInfo(path);
        var image = {
            id: id,
            src: imageInfo.path,
            width: imageInfo.width,
            height: imageInfo.height,
        }
        var $node = $.tmpl(this.imageTemplate, {image:image});
        $images.append($node);
    },

    onUploadImageSuccess: function(path) {
        this.addImage(path);
    },

    onClickDeleteButton: function(event) {
        var $li = $(event.target).parents('li');
        xlog('delete');
        $li.remove();
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        if(!W.validate($("#mallAddMallImageGroupImageDialog"))){
            return false;
        }

        var images = [];
        this.$('.xa-image').each(function() {
            var $li = $(this);
            var id = $li.data('imageId');
            var src = $li.find('img').attr('src');
            var width = $.trim($li.find('.xa-width').text());
            var height = $.trim($li.find('.xa-height').text());
            images.push({
                id: id,
                path: src,
                width: width,
                height: height
            });
        });
        return {
            "name": this.getDialogTitle(),
            "images": images
        };
    }
});
