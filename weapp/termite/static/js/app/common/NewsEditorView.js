/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑器
 * @class
 */
W.common.NewsEditorView = Backbone.View.extend({
	el: '#news-editor',

	events: {
        'click #delete-news-btn': 'onDeleteNews',
        'input input[name="title"]': 'onChangeTitle',
        'input textarea[name="summary"]': 'onChangeSummary',
        'input textarea[name="text"]': 'onChangeText'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$form = this.$('#formWrapper');

		this.enableAnimation = options.enableAnimation;
		this.container = null;

		this.news = null;
		this.preserveNewsIndex = 0;

        //初始化ImageView
        this.imageView = new W.ImageView({
            el: options.imageView
        });
        this.imageView.bind('upload-image-success', function(path) {
        	this.$el.find('#picUrlInput').val(path);
        	this.news.set('pic_url', path);
            this.trigger('upload-image-success', path);
        }, this);
        this.imageView.bind('delete-image', function(path) {
            this.$el.find('#picUrlInput').val('');
            if (this.news) {
	            this.news.set('pic_url', '');
	        }
        }, this);
        this.imageView.render();

        this.editor = new W.common.RichTextEditor({
			el: 'textarea#text',
			type: 'richtext',
			imgSuffix: "uid="+W.uid,
	        height: 300,
	        autoHeight: false,
			wordCount: false,
			maxCount: 600
		})
		this.editor.bind('contentchange', function() {
			this.$textInput.val(this.editor.getContent());
			this.onChangeText();
		}, this);
		this.editor.render();

        //初始化输入控件
        this.$titleInput = this.$('input[name="title"]');
        this.$summaryInput = this.$('textarea[name="summary"]');
        this.$textInput = this.$('textarea[name="text"]');

		this.countNews = options.countNews || this.preserveNewsIndex
	},

	/**
	 * 对于display_index小于等于index的message，不显示delete按钮
	 */
	preserveNewsUnder: function(index) {
		this.preserveNewsIndex = index;
	},

	setCountNews: function(count){
		this.countNews = count;
	},

	/**
	 * 显示删除按钮
	 */
	showDeleteButtonFor: function(message) {
		if (parseInt(message.get('display_index')) > 1 && this.countNews > this.preserveNewsIndex) {
			$('#update-news-btns-box').show();
		} else {
			$('#update-news-btns-box').hide();
		}
	},

	/**
	 * 重置编辑器
	 */
	reset: function() {
		this.news = null;
        $('#picUrlInput').val('');
		$('#title').val('');
		$('#text').val('');
		$('#summary').val('');
        this.imageView.cleanImage();
	},

	/**
	 * 编辑一条news
	 * @param news
	 */
	edit: function(news) {
        xlog('edit')
		if (!this.news || this.news.id != news.id) {
			this.reset();
			this.news = news;
			
			var titleInput = $('#title');
			titleInput.val(news.get('title'));
			$('#text').val(news.get('text'));
			this.editor.setContent(news.get('text'));

			this.imageView.showImage(news.get('pic_url'));
			$('#picUrlInput').val(news.get('pic_url'));

            $('#summary').val(news.get('summary'));

			titleInput.focus();

			this.showDeleteButtonFor(this.news);
		}
	},

	render: function() {
	},

	/**
	 * title输入框内容改变的响应函数
	 */
	onChangeTitle: function() {
		this.news.set('title', this.$titleInput.val());
	},

	/**
	 * summary输入框内容改变的响应函数
	 */
	onChangeSummary: function() {
		this.news.set('summary', this.$summaryInput.val());
	},

	/**
	 * text输入框内容改变的响应函数
	 */
	onChangeText: function() {
		this.news.set('text', this.$textInput.val());
	},

	/**
	 * delete-news-btn按钮的点击响应函数
	 */
	onDeleteNews: function() {
        var $el = $("#delete-news-btn");
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
            this.trigger('delete-news', this.news);
            deleteCommentView.hide();
            this.trigger('finish-delete-news');
        }, this);
        deleteCommentView.show({
             $action: $el,
             info: '确定删除吗?'
        });
	},

	/**
	 * 验证当前编辑器中的字段是否合法
	 */
	validate: function() {
		return W.validate();
	}
});