/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 问答题目列表
 * @class
 */
W.question.ProblemListView = Backbone.View.extend({
	el: '',

	events: {
		'click .start_add_problem': 'onClickAddButton',
		'click .delete-problem-btn': 'onClickDeleteButton',
		'click .update-problem-btn': 'onClickUpdateButton'
	},

	getTemplate: function(){
		$('#question-problem-tmpl-src').template('question-problem-tmpl');
		return 'question-problem-tmpl';
	},

	getOneProblemTemplate: function() {
		var name = 'one-problem-tmpl';
		$('#question-one-problem-tmpl-src').template(name);
		return name;
	},

	/*在拖动时，拖动行的cell（单元格）宽度会发生改变。在这里做了处理就没问题了*/
	storHelper: function(e, ui) {
		ui.children().each(function() {
			$(this).width($(this).width());
		});
		return ui;
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.$problemsContainer = null;
		this.questionId=options.questionId;
		this.oneProblem = null;
		this.indexCounter = -99;

		this.template = this.getTemplate();
		this.oneProblemTemplate = this.getOneProblemTemplate();

		this.optionsDialog = {
			title: '编辑问答题目',
			imageWidthAndHeight: {width: 70, height: 70},
			problem: null,
			state: 'create'
		}
		//排序顺序
		this.sortedProblemIds = [];
		//创建编辑界面，绑定添加后刷新列表
		this.editProblemDialog = W.question.getEditProblemDialog(this.optionsDialog);

		//创建collection对象，绑定其add事件
		this.problems = new W.question.Problems();
		this.problems.questionId = this.questionId;
		this.problems.bind('add', this.onAdd, this);
		this.problems.bind('change', this.onChange, this);
		this.problems.fetch();
	},

	render: function() {
		this.$el.html($.tmpl(this.template));
		this.$problemsContainer = this.$('tbody');

		//拖动排序
		this.$el.find("tbody").css({cursor:'move'});
		this.$el.find("tbody").sortable({
			axis: 'y',
			helper: this.storHelper,
			stop: _.bind(function(options) {
				this.sortedProblemIds = this.submitForSort();
			}, this)
		}).disableSelection();

		return this;
	},

	refresh: function(){
		this.problems.fetch();
	},

	/**
	 * 接收到一条message时的响应函数
	 */
	onAdd: function(message) {
		this.sortedProblemIds.push(message.get('id'));
		this.$problemsContainer.append($.tmpl(this.oneProblemTemplate, message.toJSON()));
	},

	onChange: function(message){
		var $el = this.$('tr[problem_id="'+message.get('id')+'"]');
		$el.replaceWith($.tmpl(this.oneProblemTemplate, message.toJSON()));
	},

	/**
	 * 将一条消息从页面上移除
	 */
	removeOne: function(li) {
		li.remove();
	},

	submitForSort: function() {
		var sortedCategoryIds = [];
		this.$("tbody tr").each(function() {
			var id = $(this).attr("problem_id");
			sortedCategoryIds.push(id);
		});
		return sortedCategoryIds;
	},

	submitDialog: function(data){
		W.getLoadingView().show();
		var id = (this.oneProblem == null || this.oneProblem =='' ? '-1' : this.oneProblem.id);
		this.problems.push(data);

		this.editProblemDialog.close();
		W.getLoadingView().hide();
	},

	/**
	 * 点击"删除"链接的响应函数
	 */
	onClickDeleteButton: function(event) {
		event.stopPropagation();
		event.preventDefault();
		var $el = $(event.target);
		var $tr = $el.parents('tr');
		var problemId = $tr.attr('problem_id');
		this.trigger('finish-submit-message');
		this.removeOne($tr);
		var remove_model = null;
		this.problems.each(function(model) {
			if(model.get('id') == problemId){
				remove_model = model;
			}
		});
		var sorted_ids = [];
		for(var i=0; i<this.sortedProblemIds.length; i++){
			if(problemId!=this.sortedProblemIds[i]){
				sorted_ids.push(this.sortedProblemIds[i]);
			}
		}
		this.sortedProblemIds = sorted_ids;
		this.problems.remove(remove_model);
	},

	onClickAddButton: function(event){
		event.stopPropagation();
		event.preventDefault();

		this.oneProblem = null;
		this.optionsDialog.problem = new W.question.Problem.createNewProblem();
		this.optionsDialog.problem.set('id',this.indexCounter--);
		this.optionsDialog.state = 'create';

		this.editProblemDialog.show(this.optionsDialog);
		this.editProblemDialog.unbind(this.editProblemDialog.SUBMIT_SUCCESS_EVENT);
		this.editProblemDialog.bind(this.editProblemDialog.SUBMIT_SUCCESS_EVENT, function(data) {
			this.submitDialog(data);
		},this);
	},

	onClickUpdateButton: function(event){
		var $el = $(event.currentTarget);
		var id = $el.parents('tr').attr('problem_id');
		var problems = this.problems.models;
		var problem = null;
		$.each(problems,function(idx,item){
			if(item.id==id){
				problem = item;
			}
		});

		this.oneProblem = problem;
		this.optionsDialog.problem = problem
		this.optionsDialog.state = 'update';

		this.editProblemDialog.show(this.optionsDialog);
		this.editProblemDialog.unbind(this.editProblemDialog.SUBMIT_SUCCESS_EVENT);
		this.editProblemDialog.bind(this.editProblemDialog.SUBMIT_SUCCESS_EVENT, function(data) {
			this.submitDialog(data);
		},this);

		event.stopPropagation();
		event.preventDefault();
	}
});