/*
Copyright (c) 2011-2012 Weizoom Inc
*/


$('#image-view-tmpl-src').template('image-view-tmpl');

/**
 * 图片上传View
 */
W.ImageView = Backbone.View.extend({
    el: '',

    events: {
        'click .imageView-imgZone button.close': 'onDeleteImage'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.picUrl = options.picUrl || null;
        this.maxWidth = options.maxWidth || 280;
        this.width = options.width || this.maxWidth;
        this.height = options.height || this.maxWidth;
		this.tagId = (+new Date());
        this.autoShowHelp = options.autoShowHelp || false;//是否显示建议信息

        this.computeWidthAndHeight();

        if (options.hasOwnProperty('autoShowImage')) {
            this.autoShowImage = options.autoShowImage;
        } else {
            this.autoShowImage = true;
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

        this.$el.parent('div').find('.help-block').remove();
        if(this.autoShowHelp){
            this.$el.parent('div').append("<span class='help-block mt15' >建议图片尺寸为 "+this.width+"*"+this.height+"像素</span>");
        }

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

        this.imgTmpl = new W.Template('<img src="${url}" width="${width}px" height="${height}px" style="width: ${width}px; height: ${height}px" />');

    },

    render: function() {
        var picUrl = this.picUrl;
        if (!picUrl) {
            picUrl = '/static/img/empty_image.png'
        }
	    this.$el.html($.tmpl('image-view-tmpl', {
		    picUrl: this.picUrl,
		    width: this.width,
		    height: this.height
	    }));

        this.initImageUploader();
    },

    /**
     * 初始化图片上传器
     */
    initImageUploader: function() {
        var _this = this;
        var fileUploader = this.$('[name="imageView-fileUploader"]');
        var _path = null;
        fileUploader.each(function() {
	        $(this).attr('id', $(this).attr('id')+_this.tagId);
			$(this).uploadify({
	            swf: '/static/uploadify.swf',
	            multi: false,
	            removeCompleted: true,
	            uploader: '/account/upload_picture/',
	            cancelImg: '/static/img/cancel.png',
	            buttonText: '选择图片...',
	            fileTypeDesc: '图片文件',
	            fileTypeExts: '*.jpg; *.png; *.gif',
	            method: 'post',
	            formData: {
	                uid: 'sid'+W.uid
	            },
	            removeTimeout: 0.0,
	            onUploadSuccess : function(file, path, response) {
	                _this.trigger('upload-image-success', path);
	                _path = path;
	            },
	            onUploadComplete: function() {
	                //在onUploadComplete中隐藏uploadZone，防止queue不清空的bug
	                if (_path && _this.autoShowImage) {
	                    _this.showImage(_path);
	                    _path = null;
	                }
	            },
	            onUploadError: function(file, errorCode, errorMsg, errorString) {
	                xlog(errorCode);
	                xlog(errorMsg);
	                xlog(errorString);
	                W.getErrorHintView().show('图片数据损坏，无法在Android平台显示，请处理图片，再次上传');

	            }
	        });
        });
    },

    /**
     * 显示url指向的image
     * @param url
     */
    showImage: function(url) {
        this.picUrl = $.trim(url);
        if (!this.picUrl) {
            this.cleanImage();
            return;
        }

        //var img = '<img src="' + this.picUrl + '" width="' + this.width + 'px" />';
        var img = this.imgTmpl.render({
            url: this.picUrl,
            width: this.width,
            height: this.height
        })
        var imgZone = this.$('[name="imageView-imgZone"]');
        if (imgZone.is(':visible')) {
            this.$('.imageView-imgContainer').html(img);
        } else {
            this.$('.imageView-uploadZone').hide();
            this.$('.imageView-imgContainer').html(img);
            this.$('.imageView-imgZone').show();
        }
    },

    /**
     * 清除image
     */
    cleanImage: function() {
        this.onDeleteImage();
    },

    /**
     * 获得图片地址
     * @return {*}
     */
    getImageUrl: function() {
        return this.picUrl;
    },

    /**
     * 响应删除按钮的点击事件
     */
    onDeleteImage: function(event) {
        this.picUrl = '';
        this.$el.find('.imageView-imgZone').hide();
	    this.$el.find('.imageView-uploadZone').show()
	    this.$el.find('.imageView-imgContainer').html('');
        this.trigger('delete-image');

        if(event){
            event.stopPropagation();
            event.preventDefault();
        }
    }
});