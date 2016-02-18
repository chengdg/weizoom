/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * csv文件上传View
 */
ensureNS('W.view.common');
W.view.common.CVSView = Backbone.View.extend({
    el: '',

    events: {
        'click .videoView-fileZone .xui-close': 'onDeleteFile'
    },

    getTemplate: function() {
        $('#cvs-view-tmpl-src').template('cvs-view-tmpl');
        return 'cvs-view-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.fileUrl = options.fileUrl || null;
        this.maxWidth = options.maxWidth || 280;
        this.width = options.width || this.maxWidth;
        this.height = options.height || this.maxWidth;
        this.tagId = (+new Date());
        this.autoShowHelp = options.autoShowHelp || false;//是否显示建议信息
        this.template = this.getTemplate();

        this.computeWidthAndHeight();

        if (options.hasOwnProperty('autoShowVideo')) {
            this.autoShowVideo = options.autoShowVideo;
        } else {
            this.autoShowVideo = true;
        }
    },

    /**
     * 计算宽和高
     */
    computeWidthAndHeight: function(options){
        if(options){
            this.width = options.width || this.maxWidth;
            this.height = options.height || this.maxWidth;
        }

        // this.$el.parent('div').find('.help-block').remove();
        if(this.autoShowHelp){
            // this.$el.parent('div').append("<span class='help-block mt15' >仅支持CSV文件</span>");
        }
        this.$el.parent('div').find('.errorHint').html('');
        var mark,old = 0;
        if(this.width > this.maxWidth){
            old = this.width;
            this.width = this.maxWidth;
            this.height = parseInt((this.width * this.height) / old )
        }
        if(this.height > this.maxWidth){
            old = this.height;
            this.height = this.maxWidth;
            this.width = parseInt((this.width * this.height)/ old )
        }

//     this.imgTmpl = new W.Template('<img src="${url}" width="${width}px" height="${height}px" style="width: ${width}px; height: ${height}px" />');
         this.imgTmpl = _.template('上传成功');

    },

    render: function() {
        var fileUrl = this.fileUrl;
        if (!fileUrl) {
            fileUrl = '/static/img/empty_image.png'
        }
        this.$el.html($.tmpl(this.template, {
            fileUrl: this.fileUrl,
            width: this.width,
            height: this.height
        }));

        this.initVideoUploader();
    },

    /**
     * 初始化图片上传器
     */
    initVideoUploader: function() {
        var _this = this;
        var fileUploader = this.$('[name="cvsView-fileUploader"]');
        var _path = null;
        fileUploader.each(function() {
            $(this).attr('id', $(this).attr('id')+_this.tagId);
            $(this).uploadify({
                swf: '/static/uploadify.swf',
                multi: false,
                removeCompleted: true,
                uploader: '/account/upload_video/',
                buttonText: '选择文件',
                fileTypeDesc: 'CSV文件',
                fileTypeExts: '*.csv',
                method: 'post',
                fileSizeLimit: '1GB',
                formData: {
                    uid: 'sid'+W.uid
                },
                removeTimeout: 0.0,
                onUploadSuccess : function(file, path, response) {
                    _this.trigger('upload-file-success', path);
                    _path = path;
                },
                onUploadComplete: function() {
                    //在onUploadComplete中隐藏uploadZone，防止queue不清空的bug
                    if (_path && _this.autoShowVideo) {
                        _this.showImage(_path);
                        _path = null;
                    }
                },
                onUploadError: function(file, errorCode, errorMsg, errorString) {
                    xlog(errorCode);
                    xlog(errorMsg);
                    xlog(errorString);
                    W.getErrorHintView().show('视频数据损坏，无法显示，请处理后，再次上传');

                }
            });
        });
    },

    /**
     * 显示url指向的image
     * @param url
     */
    showImage: function(url) {
        this.fileUrl = $.trim(url);
        if (!this.fileUrl) {
            this.cleanImage();
            return;
        }

        //var img = '<img src="' + this.fileUrl + '" width="' + this.width + 'px" />';
        var img = this.imgTmpl({
            url: this.fileUrl,
            width: this.width,
            height: this.height
        })
        var fileZone = this.$('[name="videoView-fileZone"]');
        fileZone.width(this.width+'px');
        if (fileZone.is(':visible')) {
            this.$('.videoView-fileContainer').html(img);
        } else {
            this.$('.videoView-uploadZone').hide();
            this.$('.videoView-fileContainer').html(img);
            this.$('.videoView-fileZone').removeClass('hide').show();
        }
    },

    /**
     * 清除image
     */
    cleanImage: function() {
        this.onDeleteFile();
    },

    /**
     * 获得图片地址
     * @return {*}
     */
    getImageUrl: function() {
        return this.fileUrl;
    },

    /**
     * 响应删除按钮的点击事件
     */
    onDeleteFile: function(event) {
        this.fileUrl = '';
        this.$el.find('.videoView-fileZone').hide();
        this.$el.find('.videoView-uploadZone').show()
        this.$el.find('.videoView-fileContainer').html('');
        this.trigger('delete-file');

        this.$el.parent('div').find('.errorHint').html('');
        if(event){
            event.stopPropagation();
            event.preventDefault();
        }
    }
});
