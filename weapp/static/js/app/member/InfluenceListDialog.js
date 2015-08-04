/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * Customer备注的编辑对话框
 */
W.InfluenceListDialog = W.DropBox.extend({

	getTemplate: function() {
		$('#dialog-view-influence-list-tmpl-src').template('influence-list-dialog-tmpl');
		return 'influence-list-dialog-tmpl';
	},

	getOneTemplate: function() {
		$('#one-influence-tmpl-src').template('one-influence-tmpl');
		return 'one-influence-tmpl';
	},

	events: _.extend({}, W.Dialog.prototype.events, {
		'click .tx_submit': 'submit'
	}),

	initializePrivate: function(options) {
		this.tmplName = this.getTemplate();
		this.typeTextCount = 300;
		this.memberId = 0;
	},

	showPrivate: function(options) {
		this.title = 'bianji'
		this.render(options);
	},

	render: function(options) {
		options = options || {};
		this.appName = options.appName;
		this.setPosition('down-left');
		if(this.memberId != options.memberId){
			this.memberId = options.memberId || 0;
			this.influences = new W.rice.Influences();
			this.influences.app = this.appName || 'rice'
			this.influences.memberId = this.memberId;
			this.influences.bind('add', this.onAdd, this);
			this.influences.fetch();
			this.$content.html($.tmpl(this.tmplName, options));
			this.$notTr = this.$('tr[data-id="0"]');
		}
	},

	onAdd: function(influence){
		this.$notTr.hide();
		var influence_count = parseFloat(influence.get('influence'));
		influence.set('influence',influence_count.toFixed(2));
		this.$('table.rice-influence-table>tbody').prepend($.tmpl(this.getOneTemplate(), influence.toJSON()));
	}

});

/**
 * 获得InfluenceListDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getInfluenceListDialog = function(options) {
	options = options || {}
	options.width = options.width || 480;
	options.height = options.height || 500;

	var dialog = W.registry['InfluenceListDialog'];
	if (!dialog) {
		//创建dialog
		xlog('create W.InfluenceListDialog');
		dialog = new W.InfluenceListDialog(options);
		W.registry['InfluenceListDialog'] = dialog;
	}
	return dialog;
};