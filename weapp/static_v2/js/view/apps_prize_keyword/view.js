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

	events: {
		'keypress .xa-add': 'onPressEnter',
		'click .xa-mistiness': 'onClickMistinessRadio',
		'click .xa-exact': 'onClickExactRadio',
		'click .xa-appendSubmit': 'onClickSubmit',
		'click .xa-cancel': 'onClickClose'
	},

	initialize: function(options) {
        this.md = "精确匹配";
        this.type = 0;
        this.template = Handlebars.compile($("#addkey-view-tmpl-src").html());
	},

	render: function() {
		if (this.$('.xui-newKeyView').length === 0) {
			this.$el.append($('#apps-prize-keyword-tmpl-src').html());
		} else {
			this.$el.show();
		}
	},

	onPressEnter: function (e) {
		if (e.keyCode == 13) {
			this.$('.xa-errorHint').html('');
			//替换相邻多个空格为一个
			var keyword = this.$('.xa-add').val().trim().replace(/\s+/g, ' ');
			if(keyword == '') {
				return;
			}

			if(keyword.length > 15) {
				W.showHint('error', '单个关键词字数不能超过15个字');
				return;
			}
			
			var keywords = [];
			$('#' + this.id).find($('.xa-editeTable .data-keyword')).each(function(){
				keywords.push($(this).text().trim());
			});
			this.$el.find($('.data-keyword')).each(function(){
				keywords.push($(this).text().trim());
			});

			//判断关键词个数是否超过10个
			if (keywords.length > (10 - 1)) {
				W.showHint('error', '关键词个数不能超过10个');
				return;
			}

			args = {
				keyword: keyword,
				keywords: JSON.stringify(keywords)
			};
		    var _this = this;
			W.getApi().call({
				app: 'new_weixin',
				resource: 'keyword_rules',
				method: 'get',
				args: args,
				success: function(data) {
					var pattern = {
						keyword: _this.$('.xa-add').val(),
						mode: _this.md,
						type: _this.type
					};
					if(data.msg == null) {
						_this.$('.xa-keywords').append(_this.template(pattern));
					} else {
						_this.$('.xa-errorHint').html(data.msg);
						_this.$('.xa-errorHint').show();
						_this.$('.xa-add').attr("value","");
					}
					_this.$el.find($('.xa-add')).val('');
				},
				error: function(resp) {
					_this.$el.find($('.xa-add')).val('');
				}
			})
		}
	},

	onClickMistinessRadio: function() {
		this.md = "模糊匹配";
		this.type = 1;
	},

	onClickExactRadio: function() {
		this.md = "精确匹配";
		this.type = 0;
	},

	onClickSubmit: function(){
		this.$('.xa-errorHint').html('');
		//替换相邻多个空格为一个
		var keyword = this.$('.xa-add').val().trim().replace(/\s+/g, ' ');

		if(keyword == '') {
			var temp = this.$el.find('.xa-keywords').html();
			$('#' + this.id).find('.xa-patternapend').append(temp);
			if(this.$el.find('.data-keyword').length == 0) {
				W.showHint('error', '关键词不能为空');
				return;
			}
			$('#' + this.id).find('.xa-hint').hide();
			this.hide();
			return;
		}

		if(keyword.length > 15) {
			W.showHint('error', '单个关键词字数不能超过15个字');
			return;
		}

		var keywords = [];
		$('#' + this.id).find($('.xa-editeTable .data-keyword')).each(function(){
			keywords.push($(this).text().trim());
		});
		this.$el.find($('.data-keyword')).each(function(){
			keywords.push($(this).text().trim());
		});

		//判断关键词个数是否超过10个
		if (keywords.length > (10 - 1)) {
			W.showHint('error', '关键词个数不能超过10个');
			return;
		}
		
		args = {
			keyword: keyword,
			keywords: JSON.stringify(keywords)
		};
	    var _this = this;
		W.getApi().call({
			app: 'new_weixin',
			resource: 'keyword_rules',
			method: 'get',
			args: args,
			success: function(data) {
				var pattern = {
					keyword: _this.$('.xa-add').val(),
					mode: _this.md,
					type: _this.type
				};
				if(data.msg == null) {
					_this.$('.xa-keywords').append(_this.template(pattern));
					var temp = _this.$el.find('.xa-keywords').html();
					$('#' + _this.id).find('.xa-hint').hide();
					$('#' + _this.id).find('.xa-patternapend').append(temp);
					_this.hide();
				}
				else{
					_this.$('.xa-errorHint').html(data.msg);
					_this.$('.xa-errorHint').show();
					_this.$('.xa-add').attr("value","");
				}
				_this.$el.find($('.xa-add')).val('');
			},
			error: function(resp) {
				_this.$el.find($('.xa-add')).val('');
			}
		})
	},

	onClickClose: function() {
		this.hide();
	},

	setId: function (id) {
		this.id = id;
	},

	setPos: function (offset) {
		this.$el.css('top', offset.top + 'px');
		this.$el.css('left', offset.left + 'px');
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		 
		this.$el.find($('.errorHint')).hide();
		this.$el.find($('.xa-errorHint')).hide();
		this.$el.find($('.xa-add')).val('');
		this.$el.hide();
	}
});    