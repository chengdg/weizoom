
W.alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

ensureNS('W.view.market_tools.test_game');
W.view.market_tools.test_game.TestOptionsListView = Backbone.View.extend({
	initialize: function (options) {
		this.$el = $(options.el);
		this.template = this.getTemplate();
		this.deleteView = W.getItemDeleteView ();
		this.isAddOne = options.isAddOne || false;
	},
	getTemplate: function() {
		$('#test-option-tmpl-src').template('test-option-tmpl');
        return 'test-option-tmpl';
	},
	getOneTemplate: function() {
		$('#one-test-option-tmpl-src').template('one-test-option-tmpl');
        return 'one-test-option-tmpl';
	},
	getAnswerTemplate: function() {
		$('#answer-test-option-tmpl-src').template('answer-test-option-tmpl');
        return 'answer-test-option-tmpl';
	},
	render: function() {
		var $el = $.tmpl(this.template);
		this.$container = this.$el.find('tbody');
		if (this.isAddOne) {
			this.$container.append($el);
		}
	},
	events: {
		'click .ua-addAnswer': 'addAnswer',
		'click .ua-deleteAnswer': 'deleteAnswer',
		'click .ua-deleteQuestion': 'deleteQuestion',
		'click .ua-addQuestion':  'addQuestion'
	},
	addAnswer: function(event) {
		var $el = $(event.currentTarget);
		var $container = $el.parents('td:eq(0)').find('.ua-answer-box');
		var answerCount = $container.find('.answer-box').length;
		var title = W.alphabets[answerCount];
		var index = $el.parents('tr:eq(0)').find('.ua-questionIndex').text();
		$container.append($.tmpl(this.getAnswerTemplate(), {title: title, index: index}));
	},
	deleteAnswer: function(event) {
		var $el = $(event.currentTarget).parents('.answer-box:eq(0)');
		var $container = $el.parents('.ua-answer-box:eq(0)');
		this.deleteView.bind(this.deleteView.SUBMIT_EVENT, function(){
			var $titles = $container.find('.ua-answerTitle');
			if ($titles.length===1){
				W.getErrorHintView().show('必须有一个选项！');
				return false;
			}
			$el.remove();
			this.updateAnswer($container);
			this.deleteView.hide()
		}, this);
		var is_delete = this.deleteView.show({
			$action: $(event.currentTarget),
			info: '确定删除？'
		})
		
	},
	updateAnswer: function($container) {
		var $titles = $container.find('.ua-answerTitle');
		for (var i=0; i<$titles.length; i++){
			$($titles[i]).html(W.alphabets[i]);
		}
		var index = $container.parents('tr:eq(0)').find('.ua-questionName').attr('name').split('_')[3]
		
		var names = $container.find('.ua-answerName');
		for (var i=0; i<names.length; i++){
			$(names[i]).attr('name', 'test_game_answer_'+index+'_'+W.alphabets[i]);
		}
		var scores = $container.find('.ua-answerScore');
		for (var i=0; i<scores.length; i++){
			$(scores[i]).attr('name', 'test_game_answer_score_'+index+'_'+W.alphabets[i]);
		}
	},
	deleteQuestion: function(event) {
		var $el = $(event.currentTarget);
		this.deleteView.bind(this.deleteView.SUBMIT_EVENT, function(){
			var questionTitles = this.$el.find('.ua-questionIndex');
			if (questionTitles.length===1) {
				W.getErrorHintView().show('必须有一个问题！');
				return false;
			}
			$el.parents('tr').remove();
			this.updateQuestion();
			this.deleteView.hide()
		}, this);
		var is_delete = this.deleteView.show({
			$action: $el,
			info: '确定删除？'
		})
		
	},
	updateQuestion: function() {
		var questionTitles = this.$el.find('.ua-questionIndex');
		for (var i=0; i<questionTitles.length; i++){
			$(questionTitles[i]).html(i+1);
		}
		var questions = this.$el.find('.ua-questionName');
		for (var i=0; i<questions.length; i++){
			$(questions[i]).attr('name', 'test_game_question_'+(i+1));
			var $container = $(questions[i]).parents('tr').find('.ua-answer-box:eq(0)');
			this.updateAnswer($container);
		}
	},
	addQuestion: function() {
		var index = this.$el.find('.ua-questionIndex').length + 1;
		this.$container.append($.tmpl(this.getOneTemplate(), {index: index}))
	}
})