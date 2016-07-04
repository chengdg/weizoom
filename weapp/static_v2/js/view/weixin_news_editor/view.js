/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.weixin')
W.view.weixin.NewsEditor = Backbone.View.extend({
	el: '',

	events: {
		'click #delete-news-btn': 'onDeleteNews',
		'input input[name="title"]': 'onChangeTitle',
		'input textarea[name="summary"]': 'onChangeSummary',
		'input textarea[name="text"]': 'onChangeText',
		'input textarea[name="text"]': 'onChangeTextDisplay',
		'input input[name="url"]': 'onChangeUrl',
		'input input[name="link_target"]': 'onChangeLinkTarget',
		'input input[name="pic_url"]': 'onChagePic',
		'click input[name="is_show_cover_pic"]': 'onChageIsShowCoverPic',
		'click .xa-news-editor-select-link-dialog': 'onClickSelectWebAppLinkTargetButton',
		// 'change input[name="change_action"]': 'changeAction',
		'click .xa-edit-textShowBtn': 'onClickShowTextBox',
		'click .xa-edit-urlShowBtn': 'onClickShowUrlBox',
		'blur input[name="urlDisplayValue"]': 'onBlurUrlDisplayValue',		
		'click .xa-news-editor-select-link-menu': 'onClickLinkMenu',

        'mouseover .xa-tips': 'onMouseoverTips',
        'mouseout .xa-tips': 'onMouseoutTips',
	},

	onClickShowTextBox: function(event){	
		$('.xa-edit-textShowBtn').addClass('active');
		$('.xa-edit-urlShowBtn').removeClass('active');

    	this.$('.xa-weixin-edit-urlBox').hide();
		this.$('.xa-weixin-edit-urlBox').find('#urlDisplayValue').attr('data-validate','');
		
		this.$('.xa-weixin-edit-textAreaBox').find('textarea').attr('data-validate','require-notempty');
		this.$('.xa-weixin-edit-textAreaBox').find('textarea').attr('data-force-validate',true);
		this.$('.xa-weixin-edit-textAreaBox').find('textarea').attr('maxlength','2000000');
		this.$('.xa-weixin-edit-textAreaBox').show();
		// 显示图文，需要显示“封面图片显示在正文中”的checkbox
		this.$('#showCoverPicOption').show();
		// 修改链接
		if (this.news) {
			if (!event) {
				this.webSiteLinkView.setEditHtml(this.news.get('link_target'), true);
			}else{
				this.webSiteLinkView.setEditHtml(null, true);
			}
		}
	},

	onClickShowUrlBox: function(event){
		$('.xa-edit-textShowBtn').removeClass('active');
		$('.xa-edit-urlShowBtn').addClass('active');	

		this.$('.xa-weixin-edit-textAreaBox').find('textarea').removeAttr('data-validate');
		this.$('.xa-weixin-edit-textAreaBox').find('textarea').removeAttr('data-force-validate');
		this.$('.xa-weixin-edit-textAreaBox').find('textarea').removeAttr('maxlength');

		this.$('.xa-weixin-edit-textAreaBox').hide();
		this.$('.xa-weixin-edit-urlBox').find('#urlDisplayValue').attr('data-validate','require-notempty');
		this.$('.xa-weixin-edit-urlBox').show();
		//进入微站，需要隐藏“封面图片显示在正文中”的checkbox
		this.$('#showCoverPicOption').hide();
	},

	changeContentBox: function(){	
		var urlLink = $.trim(this.$urlInput.val());

		if(urlLink.length === 0){
			this.onClickShowTextBox();
		}else{
			this.onClickShowUrlBox();		
		}
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.$form = this.$('.xa-news-editor-form');

		this.enableAnimation = options.enableAnimation;
		this.container = null;

		this.news = null;
		this.preserveNewsIndex = 0;

		this.imageHeight = 100;
		this.imageWidth = 100;

		this.minImageHeight = 100;
		this.minImageWidth = 100;

		//初始化ImageView
		this.imageView = new W.view.common.ImageView({
	        el: this.$('.xa-weixin-edit-imageView'),
	        height: this.imageHeight,
	        width: this.imageWidth,
	        sizeLimit: 1024,
	        format: 'jpg',
	        autoShowHelp: false,
	        buttonText: '添加图片'
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

		//创建富文本编辑器
		this.editor = new W.view.common.RichTextEditor({
			el: 'textarea#text',
			type: 'full',
			imgSuffix: "uid="+W.uid,
			width: 367,
			height: 250,
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
		this.$urlInput = this.$('input[name="url"]');
		this.$linkTargetInput = this.$('input[name="link_target"]');

		//选择内部链接
		this.webSiteLinkView = W.getSelectWebSiteLinkView({
			el: '.xa-weixin-edit-urlBox'
		});
		/*
		this.webSiteLinkView.bind('selected-url', function(data){
            var linkTarget = $.parseJSON(data);
            $urlInput.val(linkTarget.data).trigger('input');
            $linkTargetInput.val(data).trigger('input');
            $displayValueInput.val(linkTarget.data_path);
		});*/

		this.countNews = options.countNews || this.preserveNewsIndex;

		// this.changeContentBox();
	},

	onClickLinkMenu: function(event){		
		//选择内部链接
		this.webSiteLinkView = W.getSelectWebSiteLinkView({
			el: '.xa-weixin-edit-urlBox'
		});
		this.webSiteLinkView.onClickLinkMenu(event);
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

	setImagePromptInfo: function(index){
		var imgPrompt = '900X500';
		if (index > 1) {
			imgPrompt = '200X200';
		}
		this.$el.find('.xa-img-prompt').html(imgPrompt);
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
	 * 显示图片编辑，主要修改图片显示宽高，和默认图片显示
	 */
	showImageViewFor: function(message) {
		if (parseInt(message.get('display_index')) > 1) {
			// this.imageView.setSizeLimit(64);
			this.imageView.computeWidthAndHeight({
				width: this.minImageWidth,
				height: this.minImageHeight
			});
		} else {
			//this.imageView.setSizeLimit(128);
			this.imageView.computeWidthAndHeight({
				width: this.imageWidth,
				height: this.imageHeight
			});
		}
		this.imageView.showImage(message.get('pic_url'));
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
		$('#url').val('');
		$('#linkTarget').val('');
		$('#urlDisplayValue').val('');
		$('#showCoverPicCheckbox').removeAttr('checked');
		this.imageView.cleanImage();
	},

	/**
	 * 编辑一条news
	 * @param news
	 */
	edit: function(news) {
		xlog('edit')
		xlog(news);

		// 清空错误提示
		this.$el.find('.errorHint').css('display', 'none');
		
		if (!this.news || this.news.id != news.id) {
			this.reset();
			this.news = news;
			var titleInput = $('#title');
			titleInput.val(news.get('title'));
			$('#text').val(news.get('text'));
			this.editor.setContent(news.get('text'));

			$('#picUrlInput').val(news.get('pic_url'));

			$('#summary').val(news.get('summary'));

			$('#url').val(news.get('url'));

			if (news.get('is_show_cover_pic')) {
				$('#showCoverPicCheckbox').attr('checked', 'checked');
			}

			var linkTarget = news.get('link_target');
			// $('#urlDisplayValue').val(linkTarget.data_path);
			// $('#linkTarget').data('link_target', linkTarget);
			if (typeof(linkTarget) === 'object') {
				linkTarget = JSON.stringify(linkTarget);
			}
			this.webSiteLinkView.setEditHtml(linkTarget, true);

			titleInput.focus();

			this.showDeleteButtonFor(this.news);
			this.showImageViewFor(this.news);
			// this.textDivIsShow();

			//初始化是否在封面显示图片的选择值
			if (news.get('is_show_cover_pic')) {
				$('#showCoverPicOption').val('true');
			} else {
				$('#showCoverPicOption').val('false');
			}

			this.setEditPagePosition(news);
			// this.changeContentBox();
		}
	},

	setEditPagePosition: function(news){
		var top = $('.xa-i-news-message[data-id="'+news.id+'"]').position().top;
		this.$el.css('margin-top', top);
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
	 * url输入框内容改变的响应函数
	 */
	onChangeUrl: function() {
		this.news.set('url', $.trim(this.$urlInput.val()));	
		// this.textDivIsShow();
	},

	onBlurUrlDisplayValue: function(){		
		/**
		 * 处理外部链接
		 */	
		this.webSiteLinkView.handlerCustomerUrl();
	},

	/**
	 * link_target输入框内容改变的响应函数
	 */
	onChangeLinkTarget: function() {
		// var linkTargetVal = $.trim(this.$linkTargetInput.val());
		// this.news.set('link_target', $.parseJSON(linkTargetVal));
		this.news.set('link_target', $.trim(this.$linkTargetInput.val()));
	},

	/**
	 * text输入框内容改变的响应函数
	 */
	onChangeText: function() {
		this.news.set('text', this.$textInput.val());
	},

	onChangeTextDisplay: function() {
		this.editor.setContent(this.$textInput.val());
	},

	onChagePic: function(event) {
		var pic_url = $(event.currentTarget).val();
		if(this.imageView) {
			this.imageView.showImage(pic_url);
		}
		this.news.set('pic_url', pic_url);
	},

	onChageIsShowCoverPic: function(event) {
		var $checkbox = $(event.currentTarget);
		this.news.set('is_show_cover_pic', $checkbox.is(':checked'));
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
	},

	/**
	 * 当连接地址中内容时，正文输入框就消失；
	 * 当连接地址没有内容时，正文输入框显示。
	 */
	textDivIsShow: function(){
		if($.trim(this.$urlInput.val())){
			this.$('.xa-weixin-edit-textAreaBox').hide();
			this.$textInput.attr('data-validate', '');
		}else{
			this.$('.xa-weixin-edit-textAreaBox').show();
			this.$textInput.attr('data-validate', 'require-notempty');
		}
	},

	/**
	 * onClickSelectWebAppLinkTargetButton: 点击选择weapp链接地址的按钮后的响应函数
	 */ 
	onClickSelectWebAppLinkTargetButton: function(event) {
		var inputName = this.$('.xa-news-editor-select-link-dialog').attr('data-input');
        var $urlInput = this.$('[name="'+inputName+'"]');
        var $linkTargetInput = this.$('[name="link_target"]');
        var $displayValueInput = this.$('[name="'+inputName+'DisplayValue"]');
        var currentLinkTarget = $linkTargetInput.data('link_target');
        xlog('1.');
        xlog(currentLinkTarget);
        W.dialog.showDialog('W.dialog.workbench.SelectLinkTargetDialog', {
            currentLinkTarget: currentLinkTarget,
            success: function(data) {
                var linkTarget = $.parseJSON(data);
                $urlInput.val(linkTarget.data).trigger('input');
                $linkTargetInput.val(data).trigger('input');
                $displayValueInput.val(linkTarget.data_path);
            }
        });
	},

    onMouseoverTips: function(event){
        console.log('onMouseoverTips', this.wrapEl)
        if ($('.xa-tips-wrap').length > 0) {
            $('.xa-tips-wrap').css("display","block");
        };
    },

    onMouseoutTips: function(event){
        if ($('.xa-tips-wrap').length > 0) {
            $('.xa-tips-wrap').css("display","none");
        }
    }
});