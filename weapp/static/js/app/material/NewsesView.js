/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 多条newses的view
 * @constructor
 */
W.material.NewsesView = Backbone.View.extend({
    events:{
        'click #embededPhone-deleteBtn': 'onDeleteNews',
	    'click #embededPhone-editBtn': 'onUpdateNews',
	    'mouseover #small-phone': 'overEditShow',
	    'mouseout #small-phone': 'outEditShow'
    },

    getOneMessageTemplate: function() {
        var name = 'one-news-tmpl';
        $('#one-news-tmpl-src').template(name);
        return name;
    },

    compileNewsTemplate: function() {
        $('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
    },

    initialize: function(options) {
        this.$el = $(this.el);
	    this.$messageContainerLeft = $('<div class="leftList fl"></div>');
	    this.$messageContainerRight = $('<div class="rightList fr"></div>');
	    this.$el.html('');
	    this.$el.append(this.$messageContainerLeft);
	    this.$el.append(this.$messageContainerRight);
	    this.$el.css({'overflow':'hidden','height':'auto'});

        this.oneMessageTemplate = this.getOneMessageTemplate();
        this.compileNewsTemplate();

        this.showInfoType = options.showInfoType || '-1';
	    this.enableEdit = options.enableEdit || false;

        this.createPaginationView();

        //创建collection对象，绑定其add事件
        this.newses = new W.material.Newses();
        this.newses.bind('add', this.onAddMessage, this);
        this.fetchData();
    },

    reload: function(){
        this.fetchData();
    },

	overEditShow: function(event){
		var $el = $(event.currentTarget);
		$el.find('div.edit-div input').css({
			display:''
		});
	},

	outEditShow: function(event) {
		var $el = $(event.currentTarget);
		$el.find('div.edit-div input').css({
			display:'none'
		});
	},

    /**
    * 将一条消息从页面上移除
    */
    removeOneMessage: function(li) {
        li.remove();

    },

    /**
    * 接收到一条message时的响应函数
    */
    onAddMessage: function(message) {
	    this.newsItemCount++;
        var messageJSON = message.toJSON();
        var node = $.tmpl(this.oneMessageTemplate, messageJSON);
        var newses = messageJSON.newses;
        if (newses.length == 1) {
            var newsNode = $.tmpl('single-news-tmpl', {
                news: newses[0],
	            enableEdit: this.enableEdit,
	            enableUpdateMaterial: true,
	            enableDeleteMaterial: true
            }).removeClass('mt10');
        } else {
            var mainNews = newses[0];
            var subNewses = newses.slice(1);
            var newsNode = $.tmpl('multi-newses-tmpl', {
                mainNews: mainNews,
                subNewses: subNewses,
	            enableEdit: this.enableEdit,
	            enableUpdateMaterial: true,
	            enableDeleteMaterial: true
            }).removeClass('mt10');
        }
        var phoneNode = $('<div id="small-phone" class="small-phone-nobackground" can-checked="true" data-id="'+message.get('id')+'"></div>')
        phoneNode.append(newsNode);

	    if(this.newsItemCount%2 === 0) {
		    this.$messageContainerRight.append(phoneNode);
	    }else {
		    this.$messageContainerLeft.append(phoneNode);
	    }
	    //隐藏编辑和删除按钮
	    $('div.edit-div input').hide();
    },

    /**
    * 创建分页部分view
    */
    createPaginationView: function() {
        this.paginationView = new W.PaginationView({
            el: $('.wx_paginationContent'),
            isHasDetailedPage: true,
            isHasJumpPage: true
        });
        this.paginationView.bind('goto', this.gotoPage, this);
    },

    gotoPage: function(page){
        this.newses.setPage(page);
        this.fetchData();
    },

    /**
    * 从server端加载数据
    */
    fetchData: function() {
        var _this = this;
        this.clear();
	    this.newsItemCount = 0;
        this.newses.fetch({
            reset: false,
            success: function(sessions, response) {
	            if(sessions.length <= 0 ){
		            _this.$el.html('没有图文素材信息！');
	            }
                _this.paginationView.setPageInfo(_this.newses.getPageData(response));
                _this.paginationView.show();
            },
            error: function(sessions, response) {
                //var msg = response.errMsg || '由于网络原因，加载失败，请重新刷新页面!';
                //alert(msg)
                if (response.errMsg) {
                    alert(response.errMsg);
                }
            }
        });
    },

    clear: function(){
        this.newses.reset([])
        this.$el.find('li').remove();
    },

    /**
    * 点击"删除"链接的响应函数
    */
    onDeleteNews: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $el = $(event.target);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
	        var $li = $el.parents('#small-phone');
	        var newsId = $li.attr('data-id');

	        W.getApi().call({
	            app: 'material',
	            api: 'news/delete',
	            args: {
	                id: newsId
	            },
	            success: function(data) {
	                //改变日历中，已有信息
	                this.trigger('finish-delete-news');
	                deleteCommentView.hide();
	            },
	            error: function(resp) {

	            },
	            scope: this
	        });
        }, this);

        deleteCommentView.show({
            $action: $el,
            info: '确定删除吗?'
        });
    },

	/**
	 * 点击"修改"链接的响应函数
	 */
	onUpdateNews: function(event) {
		event.stopPropagation();
		event.preventDefault();

		var $div = $(event.target).parents('#small-phone');
		var newsId = $div.attr('data-id');
		this.trigger('finish-update-news', newsId);
	}
})