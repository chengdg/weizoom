/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.SelectMallImagesDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-select-mall-images-dialog-tmpl-src').template('mall-select-mall-images-dialog-tmpl');
        return "mall-select-mall-images-dialog-tmpl";
    },

    getImageTemplate: function() {
        $('#mall-select-mall-images-dialog-image-tmpl-src').template('mall-select-mall-images-dialog-image-tmpl');
        return "mall-select-mall-images-dialog-image-tmpl";
    },

    events: _.extend({
        'click .xa-delete': 'onClickDeleteButton',
        'change .xa-imageGroupSelector': 'onChangeImageGroup',
        'click .xa-image': 'onClickImage'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.imageUploader = new W.view.common.ImageView({
            el: this.$('.xa-imageUploader').get(0),
            height: 640,
            width: 640,
            sizeLimit: 500,
            autoShowHelp: true,
            autoShowImage: false,
            isMulti: true,
            isNeedSizeInfo: true
        });
        this.imageUploader.bind('upload-image-success', _.bind(this.onUploadImageSuccess, this));
        this.imageUploader.render();
        this.$imageUploader = this.$('.xa-imageUploader').eq(0);

        this.imageTemplate = this.getImageTemplate();
    },

    beforeShow: function(options) {
        this.$('.xa-imageGroupSelector').empty();
        this.$('.xa-images').empty();
        this.$('.xa-customImages').empty();
        this.imageUploader.show();
    },

    onShow: function(options) {
        this.groupId = options.groupId || -1;
        this.selectedImages = new Backbone.Collection();
    },

    afterShow: function(options) {
        W.getApi().call({
            app: 'mall',
            api: 'image_groups/get',
            args: {},
            scope: this,
            success: function(data) {
                var buf = ['<option value="0" selected="selected">手动上传</option>'];
                _.each(data, function(imageGroup) {
                    buf.push('<option value="'+imageGroup.id+'">'+imageGroup.name+'</option>')
                });
                this.$('.xa-imageGroupSelector').empty().append($(buf.join('')));
            },
            error: function(resp) {
                
            }
        });
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
        var $images = this.$('.xa-customImages').eq(0);
        var id = 0-($images.find('.xa-image').length+1);
        var imageInfo = this.extractImageInfo(path);
        var image = {
            id: id,
            src: imageInfo.path,
            width: imageInfo.width,
            height: imageInfo.height
        }
        var $node = $.tmpl(this.imageTemplate, {image:image});
        $images.append($node);

        return $node;
    },

    onUploadImageSuccess: function(path) {
        var $image = this.addImage(path);

        //选中上传的图片
        event = {
            currentTarget: $image.get(0)
        }
        this.onClickImage(event);
    },

    onClickImage: function(event) {
        var $li = $(event.currentTarget);
        var id = parseInt($li.data('imageId'));
        if ($li.hasClass('xui-i-selected')) {
            $li.removeClass('xui-i-selected');
            var image = this.selectedImages.get(id);
            this.selectedImages.remove(image);
        } else {
        $li.addClass('xui-i-selected');
            var $img = $li.find('img').eq(0);
            var url = $img.attr('src');
            var width = $li.find('.xa-width').text();
            var height = $li.find('.xa-height').text();
            this.selectedImages.push({
                id: id,
                url: url,
                width: width,
                height: height
            });
            xlog(this.selectedImages);
        }
    },

    onChangeImageGroup: function(event) {
        var groupId = $(event.target).val();
        if (groupId === '0') {
            this.imageUploader.show();
            this.$('.xa-images').hide();
            this.$('.xa-customImages').show();
        } else {
            this.imageUploader.hide();
            this.$('.xa-customImages').hide();

            W.getApi().call({
                app: 'mall',
                api: 'image_group_images/get',
                args: {id: groupId},
                scope: this,
                success: function(data) {
                    var buf = [];
                    var images = data;
                    _.each(images, function(image) {
                        var $node = $.tmpl(this.imageTemplate, {image:image});
                        buf.push($node);
                    }, this);
                    
                    this.$('.xa-images').empty().append(buf).show();
                },
                error: function(resp) {

                }
            })
        }
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        return this.selectedImages.toJSON();
    }
});