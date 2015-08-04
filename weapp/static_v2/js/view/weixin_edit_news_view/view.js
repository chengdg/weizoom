/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑面板
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.EditNewsPanel = Backbone.View.extend({
    el: '',

    events: {
        'click #submit-btn': 'onSubmitNews',
        'change input[name="change_action"]': 'changeEditAction',
    },

    getTemplate: function() {
        $('#weixin-edit-news-view-tmpl-src').template('weixin-edit-news-view-tmpl');
        return 'weixin-edit-news-view-tmpl';
    },

    changeEditAction: function() {
        var actionType = $('input[name=change_action]:radio:checked').val();
        if (actionType == '1') {
            //进入微站，需要隐藏“封面图片显示在正文中”的checkbox
            $('#showCoverPicOption').hide();
        } else {
            //显示图文，需要显示“封面图片显示在正文中”的checkbox
            $('#showCoverPicOption').show();
        }
    },

    initialize: function(options) {

        this.$el = $(this.el);
        this.mode = options.mode || 'multi-news';
        this.scheduledDate = options.scheduledDate;
        this.materialId = options.materialId || '-1';

        this.initCount = options.initCount || 1; //model为multi-news时有效
        this.patterns = options.patterns || '';
        this.showPattern = options.showPattern || false;

        this.template = this.getTemplate();

        this.$el.html($.tmpl(this.template, {
            patterns: this.patterns,
            showPattern: this.showPattern
        }));

        var enableAddNews = (this.mode === 'multi-news');
        var enableSummary = (this.mode === 'single-news');
        if (enableSummary) {
            this.$('.xa-weixin-edit-summaryBox').show();
            this.$el.find('#summary').attr('data-validate', 'require-notempty');
            // this.$('.xa-weixin-edit-urlBox').show();
            //this.$el.find('#url').attr('data-validate','customer-url');
        } else {
            this.$el.find('#summary').attr('data-validate', '');
            // this.$('.xa-weixin-edit-urlBox').show();
            //this.$el.find('#url').attr('data-validate','customer-url');
        }

        /**
         * 创建news editor
         * @type {W.NewsEditorView}
         */
        this.newsEditor = new W.view.weixin.NewsEditor({
            el: this.$('.xa-news-editor-box').get(),
            enableAnimation: true
        });
        if (options.mode == 'single-news') {
            this.newsEditor.preserveNewsUnder(1);
        } else if (options.mode == 'multi-news') {
            this.newsEditor.preserveNewsUnder(2);
        }

        /**
         * 初始化模拟器
         */
        this.phone = new W.view.weixin.EmbededPhoneView({
            el: this.$('.xa-simulator-box').get(),
            enableAddNews: enableAddNews,
            enableAction: true,
            onBeforeChangeNews: _.bind(function() {
                return this.newsEditor.validate();
            }, this),
            onBeforeCreateNews: _.bind(function() {
                return this.newsEditor.validate();
            }, this)
        });
        this.phone.bind('select-news', function(news, count, index) {
            this.newsEditor.setCountNews(count);
            this.newsEditor.edit(news);
            this.newsEditor.setImagePromptInfo(index);
        }, this);
        this.phone.bind('start-create-news', function() {
            xlog('start-create-news')
            var message = W.model.weixin.Message.createNewsMessage({
                autoSelect: true
            });
            if (this.mode === 'multi-news') {
                this.phone.appendNews(message);
            } else {
                this.phone.addNews(message);
            }
            //this.newsEditor.startCreateNews();
        }, this);
        this.phone.render();

        //初始化微信消息
        var newsCount = options.newses ? options.newses.length : 0;
        for (var i = 0; i < newsCount; ++i) {
            var news = options.newses[i];
            news.summary = news.summary.replace(/<br\/>/g, '\n');
            var newsMessage = W.model.weixin.Message.createNewsMessage();
            newsMessage.set(news);
            if (i == 0) {
                this.phone.addNews(newsMessage);
            } else {
                this.phone.appendNews(newsMessage);
            }
        }

        /**
         * 绑定news editor事件
         */
        this.newsEditor.bind('finish-create-news', function(news) {
            this.phone.appendNews(news);
        }, this);
        this.newsEditor.bind('delete-news', function(news) {
            this.phone.deleteNews(news);
        }, this);
        this.newsEditor.bind('finish-delete-news', function(news) {
            this.phone.selectNewsByIndex(0);
        }, this);

        //在newsCount为0时，依据mode创建空news
        if (newsCount == 0 && options.mode) {
            if (options.mode == 'single-news') {
                this.newsEditor.preserveNewsUnder(1);
                var message = W.model.weixin.Message.createNewsMessage({
                    autoSelect: true,
                    scheduledDate: this.scheduledDate
                });
                this.phone.addNews(message);
            } else if (options.mode == 'multi-news') {
                this.newsEditor.preserveNewsUnder(2);
                var messages = [
                    W.model.weixin.Message.createNewsMessage({
                        autoSelect: true
                    })
                ];
                for (var i = 1; i < this.initCount; i++) {
                    messages.push(W.model.weixin.Message.createNewsMessage());
                }
                this.phone.addNewses(messages);
            }
        }
        this.messageId = options.messageId;

        this.changeEditAction();
    },

    render: function() {
        //创建html
        return this;
    },

    /**
     * 提交按钮的响应函数
     * @param event
     */
    onSubmitNews: function(event) {
        if(!this.phone.validate()){
            return false;
        }
        // if (!W.validate()) {
        //     return false;
        // }

        var newses = this.phone.getNewCreatedNewses();
        // 多图文时判断是否添加了两条
        var isAllRight = this.isAllRightNewses(newses);
        if (!isAllRight) {
            W.getErrorHintView().show('请添加第二条图文信息');
            this.phone.selectNewsByIndex(1); //选中第二条图文信息
            return false;
        }
        W.getLoadingView().show();

        var data = JSON.stringify(newses);

        var method = 'put';
        if (this.materialId != "-1") {
            method = 'post'
        }

        var resource = 'single_news';
        if (this.mode === 'multi-news') {
            resource = 'multi_news'
        }
        var task = new W.DelayedTask(function() {
            W.getApi().call({
                method: method,
                app: 'new_weixin',
                resource: resource,
                args: {
                    material_id: this.materialId,
                    delete_ids: this.phone.getDeletedNewsIds(),
                    action_value: $('#actionDiv input[type=radio]:checked').val() || 0,
                    data: data
                },
                success: function(data) {
                    this.trigger('finish-create-material', data);
                    W.getLoadingView().hide();
                },
                error: function(response) {
                    alert('添加素材失败');
                    W.getLoadingView().hide();
                },
                scope: this
            });
        }, this);
        task.delay(100);
    },
    /**
     * 判断多图文是否添加完两条记录
     * @param newses
     */
    isAllRightNewses: function(newses) {
        var isAllRight = true;
        _.filter(newses, function(news) {
            if (news.title == "") {
                isAllRight = false;
                return isAllRight;
            }
        }, this);
        return isAllRight
    }
});
