/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 自定义菜单列表
 * @class
 */
W.customerMenu.EditCustomerMenuItemView = Backbone.View.extend({
	el: '',

	events: {
		'click #add-menu-btn': 'onAddButton',
		'click #update-menu-btn': 'onUpdateButton',
		'change #type': 'onTypeChange',

//		'input input[id="name"]': 'onChangeName',
//		'change select[id="type"]': 'onChangeType',
		'change select[id="qa_rule_id"]': 'onChangeRuleId',
//		'input input[id="url"]': 'onChangeUrl'
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.$form = this.$el.find("form");
		this.fatherId = options.fatherId || 0;

		//初始化输入控件
		this.$nameInput = this.$('input[id="name"]');
		this.$typeInput = this.$('select[id="type"]');
		this.$ruleIdInput = this.$('select[id="qa_rule_id"]');
		this.$urlInput = this.$('input[id="url"]');
		this.keyWords = [];

		this.loadingKeyWords();
	},

	onAddButton: function(event){
		if (!W.validate()) {
			return false;
		}
		this.item.set('name', this.$nameInput.val());
		this.item.set('type', this.$typeInput.val());
		this.item.set('url', this.$urlInput.val());
		this.item.set('rule_id', this.$ruleIdInput.val());
		this.trigger('end_create_item', this.item);
	},

	onUpdateButton: function(){
		if (!W.validate()) {
			return false;
		}
		console.log('修改后的item', this.item);

		this.item.set('name', this.$nameInput.val());
		this.item.set('type', this.$typeInput.val());
		this.item.set('url', this.$urlInput.val());
		this.item.set('rule_id', this.$ruleIdInput.val());
		this.trigger('end_update_item', this.item);
	},

	onTypeChange: function(event){
		var $type = $(event.target);
		var value = parseInt($type.val());
		if(value === W.customerMenu.CustomerMenu.KEYWORD_TYPE){//关键词
			this.$el.find('#urlDiv').hide();
			this.$el.find('#qaRuleIdDive').show();
			this.$el.find('#url').attr("data-validate", "");
			this.$el.find('#qa_rule_id').attr("data-validate", "require-select-valid-option");
		}else{//链接
			this.$el.find('#qaRuleIdDive').hide();
			this.$el.find('#urlDiv').show();
			this.$el.find('#url').attr("data-validate", "url");
			this.$el.find('#qa_rule_id').attr("data-validate", "");
		}
		this.$urlInput.val("");
		this.$ruleIdInput.val(-1);
		this.$('.previewMessage').hide()
	},
	/**
	 * 显示form
	 */
	showForm: function(options) {
		if(options.item != null && parseInt(options.item.get('type')) === W.customerMenu.CustomerMenu.LINK_TYPE){
			this.showLinkView();
		}else {
			this.showKeyWordView();
		}
		this.item = options.item || W.customerMenu.CustomerMenu.createKeyWordMessage();
		this.fatherId = options.fatherId || 0;
		this.item.set("father_id", this.fatherId);
		this.$form.show();
		this.resetForm(options.item);
		this.getPreviewShow(this.item.get("rule_id"));

		console.log('开始的item', this.item);
	},

	showKeyWordView: function(){
		this.$el.find('#urlDiv').hide();
		this.$el.find('#qaRuleIdDive').show();
		this.$el.find('#url').attr("data-validate", "");
		this.$el.find('#qa_rule_id').attr("data-validate", "require-select-valid-option");
	},

	showLinkView: function(){
		this.$el.find('#qaRuleIdDive').hide();
		this.$el.find('#urlDiv').show();
		this.$el.find('#url').attr("data-validate", "url");
		this.$el.find('#qa_rule_id').attr("data-validate", "");
	},

	resetForm: function(item){
		if(item){
			this.$nameInput.val(item.get('name'));
			this.$typeInput.val(item.get('type'));
			this.$ruleIdInput.val(item.get('rule_id'));
			this.$urlInput.val(item.get('url'));
			this.$el.find('#add-menu-btn').hide();
			this.$el.find('#update-menu-btn').show();
			this.$el.find('legend').html(' 修改菜单项:');
		}else{
			this.$nameInput.val("");
			this.$typeInput.val(0);
			this.$ruleIdInput.val(-1);
			this.$urlInput.val("");
			this.$el.find('#add-menu-btn').show();
			this.$el.find('#update-menu-btn').hide();
			this.$el.find('legend').html(' 添加菜单项:');
			this.$el.find('#nameDiv span.help-block').html('一级菜单可输入4个字符！');
			this.$el.find('#nameDiv input[id="name"]').attr('data-validate-max-length', 4);
		}

		if(this.fatherId == 0){
			this.$el.find('#nameDiv span.help-block').html('一级菜单可输入4个字符！');
			this.$el.find('#nameDiv input[id="name"]').attr('data-validate-max-length', 4);
		}else{
			this.$el.find('#nameDiv span.help-block').html('二级菜单可输入7个字符！');
			this.$el.find('#nameDiv input[id="name"]').attr('data-validate-max-length', 7);
		}
		this.$el.find('#nameDiv input[id="name"]').attr('data-validate', 'required');
	},
	/**
	 * name输入框内容改变的响应函数
	 */
	onChangeName: function() {
		this.item.set('name', this.$nameInput.val());
	},

	/**
	 * type输入框内容改变的响应函数
	 */
	onChangeType: function() {
		this.item.set('type', this.$typeInput.val());
		console.log('修改type', this.item.get('type'), this.item);
	},

	/**
	 * url输入框内容改变的响应函数
	 */
	onChangeUrl: function() {
		this.item.set('url', $.trim(this.$urlInput.val()));
		console.log('修改url', this.item.get('url'), this.item);
	},

	/**
	 * qa_rule_id输入框内容改变的响应函数
	 */
	onChangeRuleId: function() {
//		this.item.set('rule_id', this.$ruleIdInput.val());
		this.getPreviewShow(this.$ruleIdInput.val());
	},

	/**
	 * 隐藏form
	 */
	hideForm: function() {
		this.$el.find('#nameDiv input[id="name"]').attr('data-validate', '');
		this.$el.find('#customer-menu-form').hide();
	},
	/**
	 * 加载关键词
	 */
	loadingKeyWords: function(){
		var _this = this;
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'weixin/message/qa',
				api: 'keywords/get',
				method: 'post',
				success: function(data) {
					var $select_rule = _this.$el.find('#qa_rule_id');
					$select_rule.empty();
					this.keyWords = data.rules;
					if(data.rules.length > 0){
						$select_rule.append('<option selected="" value="-1">请选择</option>');
						for(var i = 0; i < data.rules.length; i++){
							$select_rule.append('<option value="'+data.rules[i].id+'">'+data.rules[i].patterns+'</option>');
						}
					}else{
						$select_rule.append('<option selected="" value="-1">还没有添加关键词</option>');
					}
					W.getLoadingView().hide();
				},
				error: function(response) {
					alert('添加素材失败');
					W.getLoadingView().hide();
				},
				scope: this
			});
		}, this);
		task.delay(100);
	},

	getKeyWordName: function(id){
		for(var i = 0; i < this.keyWords.length; i++){
			if(parseInt(this.keyWords[i].id) == id){
				return this.keyWords[i].patterns;
			}
		}
		return null;

	},

	getPreviewShow: function(rule_id){
		var phone = this.$('.previewMessage');
		if(rule_id > 0){
			W.getLoadingView().show();
			W.getApi().call({
				app: 'school',
				api: 'newses/get',
				method: 'post',
				args: {
					id: rule_id
				},
				success: function(data) {
					phone.html("");
					if(data.rule.type == 1){//文本
						phone.html(data.rule.answer);
					}else if(data.rule.type == 2){//图文
						phone.html("图文");
						var newses = data.newses;
						if (newses.length === 1) {
							var news = newses[0];
							var node = $.tmpl('single-news-tmpl', {
								news: news,
								enableEdit: true,
								enableDeleteMaterial: false
							}).removeClass('mt10');
							phone.html(node).show();
						} else {
							//multi_news
							var mainNews = newses[0];
							var subNewses = newses.slice(1);
							var node = $.tmpl('multi-newses-tmpl', {
								mainNews: mainNews,
								subNewses: subNewses,
								enableEdit: true,
								enableDeleteMaterial: false
							}).removeClass('mt10');
							phone.html(node).show();
						}
					}
					W.getLoadingView().hide();
				},
				error: function(response) {
//					alert('预览素材失败');
					phone.html("");
					W.getLoadingView().hide();
				},
				scope: this
			});
		}else{
			this.$('.previewMessage').html("");
		}

	}

});