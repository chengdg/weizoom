/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * AdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table
 */
ensureNS('W.view.common');
W.view.common.SwipeImageSelector = Backbone.View.extend({
	el: '',

    events: {
        'click #swipeImageList-addBtn': 'onClickAddImageButton',
        'click .x-removeImage': 'onClickDeleteImageButton'
    },

    getTemplate: function(){
        $('#common-swipe-image-list-tmpl-src').template('common-swipe-image-list-tmpl');
        return 'common-swipe-image-list-tmpl';
    },

    getOneImageTemplate: function() {
        var name = 'common-swipe-image-list-one-image-tmpl';
        $('#common-swipe-image-list-one-image-tmpl-src').template(name);
        return name;
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$container = null;

        this.imageWidth = options.imageWidth || 100;
        this.imageHeight = options.imageHeight || 100;
        this.maxCount = options.maxCount || 6;
        this.images = options.images || [];
        this.isMulti = options.isMulti || false;

        this.template = this.getTemplate();
        this.oneImageTemplate = this.getOneImageTemplate();
    },

    render: function() {
        var $node = $.tmpl(this.template, {'maxCount': this.maxCount});
        var $imageContainer = $node.find('#swipeImageList-images');
        for (var i = 0; i < this.images.length; ++i) {
            $imageContainer.append($.tmpl(this.oneImageTemplate, {
                url: this.images[i].url
            }));
        }

        this.$el.empty().append($node);
        this.$container = this.$('#swipeImageList-images');
        return this;
    },

    /**
     * onClickAddImageButton: 点击“添加”按钮的响应函数
     */
    onClickAddImageButton: function(event){
        var _this = this;
	    var size = _this.$el.find('.x-oneSwipePhoto').length;
	    if(size >=  _this.maxCount ){
		    W.getErrorHintView().show('系统只允许添加'+_this.maxCount+'张图片');
	    } else {
		    W.dialog.showDialog('W.dialog.common.SelectSwipeImageDialog', {
			    imageWidth: this.imageWidth,
			    imageHeight: this.imageHeight,
                isMulti: _this.isMulti,
                imgCount: _this.maxCount - size,
			    success: function(data) {
                    data = data.split(',');
                    for (var i = 0; i < data.length; i++) {
                        _this.$container.append($.tmpl(_this.oneImageTemplate, {
                            url: data[i]
                        }));
                    };

				    _this.trigger('update-swipe-image', _this.getImages());
			    }
		    });
	    }
    },

    /**
     * 点击"删除"链接的响应函数
     */
    onClickDeleteImageButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $el = $(event.target);
        var $div = $el.parents('div.x-oneSwipePhoto');
        $div.remove();

        this.trigger('update-swipe-image', this.getImages());
    },

    /**
     * getImages: 获得image集合
     */
    getImages: function() {
        var images = []
        this.$('.x-oneSwipePhoto').each(function() {
            var $div = $(this);
            images.push({
                url: $div.find('img').attr('src')
            });
        });

        return images;
    }
});


W.registerUIRole('[data-ui-role="swipe-image-selector"]', function() {
    var $imageInput = $(this);
    var imageWidth = parseInt($imageInput.attr('data-image-width'));
    var imageHeight = parseInt($imageInput.attr('data-image-height'));
    var maxCount = parseInt($imageInput.attr('data-max-count'));
    var isMulti = $imageInput.attr('data-is-multi');
    var images = $imageInput.val();
    if (images) {
        var images = $.parseJSON(images);
    }
    var $imageView = $imageInput.siblings('div[data-ui-role="swipe-image-selector-view"]').eq(0);
    var view = new W.view.common.SwipeImageSelector({
        el: $imageView.get(),
        maxCount: maxCount,
        images: images,
        imageHeight: imageHeight,
        imageWidth: imageWidth,
        autoShowHelp: true,
        isMulti: isMulti
    });
    view.bind('update-swipe-image', function(images) {
        $imageInput.val(JSON.stringify(images));
    });
    view.render();
});
