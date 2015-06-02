/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑面板
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.NewsPreviewer = Backbone.View.extend({
    el: '',

    events: {
    },

    getTemplate: function() {
        $('#weixin-news-preview-tmpl-src').template('weixin-news-preview-tmpl');
        return 'weixin-news-preview-tmpl';
    },

    initialize: function(options) {
        xlog("in NewsPreviewer.initialize()");
        this.$el = $(this.el);
        this.mode = options.mode || 'multi-news';
        this.scheduledDate = options.scheduledDate;
        this.materialId = options.materialId || '-1';
        this.headImg = options.headImg || '/static/img/user-1.jpg';

        this.initCount = options.initCount || 1; //model为multi-news时有效
        this.patterns = options.patterns || '';
        this.showPattern = options.showPattern || false;
        this.typeMaterial = options.typeMaterial || 1;

        this.template = this.getTemplate();

        this.$el.html($.tmpl(this.template, {
            patterns: this.patterns,
            showPattern: this.showPattern,
            materialId: this.materialId,
            headImg: this.headImg,
            typeMaterial: this.typeMaterial
        }));

        /**
         * 初始化模拟器
         */
        this.phone = new W.view.weixin.EmbededPhoneView({
            el: this.$('.xa-simulator-box').get(),
            enableAction: false,
            enableAddNews: false
        });
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
        this.messageId = options.messageId
    },

    render: function() {
        //创建html
        return this;
    }
});
