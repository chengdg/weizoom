/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 问答题目
 */

W.question.Problem = Backbone.Model.extend({
}, {
	idCounter: -99,
	index: 1,

	createNewProblem: function() {
		var id = this.idCounter;
		this.idCounter += 1;

		var problem = new W.question.Problem({
			id: id,
			right_answer: "",
			title: "",
			right_feedback: "",
			error_feedback: "",
			title_content: "",
			right_feedback_content: "",
			error_feedback_content: ""
		});

		return problem;
	},
	getTitle:function(){
		return 'abc';
	}
});


/**
 * 问答题目
 */
W.question.Problems = W.ApiCollection.extend({
	model: W.question.Problem,
	app: 'question',

	initialize: function(models, options) {
		this.items = null;
		this.questionId = -1;
	},

	url: function() {
		return this.getApiUrl('problems/get/'+this.questionId);
	},

	parse: function(response){
		var data = response.data;
		if(!data) {
			return [];
		}
		this.items = data.items;
		return data.items;
	},

	getItems: function(){
		return this.items;
	}
});
