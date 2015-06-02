/*
Copyright (c) 2011-2012 Weizoom Inc
*/




/**
 * 图片上传View
 */
W.MultiImageView = Backbone.View.extend({
    el: '',

    events: {
        'click .multi-imageView-imgZone button.close': 'onDeleteImage'
    },
    
    getTemplate: function() {
        $('#multi-image-view').template('multi-image-view-tmpl');
        return 'multi-image-view-tmpl';
    },
    
    toArray: function(url, dot) {
        if(!url) {
            return [];
        }        
        if(url.indexOf(dot) > 0) {
            var urlLength = url.length-1;
            if(url.substr(urlLength, url.length) === dot) {
                url = url.substr(0, urlLength);
            }
            url = url.split(dot);
        }
        else {
            url = [url];
        }
        return url;
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.isMulti = options.isMulti || false;
        this.picUrl = this.toArray(options.picUrl, ';');
        this.maxWidth = options.maxWidth || 280;
        this.width = options.width || this.maxWidth;
        this.height = options.height || this.maxWidth;
        this.scaleInfo = options.scaleInfo || '';
		this.tagId = (+new Date());
        this.queueCount = 0;
        this.templateName = this.getTemplate();
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
            this.$el.parent('div').append("<span class='help-block mt5 cb' >"+this.scaleInfo+"</span>");
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
        var picUrlCount = this.picUrl.length;
        this.queueCount = picUrlCount;
        if (!picUrl.length) {
            picUrl = '/static/img/empty_image.png'
        }
	    this.$el.html($.tmpl(this.templateName, {
		    imgUrls: this.picUrl,
            isMulti: this.isMulti,
            picUrlCount: picUrlCount,
		    width: this.width,
		    height: this.height
	    }));
        
        this.$button = this.$('.multi-imageView-uploadZone');
        this.initImageUploader();
        
        this.bindSortable();
    },
    
    bindSortable: function() {
        this.$(".multi-imageView-imgZone").css({cursor:'move'});
        this.$('.ui-sortable').sortable({
            stop: _.bind(function(options) {
                this.sortImages();
            }, this)
        }).disableSelection();
        this.$('.ui-sortable').sortable('option', 'opacity', 0.6);
        this.$('.ui-sortable').sortable('option', 'placeholder', 'w70 h80 fl mb10 mr10');
    },

    /**
     * 初始化图片上传器
     */
    initImageUploader: function() {
        var _this = this;
        var fileUploader = this.$('[name="multi-imageView-fileUploader"]');
        fileUploader.each(function() {
	        $(this).attr('id', $(this).attr('id')+_this.tagId);
            $(this).unbind();
			$(this).uploadify({
	            swf: '/static/uploadify.swf',
	            multi: _this.isMulti,
	            uploader: '/account/upload_picture/',
	            cancelImg: '/static/img/cancel.png',
	            buttonText: _this.isMulti ? '选择多张图片...' : '选择图片...',
	            fileTypeDesc: '图片文件',
	            fileTypeExts: '*.jpg; *.png; *.gif',
	            method: 'post',
	            formData: {
	                uid: 'sid'+W.uid
	            },
	            removeTimeout: 0.0,
	            onUploadSuccess : function(file, path, response) {
                    if (path && _this.autoShowImage) {
	                    _this.showImage(path);
	                }
                    _this.trigger('change-images', _this.picUrl||[]);
	            },
                onQueueComplete: function() {
                    if(_this.isMulti) {
                        _this.multiQueueComplete();
                    }
                    else {
                        _this.queueComplete();
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
    
    sortImages: function() {
        var $imgContainer = this.$('[name="multi-imageView-imgZone"]');
        var _this = this;
        var src;
        this.picUrl = [];
        $imgContainer.each(function() {
            src = $(this).find('img').attr('src');
            _this.picUrl.push(src);
            _this.trigger('change-images', _this.picUrl||[]);
        });
    },

    /**
     * 显示url指向的image
     * @param url
     */
    showImage: function(url) {
        url = $.trim(url);
        this.picUrl.push(url);
        
        if (!this.picUrl.length) {
            this.cleanImage();
            return;
        }
        var img = this.imgTmpl.render({
            url: url,
            width: this.width,
            height: this.height
        });
        var $allImgContainer = this.$('.multi-imageView-imgZone');
        if(this.queueCount === 0) {
            
        }
        else {
            this.$('.tx_itemContainer').append(this.$('.multi-imageView-imgZone:last').clone());
        }
        
        
        var $imgContainer = this.$('.multi-imageView-imgZone:last').find('.multi-imageView-imgContainer');
        $imgContainer.html(img);
        
        this.queueCount++;
    },
    
    queueComplete: function() {
        this.queueCount = 0;     
        this.$('.multi-imageView-imgZone').show();
        this.$button.hide();
        this.bindSortable();
    },
    
    multiQueueComplete: function() {
        this.$('.multi-imageView-imgZone').show();
        this.bindSortable();
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
        if(event) {
            var $imgContainer = $(event.currentTarget).parents('.multi-imageView-imgZone');
        }
        else {
            var $imgContainer = this.$('.multi-imageView-imgZone:last');
            this.picUrl = [];
        }
        var imgSrc = $imgContainer.find('img').attr('src');
        var $imgContainers = this.$('.multi-imageView-imgZone');
        if($imgContainers.length > 1) {
            $imgContainer.remove();
        }
        else {
            $imgContainer.hide();
            $imgContainer.find('.multi-imageView-imgContainer').html('');
            this.$el.find('.multi-imageView-uploadZone').show();
            this.$imgContainer = null;
            this.queueCount = 0;
        }
        
        //移除this.picUrl中已经删掉的图片的URL
        
        var i, k;
        for(i = 0, k = this.picUrl.length; i < k; i++) {
            if(this.picUrl[i] === imgSrc) {
                this.picUrl.splice(i, 1);
            }
        }
        this.trigger('change-images', this.picUrl||[]);
        if(event){
            event.stopPropagation();
            event.preventDefault();
        }
    }
});