/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 跑马灯列表
 * @class
 */
W.rice.ProductSwipePhotoListView = Backbone.View.extend({
    el: '',

    events: {
        'click #add-swipe-photo-btn': 'onAddButton',
        'click .close': 'onDeleteButton'
    },

    getTemplate: function(){
        $('#shop-swipe-photo-tmpl-src').template('shop-swipe-photo-tmpl');
        return 'shop-swipe-photo-tmpl';
    },

    getOneSwipePhotoTemplate: function() {
        var name = 'one-swipe-photo-tmpl';
        $('#shop-one-swipe-photo-tmpl-src').template(name);
        return name;
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$container = null;
        this.productId = options.productId;
	    this.shopName = options.shopName;
	    this.siteDomain = options.siteDomain;
        this.languageType = options.languageType;
        this.template = this.getTemplate();
        this.oneSwipePhotoTemplate = this.getOneSwipePhotoTemplate();

        this.optionsDialog = {
            title: '添加轮播图片',
            state: 'SwipePhoto',
	        shopName: this.shopName,
	        siteDomain: this.siteDomain,
            imageWidthAndHeight: {width: 800, height: 600}
        }

        //创建轮播图片编辑dialog
        this.editEditSiteDialog = W.getTourEditSiteDialog(this.optionsDialog);
        var _this = this.productId;
        //创建collection对象，绑定其add事件
        this.swipePhoto = new W.rice.ProductSwipePhotos();
        this.swipePhoto.productId = _this;
        this.swipePhoto.languageType = this.languageType;
        this.swipePhoto.bind('add', this.onAdd, this);
        this.swipePhoto.fetch();
    },

    render: function() {
        this.$el.html($.tmpl(this.template));
        this.$container = this.$('#swipePhotos');
        return this;
    },

    refresh: function(){
        xlog('refresh SwipePhotoList');
        this.swipePhoto.fetch();
    },

    /**
     * 接收到一条message时的响应函数
     */
    onAdd: function(message) {
        this.$container.append($.tmpl(this.oneSwipePhotoTemplate, message.toJSON()));
    },

    /**
     * 将一条消息从页面上移除
     */
    removeOne: function(li) {
        li.remove();

    },

    submitDialog: function(data){
        W.getLoadingView().show();
        var _this = this;
       // _this.onAdd({'url':data.url});
        var size = this.$el.find('div[name="oneSwipePhoto"]').length;
        if(size<6){
            $("#swipePhotos").append("<div id='oneSwipePhoto-div' class='fl imgBox pt0 mr15 mb10 mt5' style='width: 80px;'' data-id='"+(+new Date())+"' name='oneSwipePhoto'><button class='close' type='button'>×</button><img width='80px' style='width: 80px; height: 80px;' src='"+data.url+"'></div>");
        }
        _this.trigger('finish-submit-message');
        _this.refresh();
        _this.editEditSiteDialog.close();
        W.getLoadingView().hide();
    },

    onAddButton: function(event){
        event.stopPropagation();
        event.preventDefault();

        var size = this.$el.find('div[name="oneSwipePhoto"]').length;
        xlog(size);
        if(size >=  6 ){
            alert('系统只允许添加6个轮播图片');
            return false;
        }else{
            this.editEditSiteDialog.show(this.optionsDialog);
            this.editEditSiteDialog.unbind("submit");
            this.editEditSiteDialog.bind('submit', function(data) {
                this.submitDialog(data);
            },this);
        }

    },

    /**
     * 点击"删除"链接的响应函数
     */
    onDeleteButton: function(event) {
        var $el = $(event.target);
        var $div = $el.parents('#oneSwipePhoto-div');
        var swipePhotoId = $div.attr('data-id');
        $('div[data-id='+swipePhotoId+']').remove();
        event.stopPropagation();
        event.preventDefault();
    }
});