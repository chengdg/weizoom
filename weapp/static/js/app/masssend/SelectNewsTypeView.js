/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 选择图文消息类型的View
 * @constructor
 */
W.SelectNewsTypeView = Backbone.View.extend({
	el: '',

	events: {
		'click #singleNewsLink': 'onClickSingleNewsLink',
		'click #multiNewsLink': 'onClickMultiNewsLink',
		'click #embededPhone-deleteBtn': 'onClickDeleteMaterialButton'
	},

	compileTemplate: function() {
		$('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.singleNewsUrl = '/massend/single_news/edit/';
		this.multiNewsUrl = '/massend/single_news/edit/';

		this.isDisableLink = false;
		this.returnQueryString = null;
		this.material = options.material || 0;

		this.newses = null;
	},

	render: function() {
	},

	__format_date: function(date) {
		var items = date.split('-');
		var month = parseInt(items[1]);
		var day = parseInt(items[2]);
		return month+'月'+day+'日';
	},

	/**
	 * 显示已编辑好的素材 
	 */
	showMaterial: function(materialId, enableDeleteMaterial, date) {
		this.material = materialId;
		this.$('#timedWeixinEditer-newsMessageZone-editLinkZone').hide();
		if (date) {
			date = this.__format_date(date);
		}

		W.getApi().call({
			app: 'masssend',
			api: 'material/get',
			args: {
				id: materialId
			},
			success: function(material) {
				newses = material.items;
				if (newses.length === 1) {
					var news = newses[0];
					if (date) {
						//替换date
						news.date = date;
					}
					var node = $.tmpl('single-news-tmpl', {
						news: news,
						enableEdit: true,
						enableDeleteMaterial: enableDeleteMaterial
					}).removeClass('mt10');
					this.$('#small-phone').html(node).show();
				} else {
					//multi_news
		            var mainNews = newses[0];
		            var subNewses = newses.slice(1);
		            var node = $.tmpl('multi-newses-tmpl', {
		                mainNews: mainNews,
		                subNewses: subNewses,
		                enableEdit: true,
						enableDeleteMaterial: enableDeleteMaterial
		            }).removeClass('mt10');
		            this.$('#small-phone').html(node).show();
				}
				this.trigger('showMaterialed', newses);
				return newses;
			},
			error: function(resp) {

			},
			scope: this
		});
	},

	/**
	 * 显示编辑链接区域 
	 */
	showEditLink: function() {
		var phoneZone = this.$('#small-phone');
		phoneZone.hide().html('');

		var editLinkZone = this.$('#timedWeixinEditer-newsMessageZone-editLinkZone');
		if (!editLinkZone.is(":visible")) {
			this.$('#timedWeixinEditer-newsMessageZone-editLinkZone').show();
		}
	},

	/**
	 * 设置进入图文编辑后返回链接的query string
	 */
	setReturnQueryString: function(queryString) {
		this.returnQueryString = encodeURIComponent(queryString);
	},

	// /**
	//  * 将链接禁用
	//  */
	// disableLink: function() {
	// 	this.isDisableLink = true;
	// },

	// /**
	//  * 将链接启用
	//  */
	// enableLink: function() {
	// 	this.isDisableLink = false;
	// },

	/**
	 * 单图文消息链接的点击响应函数
	 */
	onClickSingleNewsLink: function(event) {
		event.stopPropagation();
		event.preventDefault();

		this.trigger('before-edit-news');

		var url = $(event.target).attr('href');
		if (this.returnQueryString) {
			url += ('?return=' + this.returnQueryString);
		}

		window.location.href = url;
	},

	/**
	 * 多图文消息链接的点击响应函数
	 */
	onClickMultiNewsLink: function(event) {
		event.stopPropagation();
		event.preventDefault();

		this.trigger('before-edit-news');

		var url = $(event.target).attr('href');
		if (this.returnQueryString) {
			url += ('?return=' + this.returnQueryString);
		}

		window.location.href = url;
	},

	/**
	 * 点击删除素材按钮的响应函数
	 */
	onClickDeleteMaterialButton: function(event) {
		event.stopPropagation();
        event.preventDefault();

        var $el = $(event.target);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
        	this.trigger('delete-material');
			this.showEditLink();
			deleteCommentView.hide();
		}, this);

		deleteCommentView.show({
            $action: $el,
            info: '确定删除该图文消息吗?'
        });
	}
});