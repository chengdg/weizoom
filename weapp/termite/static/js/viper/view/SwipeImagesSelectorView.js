/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.common.SelectSwipeImageDialog = W.Dialog.extend({
    SUBMIT_SUCCESS_EVENT: 'submit',

    events: _.extend({
        'click .tx_cancel': 'close',
        'click .tx_submit': 'onSubmit'
    }, W.Dialog.prototype.events),

    getTemplate: function() {
        $('#swipe-images-selector-dialog-src').template('swipe-images-selector-dialog-tmpl');
        return 'swipe-images-selector-dialog-tmpl';
    },

    initializeDialog: function(options) {
        this.render();

        //初始化ImageView
        this.imageView = new W.ImageView({
            el: this.$('#swipeImagesSelector-dialog-imageView'),
            autoShowHelp: true,
            width: options.imageWidth,
            height: options.imageHeight
        });
        this.imageView.bind('upload-image-success', function(path) {
            this.$('#pic_url').val(path);
        }, this);
        this.imageView.bind('delete-image', function(path) {
            this.$('#pic_url').val('');
        }, this);
        this.imageView.render();
    },

    renderDialog: function() {
        var html = $.tmpl(this.getTemplate());
        this.$contentEl.html(html);
    },

    showDialog: function() {
        
    },

    onSubmit: function() {
        if (!W.validate(this.$contentEl, true)) {
            return;
        }

        var url = $.trim(this.$('#pic_url').val());
        this.trigger(this.SUBMIT_SUCCESS_EVENT, {url: url});
    },

    afterClose: function() {
        this.imageView.cleanImage();
        this.$('#pic_url').val('');
    }
});

/**
 * 获得SelectSwipeImageDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.common.getSelectSwipeImageDialog = function(options) {
    var dialog = W.registry['common.SelectSwipeImageDialog'];
    if (!options) {
        options = {};
    }
    options.width = options.width || 500;
    options.height = options.height || 360;
    options.imageWidth = options.imageWidth || 800;
    options.imageHeight = options.imageHeight || 600;

    if (!dialog) {
        //创建dialog
        xlog('create common.SelectSwipeImageDialog');
        dialog = new W.common.SelectSwipeImageDialog(options);
        W.registry['common.SelectSwipeImageDialog'] = dialog;
    }
    return dialog;
};


/**
 * 跑马灯列表
 * @class
 * 
 * event:
 *    add-image: 添加一张图片后激发
 *    delete-image: 删除一张图片后激发
 *    update-order: 调整顺序后激发
 * data-attribute:
 *    data-target-input: 指定关联的input控件，比如'#textInput'
 *    data-count: 指定图片数量
 *    data-image-width：图片选择对户框中图片的width
 *    data-image-height：图片选择对户框中图片的height
 *    data-images-json: 图片数据
 */
W.common.SwipeImagesSelectorView = Backbone.View.extend({
    el: '',

    events: {
        'click #add-swipe-photo-btn': 'onClickAddButton',
        'click .close': 'onClickDeleteButton'
    },

    getTemplate: function(){
        $('#swipe-images-selector-tmpl-src').template('swipe-images-selector-tmpl');
        return 'swipe-images-selector-tmpl';
    },

    getOneSwipeImageTemplate: function() {
        var name = 'swipe-images-selector-one-image-tmpl';
        $('#swipe-images-selector-one-image-tmpl-src').template(name);
        return name;
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$container = null;
        this.template = this.getTemplate();
        this.oneSwipeImageTemplate = this.getOneSwipeImageTemplate();

        this.count = options.count || 6;
        this.$targetInput = options.targetInput;
        this.images = options.images || [];

        options.selector = options.selector || {}

        //创建添加图片的dialog
        this.dialogOptions = {
            title: '添加轮播图片',
            imageWidth: options.selector.width || 800,
            imageHeight:  options.selector.height || 600
        }
        this.dialog = W.common.getSelectSwipeImageDialog(this.dialogOptions);
        this.dialog.bind('submit', function(data) {
            var image = data;
            image.id = -1;
            this.onFinishSelectImage(image);
        }, this);
    },

    render: function() {
        var $node = $.tmpl(this.template, {
            count: this.count
        });

        var $container = $node.find('#swipePhotos');
        this.$container = $container;
        if (this.images) {
            var oneImageTemplate = this.oneSwipeImageTemplate;
            _.each(this.images, function(image) {
                $container.append($.tmpl(oneImageTemplate, image));
            });
        }
        this.$el.empty().append($node);

        this.$(".swipeImagesSelector-oneImage").css({cursor:'move'});
        this.$container.sortable({
            //axis: 'x',
            //helper: this.storHelper,
            stop: _.bind(function(options) {
                this.updateTargetInput();
                this.trigger('update-order', this.getImages());
            }, this)
        }).disableSelection();

        this.updateTargetInput();

        if (W.Broadcaster) {
            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('create-swipe-image-selecotr-widget', this);    
            }, this)
            task.delay(1000);
        }
        return this;
    },

    /**
     * getImages: 获得选中的图片
     */
    getImages: function() {
        return $.parseJSON(this.$targetInput.val());
    },

    /**
     * 更新target input
     */
    updateTargetInput: function() {
        if (!this.$targetInput) {
            return;
        }

        var urls = [];
        this.$('.swipeImagesSelector-oneImage').each(function() {
            var $image = $(this).find('img').eq(0);
            urls.push($image.attr('src'));
        });

        if (this.$targetInput) {
            this.$targetInput.val(JSON.stringify(urls));
        }
    },

    /**
     * SelectImage dialog通过“确定”关闭后的响应函数
     */
    onFinishSelectImage: function(image){
        var size = this.$('div[name="oneSwipePhoto"]').length;
        if(size < this.options.count){
            var oneImageTemplate = this.oneSwipeImageTemplate;
            this.$container.append($.tmpl(this.oneSwipeImageTemplate, image));
        }
        
        this.dialog.close();
        this.updateTargetInput();
        this.trigger('add-image', this.getImages());
    },

    /**
     * onClickAddButton: 点击“添加”按钮的响应函数
     */
    onClickAddButton: function(event){
        event.stopPropagation();
        event.preventDefault();

        var size = this.$el.find('div[name="oneSwipePhoto"]').length;
        if(size >=  this.count ){
            alert('系统只允许添加'+this.count+'张轮播图片');
            return false;
        } else {
            this.dialog.show();
        }
    },

    /**
     * onClickDeleteButton: 点击图片右上角“删除”按钮的响应函数
     */
    onClickDeleteButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $el = $(event.currentTarget);
        $el.parents('.swipeImagesSelector-oneImage').remove();

        this.updateTargetInput();
        this.trigger('delete-image', this.getImages());
    }
});