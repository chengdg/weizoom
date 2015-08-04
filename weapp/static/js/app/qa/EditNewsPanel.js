/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑面板
 * @class
 */

W.EditNewsPanel = Backbone.View.extend({
	el: '#edit-news-panel',

	events: {
		'click #submit-btn': 'onSubmitNews'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.$imageView = $(options.imageViewEl);

		/**
		 * 创建news editor
		 * @type {W.NewsEditorView}
		 */
		this.newsEditor = new W.NewsEditorView({
			el: $('#news-editor-box'),
            imageView: this.$imageView,
			enableAnimation: true
		});

		/**
		 * 初始化模拟器
		 */
		this.phone = new W.SmallPhoneView({
			el: $('#small-phone-box'),
            enableAddNews: true,
            enableAction: true
		});
		this.phone.bind('select-news', function(news) {
			this.newsEditor.edit(news);
		}, this);
		this.phone.bind('start-create-news', function() {
			this.newsEditor.startCreateNews();
		}, this);
		this.phone.render();
        var newsCount = options.newses ? options.newses.length : 0;
        for (var i = 0; i < newsCount; ++i) {
            var news = options.newses[i];
            if (i == 0) {
                this.phone.addNews(news);
            } else {
                this.phone.appendNews(news);
            }
        }

		/**
		 * 绑定news editor事件
		 */
		this.newsEditor.bind('finish-create-news', function(news) {
			this.phone.appendNews(news);
		}, this);
		this.newsEditor.bind('update-news', function(news) {
			this.phone.updateNews(news);
		}, this);
		this.newsEditor.bind('delete-news', function(news) {
			this.phone.deleteNews(news);
		}, this);
		this.newsEditor.bind('editor-hidden', function(news) {
			if (this.phone.hasNewCreatedNews()) {
				$('#submit-btn').show();
			}
			this.phone.checkNews();
		}, this);

		this.ruleId = options.ruleId;
		this.categoryId = options.categoryId;
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
		if (newses.length == 0) {
			var task = new W.DelayedTask(function() {
				W.getLoadingView().hide();
                window.location.href = '/qa/rules/'+this.categoryId+'/';
			},this);
			task.delay(200);
		} else {
			var data = JSON.stringify(newses);
			var patternsInput = $('#patterns');
			var patterns = $.trim(patternsInput.val());

	        var task = new W.DelayedTask(function() {
	            W.getApi().call({
	                app: 'qa',
	                api: 'news/add',
	                method: 'post',
	                args: {
	                    rule_id: this.ruleId,
	                    category_id: this.categoryId,
	                    data: data,
	                    patterns: patterns
	                },
	                success: function(rule) {
                        window.location.href = '/qa/rules/'+this.categoryId+'/';
	                },
	                error: function(response) {
	                    alert('添加商品失败');
	                    W.getLoadingView().hide();
	                },
	                scope: this
	            });
	        }, this);
	        task.delay(300);
    	}
	}
});