/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 多条masssend message的view
 * @constructor
 */
W.MassMessagesView = Backbone.View.extend({
    el: '',

    events:{
        'click a.time_mass_message_delete': 'onDeleteMessage'
    },

    getTemplate: function(){
        $('#timed-weixin-mass-messages-tmpl-src').template('timed-weixin-mass-messages-tmpl');
        return 'timed-weixin-mass-messages-tmpl';
    },

    getOneMessageTemplate: function() {
        var name = 'one-mass-message-tmpl';
        $('#timed-weixin-one-mass-message-tmpl-src').template(name);
        return name;
    },

    compileNewsTemplate: function() {
        $('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$messageContainer = null;

        this.template = this.getTemplate();
        this.oneMessageTemplate = this.getOneMessageTemplate();
        this.compileNewsTemplate();

        this.showInfoType = options.showInfoType || '-1';

        this.createPaginationView();

        //创建collection对象，绑定其add事件
        this.massMessages = new W.MassMessages();
        this.massMessages.bind('add', this.onAddMessage, this);
        this.fetchData();
    },

    render: function() {
        this.$el.html($.tmpl(this.template));
        this.$messageContainer = this.$('ul');
        return this;
    },

    reload: function(){
        this.fetchData();
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
        if(this.showInfoType == '-1' ){
            var messageJSON = message.toJSON();
            var node = $.tmpl(this.oneMessageTemplate, messageJSON);
            var type = message.get('type');
            if ('图文消息' == type) {
                var newses = messageJSON.newses;
                if (newses.length == 1) {
                    var newsNode = $.tmpl('single-news-tmpl', {
                        news: newses[0]
                    }).removeClass('mt10');
                } else {
                    var mainNews = newses[0];
                    var subNewses = newses.slice(1);
                    var newsNode = $.tmpl('multi-newses-tmpl', {
                        mainNews: mainNews,
                        subNewses: subNewses
                    }).removeClass('mt10');
                }
                var phoneNode = $('<div id="small-phone" class="small-phone-nobackground" />')
                phoneNode.append(newsNode);
                node.find('div.oneTimeline_context').html(phoneNode);
            }
            this.$messageContainer.append(node);
        } else if (message.get('status') == this.showInfoType ){
            this.$messageContainer.append($.tmpl(this.oneMessageTemplate, message.toJSON()));
        }
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
        this.massMessages.setPage(page);
        this.fetchData();
    },

    /**
    * 从server端加载数据
    */
    fetchData: function() {
        var _this = this;
        this.clear();
        this.massMessages.fetch({
            reset: false,
            success: function(sessions, response) {
                _this.paginationView.setPageInfo(_this.massMessages.getPageData(response));
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
        this.massMessages.reset([])
        this.$el.find('li').remove();
    },

    /**
    * 点击"删除"链接的响应函数
    */
    onDeleteMessage: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $el = $(event.target);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
        var $li = $el.parents('li');
        var messageId = $li.attr('data-id');

        W.getApi().call({
            app: 'masssend',
            api: 'message/delete',
            args: {
                id: messageId
            },
            success: function(data) {
                this.removeOneMessage($li);
                //改变日历中，已有信息
                this.trigger('finish-delete-message');
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
    }
})