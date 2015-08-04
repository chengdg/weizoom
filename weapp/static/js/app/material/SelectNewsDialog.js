/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.material.SelectNewsDialog = W.Dialog.extend({
	SUBMIT_SUCCESS_EVENT: 'submit',

	events: _.extend({
		'click .tx_cancel': 'close',
		'click .tx_submit': 'onSubmit'
	}, W.Dialog.prototype.events),

	getTemplate: function() {
		$('#newses-dialog-tmpl-src').template('newses-dialog-tmpl');
		return 'newses-dialog-tmpl';
	},

	getOneTemplate: function() {
		$('#one-news-tmpl-src').template('one-news-tmpl');
		return 'one-news-tmpl';
	},

	initializeDialog: function() {
		this.render();
		this.$editEl = $('#tx_newsesSelect');

		this.state = null;
		this.title='选择推荐的商品';

		this.selectedIds = [];

		var newsesView = new W.material.NewsesView({
			el: '#dialog-newses-tmpl-src',
			enableEdit: false
		});
		newsesView.bind('finish-delete-news', function(){
			window.location.href = '/material/newses/'
		});
		newsesView.bind('finish-update-news', function(newsId){
			window.location.href = '/material/news/update/'+newsId+'/';
		});
		newsesView.$el.css({'overflow':'auto','height':'350px'});

		var itemView = new W.ItemCheck({
			el: '#dialog-newses-tmpl-src',
			isRadio: true
		});
		itemView.bind('checked', function(ids){
			this.selectedIds = ids;
		}, this);
	},

	renderDialog: function() {
		var html = $.tmpl(this.getTemplate(), {state :this.state});
		this.$contentEl.html(html);
	},

	/**
	 * 加载shop的分类
	 */
	addProductCategory: function(category) {
//		this.categorySelect.append('<option value="'+ category.get('id') +'">'+category.get('name')+'</option>');
	},


	showDialog: function(options) {
		this.title = options.title;
		this.materialId = options.materialId;
		if(this.materialId == 0){
			xlog('所有不选中');
		}
	},

	onSubmit: function() {
		xlog('finish-submit-news');
		this.trigger('finish-submit-news', this.selectedIds);
		this.close();
	},

	afterClose: function() {
		this.unbind();
	}
});

/**
 * 获得getSelectNewsDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.material.getSelectNewsDialog = function(options) {
	var dialog = W.registry['SelectNewsDialog'];
	if (!options) {
		options = {};
	}
	options.width = options.width || 725;
	options.height = options.height || 460;

	if (!dialog) {
		//创建dialog
		xlog('create W.material.SelectNewsDialog');
		dialog = new W.material.SelectNewsDialog(options);
		W.registry['SelectNewsDialog'] = dialog;
	}
	return dialog;
};