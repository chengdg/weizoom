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
		'keypress .xa-app-add': 'onPressEnter',
		'click .xa-mistiness': 'onClickMistinessRadio',
		'click .xa-exact': 'onClickExactRadio',
		'click .xa-appendSubmit': 'onClickSubmit',
		'click .xa-cancel': 'onClickClose'
	},

	initialize: function(options) {
        this.md = "精确匹配";
        this.type = 0;
        this.template = Handlebars.compile($("#addkey-view-tmpl-src").html());
		this.prize_keypress_num = 0;
		this.prize_keypress_arr =[];
		//this.$add_keyword_btn = $(options.add_btn);
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
			this.prize_keypress_num += 1;
			this.prize_keypress_arr.push(this.prize_keypress_num);
			////this.$el.unbind();
			//prize_keypress_num += 1;
			////替换相邻多个空格为一个
			//if(prize_keypress_num==1){
			//var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');
			//if(keyword == '') {
			//	this.$('.xa-errorHint').html('关键字不能为空！');
			//	return;
			//}
            //
			//if(keyword.length > 15) {
			//	this.$('.xa-errorHint').html('单个关键词字数不能超过15个字');
			//	return;
			//}
			//
			//var keywords = [];
			//$('#' + this.id).find($('.xa-editeTable .data-keyword')).each(function(){
			//	keywords.push($(this).text().trim());
			//});
			//this.$el.find($('.data-keyword')).each(function(){
			//	keywords.push($(this).text().trim());
			//});
            //
			////判断关键词个数是否超过10个
			//if (keywords.length > (10 - 1)) {
			//	W.showHint('error', '关键词个数不能超过10个');
			//	return;
			//}
            //
			//var args = {
			//	keyword: keyword,
			//	keywords: JSON.stringify(keywords)
			//};
			//console.log('---------------');
            //
            //var _this = this;
			//console.log(_this);
			//var pattern = {
			//			keyword: _this.$('.xa-app-add').val(),
			//			mode: _this.md,
			//			type: _this.type
			//		};
			//var key_el = $('.xui-propertyView-app-ReplyGroup .propertyGroup_property_horizontalField .propertyGroup_property_input span');
            //
			////$('.xa-keywords').append(_this.template(pattern));
            //
			//	key_el.append(_this.template(pattern));
			//	_this.$('.xa-app-add').val("");
			//}
			//console.log(prize_keypress_num);
		console.log(this.prize_keypress_num);
		console.log(this.prize_keypress_arr);
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
		var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');

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
		
		var args = {
			keyword: keyword,
			keywords: JSON.stringify(keywords)
		};
	    var _this = this;
		//W.getApi().call({
		//	app: 'new_weixin',
		//	resource: 'keyword_rules',
		//	method: 'get',
		//	args: args,
		//	success: function(data) {
		//		var pattern = {
		//			keyword: _this.$('.xa-app-add').val(),
		//			mode: _this.md,
		//			type: _this.type
		//		};
		//		if(data.msg == null) {
		//			_this.$('.xa-keywords').append(_this.template(pattern));
		//			var temp = _this.$el.find('.xa-keywords').html();
		//			$('#' + _this.id).find('.xa-hint').hide();
		//			$('#' + _this.id).find('.xa-patternapend').append(temp);
		//			_this.hide();
		//		}
		//		else{
		//			_this.$('.xa-errorHint').html(data.msg);
		//			_this.$('.xa-errorHint').show();
		//			_this.$('.xa-app-add').attr("value","");
		//		}
		//		_this.$el.find($('.xa-app-add')).val('');
		//	},
		//	error: function(resp) {
		//		_this.$el.find($('.xa-app-add')).val('');
		//	}
		//})
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