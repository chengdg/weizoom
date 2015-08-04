/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑器
 * @class
 */
W.NewsEditorView = Backbone.View.extend({
	el: '#news-editor',

	events: {
		'click #add-news-btn': 'onAddNews',
		'click #update-news-btn': 'onUpdateNews',
        'click #delete-news-btn': 'onDeleteNews'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$form = this.$('#formWrapper');

		this.enableAnimation = options.enableAnimation;
		this.container = null;

		this.newIdCounter = -99;
		this.news = null;

        //初始化ImageView
        this.imageView = new W.ImageView({
            el: options.imageView
        });
        this.imageView.bind('upload-image-success', function(path) {
        	this.$el.find('#picUrlInput').val(path);
            this.trigger('upload-image-success', path)
        }, this);
        this.imageView.bind('delete-image', function(path) {
            this.$el.find('#picUrlInput').val('');
        }, this);
        this.imageView.render();

        this.editer = new W.EditerView({
        	el: this.$el.find('textarea')
        })
        this.editer.render();
	},

	/**
	 * 重置编辑器
	 */
	reset: function() {
        $('#picUrlInput').val('');
		$('#title').val('');
		$('#description').val('');
        this.imageView.cleanImage();

		$('#update-news-btns-box').hide();
		$('#add-news-btns-box').show();
	},

	/**
	 * 编辑一条news
	 * @param news
	 */
	edit: function(news) {
		this.news = news;
		$('#title').val(news.title);
		$('#description').val(news.description);
		this.imageView.showImage(news.pic_url);

		$('#picUrlInput').val(news.pic_url);

		$('#add-news-btns-box').hide();
		$('#update-news-btns-box').show();

		this.showForm();
	},

	/**
	 * 创建一条新的图文信息
	 */
	startCreateNews: function() {
		this.reset();
		this.showForm();
	},

	render: function() {
	},

	/**
	 * 隐藏form
	 */
	hideForm: function() {
		var _this = this;
		if (this.enableAnimation) {
			this.$form.animate({
				"margin-left":"-=370"
			}, 300, 'swing', function() {
				_this.reset();
				_this.trigger('editor-hidden');
			});
		} else {
			this.$form.hide();
			this.trigger('editor-hidden');
		}
	},

	/**
	 * 显示form
	 */
	showForm: function() {
		if (this.$form.is(':visible') && this.$form.css('margin-left').indexOf('-') == -1) {
			//已经显示了，不用再次显示
			$('#title').focus();
			return;
		}

		if (this.enableAnimation) {
			this.$form.animate({
				"margin-left":"+=370"
			}, 300, function() {
				$('#title').focus();
			});
		} else {
			this.$form.show();
		}
	},

	/**
	 * add-news-btn按钮的点击响应函数
	 */
	onAddNews: function() {
		if (!W.validate($('#news-form'), true)) {
			return;
		}

		var title = $.trim($('#title').val());
		var description = $.trim($('#description').val());
		var picUrl = this.imageView.getImageUrl();
		//TODO: 添加url
		//TODO: 添加验证
        var date = new Date();
		this.trigger('finish-create-news', {
			id: this.newIdCounter,
			title: title,
			description: description,
			pic_url: picUrl,
            date: date.getMonth()+1+'月'+date.getDate()+'日'
		});
		this.newIdCounter -= 1;
		this.hideForm();
	},

	/**
	 * update-news-btn按钮的点击响应函数
	 */
	onUpdateNews: function() {
		if (!W.validate($('#news-form'), true)) {
			return;
		}
		
		var title = $.trim($('#title').val());
		var description = $.trim($('#description').val());
        var picUrl = this.imageView.getImageUrl();

		if (this.news.id < 0) {
			this.news.title = title;
			this.news.description = description;
			this.news.pic_url = picUrl;
			this.trigger('update-news', this.news);
			this.news = null;
			this.hideForm();
		} else {
            W.getLoadingView().show();
			this.news.title = title;
			this.news.description = description;
			this.news.pic_url = picUrl;
			var api = 'news/update';

            var task = new W.DelayedTask(function() {
                W.getApi().call({
                    app: 'qa',
                    api: api,
                    method: 'post',
                    args: {
                        title: title,
                        description: description,
                        pic_url: picUrl,
                        news_id: this.news.id
                    },
                    success: function(data) {
                        this.trigger('update-news', this.news);
                        this.news = null;
                        W.getLoadingView().hide();
                        this.hideForm();
                    },
                    error: function(response) {
                        W.getLoadingView().hide();
                        alert('修改商品信息失败');
                    },
                    scope: this
                });
            }, this);
            task.delay(300);
		}
	},

	/**
	 * delete-news-btn按钮的点击响应函数
	 */
	onDeleteNews: function() {
        var $el = $("#delete-news-btn");
        var _deleteCommentView = W.getItemDeleteView();
        _deleteCommentView.bind(_deleteCommentView.SUBMIT_EVENT, function(options){
            if (this.news.id < 0) {
                this.trigger('delete-news', this.news);
                this.news = null;
                this.hideForm();
                _deleteCommentView.hide();
            } else {
                var api = 'news/delete';
                W.getLoadingView().show();
                var task = new W.DelayedTask(function() {
                    W.getApi().call({
                        app: 'qa',
                        api: api,
                        method: 'post',
                        args: {
                            news_id: this.news.id
                        },
                        success: function(data) {
                            this.trigger('delete-news', this.news);
                            this.news = null;
                            W.getLoadingView().hide();
                            this.hideForm();
                            _deleteCommentView.hide();
                        },
                        error: function(response) {
                            alert('删除商品失败');
                            W.getLoadingView().hide();
                        },
                        scope: this
                    });
                }, this);
                task.delay(300);
            }
        }, this);
        _deleteCommentView.show({
             $action: $el,
             info: '确定删除吗?'
        });
	}
});