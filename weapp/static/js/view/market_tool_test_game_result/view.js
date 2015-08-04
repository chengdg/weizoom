ensureNS('W.view.market_tools.test_game');
W.view.market_tools.test_game.testGameResultView= Backbone.View.extend({
	initialize: function (options) {
		this.$el = $(options.el);
		this.template = this.getTemplate();
		this.validateScore = false;
		this.judgeScore();
		this.count = 1;
		this.isAddOne = options.isAddOne || false;
	},
	getTemplate: function(options) {
		$('#test-game-result-tmpl-src').template('test-game-result-tmpl');
        return 'test-game-result-tmpl';
	},
	getOneTemplate: function(options) {
		$('#one-test-game-result-tmpl-src').template('one-test-game-result-tmpl');
        return 'one-test-game-result-tmpl';
	},
	events: {
		'click .ua-addTestGameResult': 'addTestGameResult',
		'blur .ua-score': 'judgeScore',
		'click .btn-deleteResult': 'deleteResult'
	},
	deleteResult: function(event) {
		var $el = $(event.currentTarget);
		var deleteView = W.getItemDeleteView ();
		deleteView.bind(deleteView.SUBMIT_EVENT, function(){
			if ($('.result-box').length===1){
				W.getErrorHintView().show('必须有一个结果！');
				return false;
			}
			$el.parents('.result-box:eq(0)').remove();
			deleteView.hide();
		}, this);
		var is_delete = deleteView.show({
			$action: $(event.currentTarget),
			info: '确定删除？'
		})
	},
	judgeScore: function() {
		var $scores = $('.ua-score')
		var v = true;
		for (var i=0; i<$scores.length; i+=2){
			var f1 = parseInt($($scores[i]).val());
			var s1 = parseInt($($scores[i+1]).val());
			if (f1>s1){
				v = false;
			} else {
				if ($scores.length>3){
					for (var j=0; j<$scores.length; j+=2) {
						if (i!=j){
							var f2 = parseInt($($scores[j]).val());
							var s2 = parseInt($($scores[j+1]).val());
							if (f1>f2){
								if (!(s1>s2 && s1>f2 && s2<f1)){
									v = false;
								}
							} else {
								if (f1!=f2){
									if (!(s1<s2 && s1<f2 && s2>f1)) {
										v = false;
									}
								}
							}
						}
					}
				} else{
					v = true;
				}
			}
		}
		this.validateScore = v;
	},
	addTestGameResult: function() {
		var index = this.$container.find('textarea').length + 1;
		this.count += 1;
		var oneTemplate = this.getOneTemplate();
		var $el = $.tmpl(oneTemplate, {index: index, id: this.count});
		this.$container.append($el);
		var $textarea = $el.find('textarea');
		var editor = new W.view.common.RichTextEditor({
            el: $textarea.get(),
            type: 'full',
            width: 422,
            height: 180,
            autoHeight:false,
            imgSuffix: "uid="+W.uid,
            wordCount: false
        });
        editor.render();
	},
	render: function() {
		var $el = $.tmpl(this.template);
		this.$container = this.$el.find('.ua-results');
		if (this.isAddOne){
			this.$container.append($el);
		}
		this.count = this.$container.find('textarea').length;		
		
	},
})

