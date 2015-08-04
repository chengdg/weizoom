/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑面板
 * @class
 */

W.common.EditNewsPanel = Backbone.View.extend({
	el: '',

	events: {
		'click #submit-btn': 'onSubmitNews'
	},

    getTemplate: function(){
        $('#edit-news-view-tmpl-src').template('edit-news-view-tmpl');
        return 'edit-news-view-tmpl';
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.$imageView = options.imageViewEl;
        this.mode = options.mode || 'multi-news';
        this.scheduledDate = options.scheduledDate;
        this.materialId = options.materialId || '-1';

        this.initCount = options.initCount || 1;//model为multi-news时有效
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
            this.$('#summaryDiv').show();
            this.$el.find('#summary').attr('data-validate','required');
        }else{
            this.$el.find('#summary').attr('data-validate','');
        }

		/**
		 * 创建news editor
		 * @type {W.NewsEditorView}
		 */
		this.newsEditor = new W.common.NewsEditorView({
			el: $('#news-editor-box'),
			imageView: this.$imageView,
			enableAnimation: true
		});
        if (options.mode == 'single-news') {
            this.newsEditor.preserveNewsUnder(1);
        } else if(options.mode == 'multi-news') {
            this.newsEditor.preserveNewsUnder(2);
        }

		/**
		 * 初始化模拟器
		 */
		this.phone = new W.common.EmbededPhoneView({
			el: $('#small-phone-box'),
			enableAddNews: enableAddNews,
            enableAction: true,
            onBeforeChangeNews: _.bind(function() {
            	return this.newsEditor.validate();
            }, this),
            onBeforeCreateNews: _.bind(function() {
            	return this.newsEditor.validate();	
            }, this)
		});
		this.phone.bind('select-news', function(news, count) {
			this.newsEditor.setCountNews(count);
			this.newsEditor.edit(news);
		}, this);
		this.phone.bind('start-create-news', function() {
            xlog('start-create-news')
			var message = W.common.Message.createNewsMessage({autoSelect: true});
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
            var newsMessage = W.common.Message.createNewsMessage();
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
        		var message = W.common.Message.createNewsMessage({autoSelect: true, scheduledDate: this.scheduledDate});
        		this.phone.addNews(message);
        	} else if(options.mode == 'multi-news') {
        		this.newsEditor.preserveNewsUnder(2);
        		var messages = [
        			W.common.Message.createNewsMessage({autoSelect: true})
        		];
                for (var i = 1; i < this.initCount; i++){
                    messages.push(W.common.Message.createNewsMessage());
                }
        		this.phone.addNewses(messages);
        	}
        }
		this.messageId = options.messageId;
	},

    render: function(){
        //创建html
        return this;
    },

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmitNews: function(event) {
		if (!W.validate()) {
			return false;
		}
        W.getLoadingView().show();

		var newses = this.phone.getNewCreatedNewses();
		var data = JSON.stringify(newses);
        var api = 'material/create';
        if (this.materialId != "-1"){
            api = 'material/update'
        }
        var task = new W.DelayedTask(function() {
	        W.getApi().call({
	            app: 'masssend',
	            api: api,
	            method: 'post',
	            args: {
                    material_id: this.materialId,
                    delete_ids: this.phone.getDeletedNewsIds(),
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
	}
});