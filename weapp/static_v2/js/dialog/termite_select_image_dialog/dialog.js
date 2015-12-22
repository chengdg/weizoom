/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择图片的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.termite');

W.dialog.termite.SelectImagesDialog = W.dialog.Dialog.extend({
    templates: {
        dialogTmpl: '#termite-select-images-dialog-tmpl-src',
        imageTmpl: '#termite-select-images-dialog-image-tmpl-src'
    },

    events: _.extend({
        'click .xa-delete': 'onClickDeleteButton',
        'click .xa-image': 'onClickImage',
        'click .xa-selectBtn': 'onClickSelectIconType',
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.imageUploader = new W.view.common.ImageView({
            el: this.$('.xa-imageUploader').get(0),
            height: 640,
            width: 640,
            sizeLimit: 1024,
            autoShowHelp: true,
            help: '图片格式：支持jpg, png, gif<br/>图片大小：最大支持1M图片，超过1M不能上传',
            autoShowImage: false,
            isMulti: true,
            isNeedSizeInfo: true
        });
        this.imageUploader.bind('upload-image-success', _.bind(this.onUploadImageSuccess, this));
        this.imageUploader.render();
        this.$imageUploader = this.$('.xa-imageUploader').eq(0);

        //this.imageTemplate = this.getImageTemplate();
    },

    beforeShow: function(options) {        
        var defaultType = 1;
        var iconType = 2;
        var defaultTitles = [{
            name: '用过的图片',
            type: 'usedImages',
        }, {
            name: '新图片',
            type: 'uploadImage'
        }];
        var iconTitles = [{
            name: '小图标',
            type: 'iconImages',
        }, {
            name: '新图片',
            type: 'uploadImage'
        }];

        this.dialogType = parseInt(options.dialogType || defaultType);
        if (this.dialogType == defaultType) {
            this.setTitle(defaultTitles);
        }else if(this.dialogType == iconType){
            this.setTitle(iconTitles);
        }

        this.$('.xa-images').empty();
        this.$('.xa-customImages').empty();
        this.imageUploader.show();

        if (this.dialogType == 1) {
            this.clickNav('usedImages');
        }else if (this.dialogType == 2) {
            this.clickNav('iconImages');
        }
    },

    onShow: function(options) {
        this.selectedImages = new Backbone.Collection();
        this.enableMultiSelection = options.multiSelection;
    },

    afterShow: function(options) {
        if (this.dialogType == 1) {
            this.addUsedImages();
        }else if (this.dialogType == 2) {
            this.addIcons();
        }
    },

    /**
     * addUsedImages: 添加用过的图片
     */
    addUsedImages: function(){
        W.resource.termite2.Images.get({
            data: {},
            scope: this,
            success: function(data) {
                var images = data;
                var buf = [];
                var template = this.getTmpl('imageTmpl');
                for (var i = 0; i < images.length; ++i) {
                    var image = images[i];
                    image.src = image.url;
                    xlog(template({image:image}));
                    buf.push(template({image:image}));
                }

                this.$('.xa-images').empty().append($(buf.join('')));
            },
            error: function(resp) {

            }
        });
    },

    /**
     * addIcons: 添加icon图片
     */
    addIcons: function(){
        var html = [];
        html.push('<div class="xui-imgType ml10">');
        html.push('颜色：');
        html.push('<label style="display:inline-block;" class="xa-selectBtn xui-selectBtn xui-selected" data-show-class="xa-whiteImages">');
        html.push('<input style="margin-top:-3px;" type="radio" data-field="type" name="type" checked="checked" value="0">白色<i class="xui-selectedIcon"></i>');
        html.push('</label>');
        // html.push('<label style="display:inline-block;" class="xa-selectBtn xui-selectBtn" data-show-class="xa-blackImages">');
        // html.push('<input style="margin-top:-3px;" type="radio" data-field="type" name="type" value="1">黑色<i class="xui-selectedIcon" style="display:none;"></i>');
        // html.push('</label>');
        html.push('</div>');
        html.push('<div class="xui-icon-box xa-blackImages xui-hide"></div>');
        html.push('<div class="xui-icon-box xa-whiteImages"></div>');
        this.$('.xa-images').empty().append($(html.join('')))
        W.getApi().call({
            app: 'workbench',
            api: 'nav_icons/get',
            args: {
                project_id: W.projectId
            },
            scope: this,
            success: function(data) {
                var images = data['黑色系'];
                var blackBuf = [];
                var template = this.getTmpl('imageTmpl');
                for (var i = 0; i < images.length; ++i) {
                    var image = {width: 60, height: 60};
                    image.src = images[i];
                    blackBuf.push(template({image:image}));
                }
                this.$('.xa-images').find('.xa-blackImages').append($(blackBuf.join('')));
                
                images = data['白色系'];
                var whiteBuf = [];
                template = this.getTmpl('imageTmpl');
                for (var i = 0; i < images.length; ++i) {
                    var image = {width: 60, height: 60};
                    image.src = images[i];
                    whiteBuf.push(template({image:image}));
                }
                this.$('.xa-images').find('.xa-whiteImages').append($(whiteBuf.join('')));
            },
            error: function(resp) {
                alert('获取图片失败');
            }
        });
    },

    onClickSelectIconType: function(event){
        this.$el.find('.xa-selectBtn').removeClass('xui-selected');
        this.$el.find('.xui-selectedIcon').hide();

        var $el = $(event.currentTarget)
        $el.addClass('xui-selected');
        $el.find('.xui-selectedIcon').show();
        var className = $el.attr('data-show-class');

        this.$el.find('.xui-icon-box').hide();
        this.$el.find('.' + className).show();

        console.log($(event.currentTarget).html(), 6666)
    },

    onChangeNav: function(nav) {
        var $dialog = this.$dialog;
        if (nav === 'uploadImage') {
            $dialog.find('.xa-images').hide();
            $dialog.find('.xa-uploadImageZone').show();
        } else if(nav === 'iconImage') {
            $dialog.find('.xa-uploadImageZone').hide();
            $dialog.find('.xa-images').show();
        } else {
            $dialog.find('.xa-uploadImageZone').hide();
            $dialog.find('.xa-images').show();
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
        var $images = this.$('.xa-customImages').eq(0);
        var id = 0-($images.find('.xa-image').length+1);
        var imageInfo = this.extractImageInfo(path);
        var image = {
            id: id,
            src: imageInfo.path,
            width: imageInfo.width,
            height: imageInfo.height
        }

        var template = this.getTmpl('imageTmpl');
        var $node = $(template({image:image}));
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
            if (!this.enableMultiSelection) {
                this.$dialog.find('.xui-i-selected').removeClass('xui-i-selected');
                this.selectedImages.reset(null);
            }
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

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        var data = {};
        if (this.$('.xa-uploadImageZone').is(':visible')) {
            data.type = "newImage";
        } else {
            data.type = "usedImage";
        }
        data.images = this.selectedImages.toJSON();
        if (data.images.length == 0) {
            W.getErrorHintView().show('请先选择图片！');
            return ""
        } else {
            return data;
        }
    }
});