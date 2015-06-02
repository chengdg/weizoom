/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 问答奖品列表
 * @class
 */
W.question.PrizeListView = Backbone.View.extend({
	el: '',

	events: {
		'click .start_add_prize': 'onClickAddButton',
		'click .delete-prize-btn': 'onClickDeleteButton',
		'click .update-prize-btn': 'onClickUpdateButton'
	},

	getTemplate: function(){
		$('#question-prize-tmpl-src').template('question-prize-tmpl');
		return 'question-prize-tmpl';
	},

	getOnePrizeTemplate: function() {
		var name = 'one-prize-tmpl';
		$('#question-one-prize-tmpl-src').template(name);
		return name;
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.$prizesContainer = null;
		this.questionId=options.questionId;
		this.onePrize = null;
		this.indexCounter = -99;

		this.problem_length = 0; //题目数量
		this.right_nums=[];

		this.template = this.getTemplate();
		this.onePrizeTemplate = this.getOnePrizeTemplate();

		this.optionsDialog = {
			title: '编辑奖品题目',
			problem_length: this.problem_length,
			imageWidthAndHeight: {width: 70, height: 70},
			prize: null,
			state: 'create',
			right_nums: []
		}

		//创建编辑界面，绑定添加后刷新列表
		this.editPrizeDialog = W.question.getEditPrizeDialog(this.optionsDialog);

		//创建collection对象，绑定其add事件
		this.prizes = new W.question.Prizes();
		this.prizes.questionId = this.questionId;
		this.prizes.bind('add', this.onAdd, this);
		this.prizes.bind('change', this.onChange, this);
		this.prizes.fetch();
	},

	render: function() {
		this.$el.html($.tmpl(this.template));
		this.$prizesContainer = this.$('tbody');

		return this;
	},

	refresh: function(){
		this.prizes.fetch();
	},

	/**
	 * 接收到一条message时的响应函数
	 */
	onAdd: function(message) {
		this.$prizesContainer.append($.tmpl(this.onePrizeTemplate, message.toJSON()));
	},

	onChange: function(message){
		var $el = this.$('tr[prize_id="'+message.get('id')+'"]');
		$el.replaceWith($.tmpl(this.onePrizeTemplate, message.toJSON()));
	},

	/**
	 * 将一条消息从页面上移除
	 */
	removeOne: function(li) {
		li.remove();
	},

	submitDialog: function(data){
		W.getLoadingView().show();
		var id = (this.onePrize == null || this.onePrize =='' ? '-1' : this.onePrize.id);
		this.prizes.push(data);

		this.editPrizeDialog.close();
		W.getLoadingView().hide();
	},

	/**
	 * 点击"删除"链接的响应函数
	 */
	onClickDeleteButton: function(event) {
		var $el = this.$el.find(event.target);
		var $tr = $el.parents('tr');
		var prizeId = $tr.attr('prize_id');
		this.trigger('finish-submit-message');
		this.removeOne($tr);
		var remove_models = null;
		this.prizes.each(function(model) {
			if(model.get('id') == prizeId){
				remove_models = model;
				return;
			}
		});
		this.prizes.remove(remove_models);

		event.stopPropagation();
		event.preventDefault();
	},

	onClickAddButton: function(event){
		event.stopPropagation();
		event.preventDefault();
		this.trigger('get-problem-length');
		var right_nums = []
		this.prizes.each(function(model){
			right_nums.push(model.get('right_count_min'));
			right_nums.push(model.get('right_count_max'));
		});

		this.onePrize = null;
		this.optionsDialog.prize = new W.question.Prize.createNewPrize();
		this.optionsDialog.prize.set('id',++this.indexCounter)
		this.optionsDialog.problem_length = this.problem_length;
		this.optionsDialog.state = 'create';
		this.optionsDialog.right_nums = right_nums;

		this.editPrizeDialog.show(this.optionsDialog);
		this.editPrizeDialog.unbind(this.editPrizeDialog.SUBMIT_SUCCESS_EVENT);
		this.editPrizeDialog.bind(this.editPrizeDialog.SUBMIT_SUCCESS_EVENT, function(data) {
			this.submitDialog(data);
		},this);
	},

	onClickUpdateButton: function(event){
		var $el = $(event.currentTarget);
		var id = $el.parents('tr').attr('prize_id');
		var prizes = this.prizes.models;
		var prize = null;
		$.each(prizes,function(idx,item){
			if(item.id==id){
				prize = item;
			}
		});

		this.trigger('get-problem-length');

		var right_nums = []
		this.prizes.each(function(model){
			if(model != prize){
				right_nums.push(model.get('right_count_min'));
				right_nums.push(model.get('right_count_max'));
			}
		});

		this.onePrize = prize;
		this.optionsDialog.prize = prize
		this.optionsDialog.problem_length = this.problem_length;
		this.optionsDialog.state = 'update';
		this.optionsDialog.right_nums = right_nums;

		this.editPrizeDialog.show(this.optionsDialog);
		this.editPrizeDialog.unbind(this.editPrizeDialog.SUBMIT_SUCCESS_EVENT);
		this.editPrizeDialog.bind(this.editPrizeDialog.SUBMIT_SUCCESS_EVENT, function(data) {
			this.submitDialog(data);
		},this);

		event.stopPropagation();
		event.preventDefault();
	}
});