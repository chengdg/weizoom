/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 问答奖品
 */

W.question.Prize = Backbone.Model.extend({
}, {
	idCounter: -99,
	index: 1,

	createNewPrize: function() {
		var id = this.idCounter;
		this.idCounter += 1;

		var prize = new W.question.Prize({
			id: id,
			right_count_min: 0,
			right_count_max: 0,
			content: "",
			count: "",
			content_content: ""
		});

		return prize;
	}
});


/**
 * 问答奖品
 */
W.question.Prizes = W.ApiCollection.extend({
	model: W.question.Prize,
	app: 'question',

	initialize: function(models, options) {
		this.items = null;
		this.questionId = -1;
	},

	url: function() {
		return this.getApiUrl('prizes/get/'+this.questionId);
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
