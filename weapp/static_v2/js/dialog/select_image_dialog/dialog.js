/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * select image的对话框
 */
ensureNS('W.workbench');

W.workbench.SelectImageDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#select-image-dialog-tmpl-src').template('select-image-dialog-tmpl');
        return "select-image-dialog-tmpl";
    },

    events: _.extend({
        'click .selectImageDialog_imgBox': 'onClickImage',
        'click .selectImageDialog_submitBtn': 'onClickSelectButton',
        'click .selectImageDialog_deleteBtn': 'onClickDeleteButton'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        xlog("in onInitialize()");

        /*
        this.$el = $(this.el);

        this.template = this.getTemplate();
        $('body').append($.tmpl(this.template, {}));
        this.el = $('#selectImageDialog')[0];
        this.$el = $(this.el);

        this.oneImageTemplate = this.getOneImageTemplate();

        this.initImageUploader();

        this.$imageContainer = this.$('.selectImageDialog_body').eq(0);
        this.successCallback = null;

        this.isImageFetched = false;

        xlog('in initialize...');

        */
    },

    beforeShow: function() {
        xlog("in beforeShow()");
    },

    onShow: function() {
        xlog("in onShow()");
    },

    afterShow: function(options) {
        xlog("in afterShow()");
    },

    getOneImageTemplate: function() {
        $('#select-image-dialog-one-image-tmpl-src').template('select-image-dialog-one-image-tmpl');
        return "select-image-dialog-one-image-tmpl";
    },
});

W.workbench.SelectImageDialog0 = Backbone.View.extend({

    render: function() {},

    show: function(options) {
        this.successCallback = options.success;
        this.$('.activeImg').hide().removeClass('activeImg');
        $('#selectImageDialog').modal('show');

        var imageComponent = options.component;
        var uploadWidth = imageComponent.model.get('uploadWidth');
        if (!uploadWidth) {
            uploadWidth = '任意'
        }
        var uploadHeight = imageComponent.model.get('uploadHeight');
        if (!uploadHeight) {
            uploadHeight = '任意'
        }
        this.$('.selectImageDialog-width').text(uploadWidth + 'px');
        this.$('.selectImageDialog-height').text(uploadHeight + 'px');

        if (!this.isImageFetched) {
            this.isImageFetched = true;
            var task = new W.DelayedTask(function() {
                W.getApi().call({
                    app: 'workbench',
                    api: 'images/get',
                    args: {
                        project_id: W.projectId
                    },
                    scope: this,
                    success: function(data) {
                        var images = data;
                        this.$('.selectImageDialog_body_loading').hide();
                        var _this = this;
                        _.each(images, function(image) {
                            this.onAddImage(image);
                        }, this);
                        this.$('.selectImageDialog_uploadBtn').show();
                    },
                    error: function(resp) {
                        alert('获取图片失败');
                    }
                });
            }, this)
            task.delay(1000);
        }
    },

    /**
     * 初始化图片上传器
     */
    initImageUploader: function() {
        var _this = this;
        var fileUploader = this.$('[name="imageView-fileUploader"]');
        var _path = null;
        fileUploader.each(function() {
            $(this).attr('id', $(this).attr('id') + _this.tagId);
            $(this).uploadify({
                swf: '/static/uploadify.swf',
                multi: false,
                removeCompleted: true,
                uploader: '/account/upload_picture/',
                cancelImg: '/static/img/cancel.png',
                buttonText: '上传图片...',
                fileTypeDesc: '图片文件',
                fileTypeExts: '*.jpg; *.png; *.gif',
                method: 'post',
                formData: {
                    uid: 'sid' + W.uid,
                    project_id: W.projectId,
                    is_need_size: 1
                },
                removeTimeout: 0.0,
                onUploadSuccess: function(file, path, response) {
                    /*
                    _this.trigger('upload-image-success', path);
                    _path = path;
                    */
                    var items = path.split(':');
                    var width = items[0];
                    var height = items[1];
                    var path = items[2];
                    for (var i = 3; i < items.length; i++)
                        path += ':' + items[i];
                    _this.onAddImage(path, width, height);
                },
                onUploadComplete: function() {
                    //在onUploadComplete中隐藏uploadZone，防止queue不清空的bug
                    xlog('upload complete');
                },
                onUploadError: function(file, errorCode, errorMsg, errorString) {
                    xlog(errorCode);
                    xlog(errorMsg);
                    xlog(errorString);
                    alert('上传失败!')
                        //W.getErrorHintView().show('上传失败');
                }
            });
        });
    },

    /**
     *
     */
    onAddImage: function(path, width, height) {
        var $node = $.tmpl(this.oneImageTemplate, {
            url: path,
            width: width,
            height: height
        });
        this.$imageContainer.prepend($node);
    },

    /**
     * onClickImage: 点击图片后的响应函数
     */
    onClickImage: function(event) {
        this.$('.activeImg').hide().removeClass('activeImg');
        var imgBox = $(event.currentTarget);
        imgBox.find('.selectImageDialog_imgBox_cover').addClass('activeImg').show();

        this.$('.selectImageDialog_deleteBtn').show();
    },

    /**
     * onClickSelectButton: 点击图片后的响应函数
     */
    onClickSelectButton: function(event) {
        var activeImage = this.$('.activeImg').parent().find('img');
        var imageUrl = activeImage.attr('src');

        $('#selectImageDialog').modal('hide');
        this.$('.activeImg').hide().removeClass('activeImg');

        xlog('call callback');
        xlog(this.successCallback);
        if (this.successCallback) {
            //调用success callback
            var _this = this;
            var task = new W.DelayedTask(function() {
                _this.successCallback(imageUrl);
                _this.successCallback = null;
            });

            task.delay(500);
        }
    },

    /**
     * onClickDeleteButton: 点击图片后的响应函数
     */
    onClickDeleteButton: function(event) {
        var $activeImageContainer = this.$('.activeImg').parent();
        var imageUrl = $activeImageContainer.find('img').attr('src');

        W.getApi().call({
            app: 'workbench',
            api: 'image/delete',
            scope: this,
            method: 'post',
            args: {
                project_id: W.projectId,
                filename: imageUrl
            },
            success: function(data) {
                this.$('.activeImg').hide().removeClass('activeImg');
                $activeImageContainer.remove();
                this.$('.selectImageDialog_deleteBtn').hide();
            },
            error: function(resp) {
                alert('删除图片失败!')
            }
        });
    }
});
