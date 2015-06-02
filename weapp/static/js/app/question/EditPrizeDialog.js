/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.question.EditPrizeDialog = W.Dialog.extend({
	SUBMIT_SUCCESS_EVENT: 'prize_submit',

	events: _.extend({
		'click .tx_cancel': 'close',
		'click .tx_prize_submit': 'onSubmit'
	}, W.Dialog.prototype.events),

	getTemplate: function() {
		$('#edit-prize-dialog-src').template('edit-prize-dialog-tmpl');
		return 'edit-prize-dialog-tmpl';
	},

	initializeDialog: function() {
		this.render();
		this.$editEl = $('#editorView-editPrizeDialog');
		this.editor_content = new W.common.RichTextEditor({
			el: '#content',
			type: 'text',
			height: 80,
			width:360,
			maxCount: 600
		});

		this.editor_content.render();
	},

	renderDialog: function() {
		var html = $.tmpl(this.getTemplate(), {state :this.state});
		this.$contentEl.html(html);
	},

	showDialog: function(options) {
		this.title = options.title;
		this.prize = options.prize;
		this.state = options.state;
		this.right_nums = options.right_nums;
		this.problem_length = options.problem_length;

		if(this.state =='create'){
			this.$('.tx_submit').html('添加');
		}else{
			this.$('.tx_submit').html('修改');
		}
		this.$('.errorHint').hide();

		var $count_min = this.$('#right_count_min');
		var $count_max= this.$('#right_count_max');
		$count_min.html('');
		$count_max.html('');
		for(var i=0; i<= this.problem_length; i++){
			$count_min.html($count_min.html()+'<option value="'+i+'">'+i+'</option>');
			$count_max.html($count_max.html()+'<option value="'+i+'">'+i+'</option>');
		}

		$("#content").val(this.prize.get('content'));
		$('#count').val(this.prize.get('count'));
		$('#right_count_min').val(this.prize.get('right_count_min'));
		$('#right_count_max').val(this.prize.get('right_count_max'));

		this.editor_content.setContent(this.prize.get('content_content'));
	},

	onSubmit: function() {
		var is_right = false;
		var count_min = $.trim(this.$editEl.find('#right_count_min').val());
		var count_max = $.trim(this.$editEl.find('#right_count_max').val());
		if(parseInt(count_min) > parseInt(count_max)){
			this.$('.error_right').html('最小值不能大于最大值');
			this.$('.error_right').show();
			is_right = true;
		}else{
			this.$('.error_right').hide();
			this.$('.error_right').html();
		}
		if(!is_right){
			for(var i = 0; i < this.right_nums.length; i++ ){
				if(this.right_nums[i] == count_min || this.right_nums[i] == count_max){
					is_right = true;
				}
			}
			if(is_right){
				this.$('.error_right').html('设置答对数量的范围，不能与其他的奖项重叠');
				this.$('.error_right').show();
			}else{
				this.$('.error_right').hide();
				this.$('.error_right').html();
			}
		}
		if (!W.validate($('#editorView-editPrizeDialog')) || is_right) {
			return;
		}

		this.prize.set('content', $.trim(this.editor_content.getContent()));
		this.prize.set('count', $.trim(this.$editEl.find('#count').val()));
		this.prize.set('right_count_min', count_min);
		this.prize.set('right_count_max', count_max);

		this.prize.set('content_content', $.trim(this.editor_content.getHtmlContent()));

		this.trigger(this.SUBMIT_SUCCESS_EVENT, this.prize);
	},

	afterClose: function() {
		this.unbind();
		this.editor_content.setContent('');
		this.$('#content, #count').val('');
		this.$('#right_count_min, #right_count_max').val(0);
	}
});

/**
 * 获得getEditprizeDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.question.getEditPrizeDialog = function(options) {
	var dialog = W.registry['EditPrizeDialog'];
	if (!options) {
		options = {};
	}
	options.width = options.width || 500;
	options.height = options.height || 400;

	if (!dialog) {
		//创建dialog
		xlog('create W.question.EditPrizeDialog');
		dialog = new W.question.EditPrizeDialog(options);
		W.registry['EditPrizeDialog'] = dialog;
	}
	return dialog;
};