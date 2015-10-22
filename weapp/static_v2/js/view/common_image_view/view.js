/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 图片上传View
 */
ensureNS('W.view.common');
W.view.common.ImageView = Backbone.View.extend({
    el: '',

    events: {
        'click .imageView-imgZone button.close': 'onDeleteImage'
    },

    getTemplate: function() {
        $('#image-view-tmpl-src').template('image-view-tmpl');
        return 'image-view-tmpl';
    },

    getMultiTemplate: function() {
        $('#multi-image-view-tmpl-src').template('multi-image-view-tmpl');
        return 'multi-image-view-tmpl';
    },
    getOneImageTemplate: function() {
        $('#one-image-view-tmpl-src').template('one-image-view-tmpl');
        return 'one-image-view-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.template = this.getTemplate();
        this.picUrl = options.picUrl || null;
        this.maxWidth = options.maxWidth || 280;
        this.width = options.width || this.maxWidth;
        this.height = options.height || this.maxWidth;
        this.sizeLimit = options.sizeLimit || null;
        this.format = options.format || 'all';
		this.tagId = (+new Date());
        this.autoShowHelp = options.autoShowHelp || false;//是否显示建议信息
        this.isNeedSizeInfo = options.isNeedSizeInfo || false; //是否需要server端返回size信息
        this.help = options.help || null;

        this.showDelete = options.showDelete || false;//是否可以删除

        this.computeWidthAndHeight();

        if (options.hasOwnProperty('autoShowImage')) {
            this.autoShowImage = options.autoShowImage;
        } else {
            this.autoShowImage = true;
        }

        this.fileUploaders = null;

        this.isMulti = options.isMulti || false;
        if (this.isMulti) {
            this.template = this.getMultiTemplate();
            this.oneImageTemplate = this.getOneImageTemplate();
        }
        this.buttonText = options.buttonText || '上传图片';
    },

    setSizeLimit: function(sizeLimit) {
        this.sizeLimit = sizeLimit;
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
            if (this.help) {
                var helpHtml = "<span class='help-block mt15' >"+this.help+"</span>";
                this.$el.parent('div').append($(helpHtml));
            } else {
                var items = ["<span class='help-block mt15' >上传图片建议尺寸 ", this.width, "*", this.height];
                if (this.sizeLimit) {
                    items.push(", 大小不超过" + this.sizeLimit + "KB");
                }
                items.push('</span>');
                this.$el.parent('div').append(items.join(''));
            }
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

        this.imgTmpl = _.template('<img src="<%= url %>" width="<%= width %>px" height="<%= height %>px" style="width: <%= width %>px; height: <%= height %>px" />');

    },

    render: function() {
        var picUrl = this.picUrl;
        if (!picUrl) {
            picUrl = '/static/img/empty_image.png'
        }
        this.$el.html($.tmpl(this.template, {
		    picUrl: this.picUrl,
		    width: this.width,
		    height: this.height
	    }));
        this.initImageUploader();
        if (this.showDelete){
            this.$el.find('.close').css('display','block');
        }else{
            this.$el.find('#imageView-uploadZone').removeClass('xui-hide');
        }

        this.$el.find('.uploadify-button-text').text(this.buttonText);

    },

    /**
     * 初始化图片上传器
     */
    initImageUploader: function() {
        var _this = this;
        this.fileUploaders = this.$('[name="imageView-fileUploader"]');
        var _path = null;
        // 上传的数量
        this._size = 0;
        var formData = {
            uid: 'sid'+W.uid
        }
        if (this.isNeedSizeInfo) {
            formData['is_need_size'] = true;
        }
        this.fileUploaders.each(function() {
            _id = $(this).attr('id')+_this.tagId;
	        $(this).attr('id', $(this).attr('id')+_this.tagId);
            var options = {
                swf: '/static/uploadify.swf',
                multi: _this.isMulti,
                removeCompleted: true,
                uploader: '/account/upload_picture/',
                cancelImg: '/static/img/cancel.png',
                buttonText: '上传图片',
                fileTypeDesc: '图片文件',
                fileTypeExts: '*.jpg; *.png; *.gif',
                method: 'post',
                formData: formData,
                removeTimeout: 0.0,
                onUploadSuccess : function(file, path, response) {
                    _this.trigger('upload-image-success', path);
                    _path = path;
                    console.log('path', path)
                },
                onUploadComplete: function() {
                    //在onUploadComplete中隐藏uploadZone，防止queue不清空的bug
                    if (_path && _this.autoShowImage) {
                        console.log('onUploadComplete')
                        if (_this.isMulti) {
                            _this.showOneImage(_path);
                        }else{
                            _this.showImage(_path);
                        }
                        _path = null;
                    }
                },
                onUploadError: function(file, errorCode, errorMsg, errorString) {
                    xlog(errorCode);
                    xlog(errorMsg);
                    xlog(errorString);
                    W.getErrorHintView().show('图片数据损坏，无法在Android平台显示，请处理图片，再次上传');
                },
                onUploadStart: function(file) {
                    if (!_this.sizeLimit) {
                        return;
                    }
                    
                    if (file.size >= _this.sizeLimit*1024) {
                        _this.fileUploaders.each(function() {
                            $(this).uploadify('cancel', '*', true);
                        });
                        var errorMsg = '图片'+file.name+'大小超过限制('+_this.sizeLimit+'KB)，请重新选择。';
                        alert(errorMsg);
                    }
                },
                onSelectError: function(file, errorCode, errorMsg) {
                    if (errorCode === SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT) {
                        this.queueData.errorMsg = '图片'+file.name+'大小超过限制('+_this.sizeLimit+'KB)，请重新选择。';
                    }
                },
                onSelect: function(file) {
                    _this._size += 1;
                }
            }
            if (_this.sizeLimit) {
                options['fileSizeLimit'] = _this.sizeLimit + 'KB';
            }
            if (_this.format === 'all') {
                options['fileTypeExts'] = '*.jpg; *.png; *.gif';
            } else {
                options['fileTypeExts'] = '*.' + _this.format;
            }
			$(this).uploadify(options);
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
        var img = this.imgTmpl({
            url: this.picUrl,
            width: this.width,
            height: this.height
        });
        var imgZone = this.$('[name="imageView-imgZone"]');
        imgZone.width(this.width+'px');
        if (imgZone.is(':visible')) {
            this.$('.imageView-imgContainer').html(img);
        } else {
            this.$('.imageView-uploadZone').hide();
            this.$('.imageView-imgContainer').html(img);
            this.$('.imageView-imgZone').show();
        }
    },
    /**
     * 显示url指向的image
     * @param url
     */
    showOneImage: function(url) {
        this.picUrl = $.trim(url);
        if (!this.picUrl) {
            this.cleanImage();
            return;
        }

        var imgZone = this.$('[name="imageView-imgZone"]');
        imgZone.width(this.width+'px');
        // console.log(imgZone,'imgZone', imgZone.is(':visible'))
        this.onAdd();
        var total = this.$el.find('.imageView-imgContainer').length;
        if (this._size == total) {
            this.$('.imageView-uploadZone').hide();
        }
    },

    onAdd: function() {
        this.$el.find('.multi-image-zome').prepend($.tmpl(this.getOneImageTemplate(), {
            picUrl: this.picUrl,
            width: this.width,
            height: this.height
        }));
    },

    hide: function() {
        this.$el.hide();
        this.$el.parent('div').find('.help-block').hide()
    },

    show: function() {
        this.$el.show();
        this.$el.parent('div').find('.help-block').show()
    },

    /**
     * setViewData: 支持view.setViewData(value)的调用方式
     */
    setViewData: function(url) {
        this.showImage(url);
    },

    /**
     * 清除image
     */
    cleanImage: function() {
        this.onDeleteImage(null);
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
        // this.$el.find('.imageView-imgZone').hide();
	    // this.$el.find('.imageView-uploadZone').show();
	    // this.$el.find('.imageView-imgContainer').html('');
        this._size -= 1;
        if(event){
            var $el = $(event.currentTarget).parent('.imageView-imgZone');
        }else{
            var $el = this.$el.find('.imageView-imgZone');
        }
        $el.hide();

        if (this.isMulti){
            //多张图片
            $el.remove();
            var $imgZones = this.$el.find('.imageView-imgZone');
            if ($imgZones.length == 0) {
                this.$el.find('.imageView-uploadZone').show();
                this._size = 0;
            }   
            //统计图片url
            var urlList = [];
            $imgZones.each(function(){
                urlList.push($(this).attr('data-img-url'));
            })
            this.picUrl = urlList.join(',');
        }else{
            // 单张图片
            this.picUrl = '';
            $el.find('.imageView-imgContainer').html('');
            this.$el.find('.imageView-uploadZone').show();
        }
        this.trigger('delete-image', this.picUrl);

        if(event){
            event.stopPropagation();
            event.preventDefault();
        }
    }
});


W.registerUIRole('input[data-ui-role="image-selector"]', function() {
    var $imageInput = $(this);
    var width = parseInt($imageInput.attr('data-width'));
    var height = parseInt($imageInput.attr('data-height'));
    var sizeLimit = parseInt($imageInput.attr('data-size-limit'));
    var $imageView = $imageInput.siblings('div[data-ui-role="image-selector-view"]').eq(0);
        
    var autoShowHelpStr =  $imageView.attr("auto-show-help");
    var autoShowHelp = true;
    if (autoShowHelpStr == "false") {
        autoShowHelp = false;
    }

    var showDeleteStr =  $imageInput.attr("data-show-delete");
    var showDelete = true;
    if (showDeleteStr == "false") {
        showDelete = false;
    }
    var format =  $imageInput.attr("data-format");
    var buttonText = $imageInput.attr("data-button-text");
    var url = $imageInput.val();
    var view = new W.view.common.ImageView({
        el: $imageView.get(),
        picUrl: url,
        height: height,
        width: width,
        sizeLimit: sizeLimit,
        autoShowHelp: autoShowHelp,
        showDelete: showDelete,
        format: format,
        buttonText: buttonText
    });
    view.bind('upload-image-success', function(path) {
        $imageInput.val(path);
    });
    view.bind('delete-image', function() {
        $imageInput.val('');
    });
    view.render();

    $imageInput.data('view', view);
});