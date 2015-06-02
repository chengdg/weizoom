/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.question.EditProblemDialog = W.Dialog.extend({
	SUBMIT_SUCCESS_EVENT: 'problem_submit',

	events: _.extend({
		'click .tx_cancel': 'close',
		'click .tx_submit': 'onSubmit'
	}, W.Dialog.prototype.events),

	getTemplate: function() {
		$('#edit-problem-dialog-src').template('edit-problem-dialog-tmpl');
		return 'edit-problem-dialog-tmpl';
	},

	initializeDialog: function() {
		this.render();
		this.$editEl = $('#editorView-editProblemDialog');
		this.editor_title = new W.common.RichTextEditor({
			el: '#title',
			type: 'text',
			height: 60,
			width:360,
			maxCount: 600
		});

		this.editor_error_feedback = new W.common.RichTextEditor({
			el: '#error_feedback',
			type: 'text',
			height: 60,
			width:360,
			maxCount: 600
		});

		this.editor_right_feedback = new W.common.RichTextEditor({
			el: '#right_feedback',
			type: 'text',
			height: 60,
			width:360,
			maxCount: 600
		});
		this.editor_title.render();
		this.editor_error_feedback.render();
		this.editor_right_feedback.render();
	},

	renderDialog: function() {
		var html = $.tmpl(this.getTemplate(), {state :this.state});
		this.$contentEl.html(html);
	},

	showDialog: function(options) {
		this.title = options.title;
		this.problem = options.problem;
		this.state = options.state;

		if(this.state =='create'){
			this.$('.tx_submit').html('添加');
		}else{
			this.$('.tx_submit').html('修改');
		}

		this.$('.errorHint').hide();
		$("#title").val(this.problem.get('title_content'));
		$('#right_answer').val(this.problem.get('right_answer'));
		$('#right_feedback').val(this.problem.get('right_feedback_content'));
		$('#error_feedback').val(this.problem.get('error_feedback_content'));

		this.editor_title.setContent(this.problem.get('title_content'));
		this.editor_right_feedback.setContent(this.problem.get('right_feedback_content'));
		this.editor_error_feedback.setContent(this.problem.get('error_feedback_content'));

	},

	onSubmit: function() {
		if (!W.validate($('#editorView-editProblemDialog'))) {
			return;
		}

		this.problem.set('right_answer', $.trim(this.$editEl.find('#right_answer').val()));
		this.problem.set('title', $.trim(this.editor_title.getContent()));
		this.problem.set('right_feedback', $.trim(this.editor_right_feedback.getContent()));
		this.problem.set('error_feedback', $.trim(this.editor_error_feedback.getContent()));

		this.problem.set('title_content', $.trim(this.editor_title.getHtmlContent()));
		this.problem.set('right_feedback_content', $.trim(this.editor_right_feedback.getHtmlContent()));
		this.problem.set('error_feedback_content', $.trim(this.editor_error_feedback.getHtmlContent()));

		this.trigger(this.SUBMIT_SUCCESS_EVENT, this.problem);
	},

	afterClose: function() {
		this.unbind();
		this.editor_title.setContent('');
		this.editor_right_feedback.setContent('');
		this.editor_error_feedback.setContent('');
		this.$('#title, #right_feedback, #error_feedback, #right_answer').val('');
	}
});

/**
 * 获得getEditProblemDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.question.getEditProblemDialog = function(options) {
	var dialog = W.registry['EditProblemDialog'];
	if (!options) {
		options = {};
	}
	options.width = options.width || 500;
	options.height = options.height || 400;

	if (!dialog) {
		//创建dialog
		xlog('create W.EditProblemDialog');
		dialog = new W.question.EditProblemDialog(options);
		W.registry['EditProblemDialog'] = dialog;
	}
	return dialog;
};