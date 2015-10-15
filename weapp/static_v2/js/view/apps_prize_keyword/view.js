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
        this.md = "精确匹配";
        this.type = "accurate";
        this.template = Handlebars.compile($("#apps-addkey-view-tmpl-src").html());
		this.$keyword_div = $(options.keyword_div);
		this.render();
		this.num = 0;
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
			this.num += 1;
			//替换相邻多个空格为一个
			var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');//关键字
			if(keyword == '') {
				W.showHint('error','关键字不能为空！');
				return;
			}
			if(keyword.length > 5) {
				W.showHint('error','单个关键词字数不能超过5个字');
				return;
			}

			//关键字·组_检查
			var keywords = [];//关键字组
			var keywords_obj = [];//关键字组对象
			$('#add_keyword_div').find('.xa-data-patterns').each(function(){
				var key_id = $(this).attr('id');
				var key_tmp = $(this).find('.data-keyword').text().replace(/\n/g,'').replace(/\r/g,'').replace(/\r\n/g,'').replace(/\s+/g, '').trim();
				var mode_tmp = $(this).find('.xa-data-type').attr('data-type').trim();
				keywords.push(key_tmp);
				keywords_obj.push({'id':key_id,'keyword':key_tmp,'mode':mode_tmp});
			});

			//判断关键词个数是否超过8个
			if (keywords.length > (8 - 1)) {
				W.showHint('error', '关键词个数不能超过8个');
				return;
			}
			//关键字重复检查
			for(var i=0;i<keywords.length;i++){
				if(keyword==keywords[i]){
					W.showHint('error','关键字不能重复！');
					return;
				}
			}

			//插入模板
            var _this = this;
			var pattern = {
						keyword: _this.$('.xa-app-add').val(),
						mode: _this.md,
						type: _this.type,
						id:_this.num
					};

			//_this.$keyword_div.append(_this.template(pattern));
			$(_this.template(pattern)).insertBefore($('#add_keyword_btn'));
			var xx = $('#add_keyword_btn').position().top+50;
			var offset={top:xx};
			_this.setPos(offset);
			_this.$('.xa-app-add').val("");
		}

	},

	onClickMistinessRadio: function() {
		this.md = "模糊匹配";
		this.type = "blur";
	},

	onClickExactRadio: function() {
		this.md = "精确匹配";
		this.type = "accurate";
	},

	onClickSubmit: function(){
		this.num += 1;
		//替换相邻多个空格为一个
		var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');//关键字
		if(keyword == '') {
			W.showHint('error','关键字不能为空！');
			return;
		}
		if(keyword.length > 5) {
			W.showHint('error','单个关键词字数不能超过5个字');
			return;
		}

		//关键字_组_检查
		var keywords = [];//关键字组
		var keywords_obj = [];//关键字组对象
		$('#add_keyword_div').find('.xa-data-patterns').each(function(){
			var key_id = $(this).attr('id');
			var key_tmp = $(this).find('.data-keyword').text().replace(/\n/g,'').replace(/\r/g,'').replace(/\r\n/g,'').replace(/\s+/g, '').trim();
			var mode_tmp = $(this).find('.xa-data-type').attr('data-type').trim();
			keywords.push(key_tmp);
			keywords_obj.push({'id':key_id,'keyword':key_tmp,'mode':mode_tmp});
		});

		//判断关键词个数是否超过8个
		if (keywords.length > (8 - 1)) {
			W.showHint('error', '关键词个数不能超过4个');
			return;
		}
		//关键字重复检查
		for(var i=0;i<keywords.length;i++){
			if(keyword==keywords[i]){
				W.showHint('error','关键字不能重复！');
				return;
			}
		}
		//插入模板
		var _this = this;
		var pattern = {
					keyword: _this.$('.xa-app-add').val(),
					mode: _this.md,
					type: _this.type,
					id:_this.num
				};

		$(_this.template(pattern)).insertBefore($('#add_keyword_btn'));
		var xx = $('#add_keyword_btn').position().top+50;
		var offset={top:xx};
		_this.setPos(offset);
		_this.$('.xa-app-add').val("");

		//关闭
		_this.hide();
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