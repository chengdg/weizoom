/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.apps');
W.view.apps.PrizeKeyword = Backbone.View.extend({
	el: '',
	keyword_div:'',

	events: {
		'keypress .xa-app-add': 'onPressEnter',
		'click .xa-mistiness': 'onClickMistinessRadio',
		'click .xa-exact': 'onClickExactRadio',
		'click .xa-appendSubmit': 'onClickSubmit',
		'click .xa-cancel': 'onClickClose'
	},

	initialize: function(options) {
        this.md = "精确";
        this.type = 0;
        this.template = Handlebars.compile($("#apps-addkey-view-tmpl-src").html());
		this.$keyword_div = $(options.keyword_div);
		this.render();
	},
	render: function() {
		if (this.$('.xui-newKeyView').length === 0) {
			this.$el.append($('#apps-prize-keyword-tmpl-src').html());
		} else {
			$('.xui-keywordBoxDiv').css({'position':'absolute'});
			this.$el.find('.xa-keywords').empty();
			this.$el.show();
		}
	},

	onPressEnter: function (e) {
		if (e.keyCode == 13) {
			//替换相邻多个空格为一个
			var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');
			if(keyword == '') {
				W.showHint('error','关键字不能为空！');
				return;
			}

			if(keyword.length > 5) {
				W.showHint('error','单个关键词字数不能超过5个字');
				return;
			}

			var keywords = [];
			$('#' + this.id).find($('.xa-editeTable .data-keyword')).each(function(){
				keywords.push($(this).text().trim());
			});
			this.$el.find($('.data-keyword')).each(function(){
				keywords.push($(this).text().trim());
			});

			//判断关键词个数是否超过4个
			if (keywords.length > (4 - 1)) {
				W.showHint('error', '关键词个数不能超过4个');
				return;
			}

			var args = {
				keyword: keyword,
				keywords: JSON.stringify(keywords)
			};

            var _this = this;
			var pattern = {
						keyword: _this.$('.xa-app-add').val(),
						mode: _this.md,
						type: _this.type
					};
			//$('.xa-keywords').append(_this.template(pattern));
			this.$keyword_div.append(_this.template(pattern));
			_this.$('.xa-app-add').val("");
		}

	},

	onClickMistinessRadio: function() {
		this.md = "模糊";
		this.type = 1;
	},

	onClickExactRadio: function() {
		this.md = "精确";
		this.type = 0;
	},

	onClickSubmit: function(){

		var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');
		if(keyword == '') {
			W.showHint('error','关键字不能为空！');
			return;
		}

		if(keyword.length > 5) {
			W.showHint('error','单个关键词字数不能超过5个字');
			return;
		}

		var keywords = [];
		$('#' + this.id).find($('.xa-editeTable .data-keyword')).each(function(){
			keywords.push($(this).text().trim());
		});
		this.$el.find($('.data-keyword')).each(function(){
			keywords.push($(this).text().trim());
		});

		//判断关键词个数是否超过4个
		if (keywords.length > (4 - 1)) {
			W.showHint('error', '关键词个数不能超过4个');
			return;
		}

		var args = {
			keyword: keyword,
			keywords: JSON.stringify(keywords)
		};

		var _this = this;
		var pattern = {
					keyword: _this.$('.xa-app-add').val(),
					mode: _this.md,
					type: _this.type
				};
		//$('.xa-keywords').append(_this.template(pattern));
		this.$keyword_div.append(_this.template(pattern));
		_this.$('.xa-app-add').val("");
		this.hide();
	},

	onClickClose: function() {
		this.hide();
	},

	setId: function (id) {
		this.id = id;
	},

	setPos: function (offset) {
		this.$el.css('position','absolute');
		this.$el.css('top', offset.top + 'px');
		this.$el.css('left', offset.left + 'px');
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		 
		this.$el.find($('.errorHint')).hide();
		this.$el.find($('.xa-errorHint')).hide();
		this.$el.find($('.xa-app-add')).val('');
		this.$el.hide();
	}
});    