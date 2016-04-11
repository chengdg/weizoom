/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.apps');
W.view.apps.PrizeKeywordPane = Backbone.View.extend({
	el: '',
	add_keyword_btn:'',
	page_keywords:'',

	templates: {
		viewTmpl: "#apps-prize-keywordpane-src",
		badgeTmpl: "#apps-prize-badge-src"
	},

	initialize: function(options) {

		if(!$('.xa-keywordBoxDiv-v2')[0]){
			$('body').append(this.renderTmpl('viewTmpl', {}));
			this.$el = $(options.el);
			this.$el.find('.xa-add-single-keyword').on('click', _.bind(this.onAddKeyword, this));
			this.$el.find('.xa-mistiness').on('click', _.bind(this.onClickMistinessRadio, this));
			this.$el.find('.xa-exact').on('click', _.bind(this.onClickExactRadio, this));
			this.$el.find('.xa-cancel').on('click', _.bind(this.onClickClose, this));
		}
		this.$el = $(options.el);

        this.type = "accurate";
		this.keyword_btn = options.add_keyword_btn;

		this.keywords_obj = options.keywords || {};
		//this.render();
	},

	updateData: function(data){
		if(W.weixinKeywordObj) {
			this.keywords_obj = W.weixinKeywordObj;
			this.render();
			return;
		}
		this.keywords_obj = data;
		W.weixinKeywordObj = data;
		this.render();
	},

	render: function(data) {
		this.$add_keyword_btn = $(this.keyword_btn);
		data = data || this.keywords_obj;
		var badgeHtml = this.renderTmpl('badgeTmpl', {keywords: data});
		this.$add_keyword_btn.siblings().remove();
		$(badgeHtml).insertBefore(this.$add_keyword_btn);
		this.trigger('add_keywords', data);
	},

	delegateCloseSingleBadge: function($component_el){
		var that = this;
		$component_el.delegate('.xa-close', 'click', function(){
			var need_removed_key = $(this).parent().siblings().find('.data-keyword').attr('data-keyword');
			delete that.keywords_obj[need_removed_key];
			W.weixinKeywordObj = that.keywords_obj;
			that.render();
		});
	},

	onAddKeyword: function () {
		var _this = this;
		//判断关键词个数是否超过8个
		var i_length=0;
		for(var i in this.keywords_obj){
			i_length++;
		}
		if (i_length >=8){
			W.showHint('error', '关键词个数不能超过8个');
			return false;
		}
		//替换相邻多个空格为一个
		var keyword = this.$el.find('.xa-app-add').val();
		if(keyword == '') {
			W.showHint('error','关键字不能为空！');
			return false;
		}
		if(keyword.length > 5) {
			W.showHint('error','单个关键词字数不能超过5个字');
			return false;
		}
		if(keyword in this.keywords_obj){
			W.showHint('error','关键字不能重复');
			return false;
		}
		//检查关键字是否重复 has_duplicate_pattern
		W.getApi().call({
			app: 'new_weixin',
			resource: 'keyword_rules',
			method: 'get',
			args: {
				keyword: keyword
			},
			success: function(data){
				var msg = data.msg;
				if(msg && !$.isEmptyObject(msg)){
					W.showHint('error', msg);
				}else{
					_this.keywords_obj[keyword] = _this.type;
					W.weixinKeywordObj = _this.keywords_obj;
					_this.$el.find('.xa-app-add').val('');
					_this.render();
				}
			},
			error: function(error){
				W.showHint('error', '关键字重复性检查失败~');
			}
		});
	},

	onClickMistinessRadio: function() {
		this.type = "blur";
	},

	onClickExactRadio: function() {
		this.type = "accurate";
	},

	onClickClose: function() {
		this.hide();
	},

	show: function() {
		this.$add_keyword_btn = $(this.keyword_btn);
		var offset = this.$add_keyword_btn.offset();
		//this.$el.css('position','absolute');
		this.$el.css('top', offset.top+50 + 'px');
		this.$el.css('left', offset.left+50 + 'px');
		this.$el.css('display', 'block');
		this.$el.removeClass('xui-hide');
	},

	hide: function() {
		this.$el.hide();
	}
});


W.registerUIRole('[data-ui-role="apps-prize-keyword-pane"]', function() {
    var $el = $(this);
	var view = view = new W.view.apps.PrizeKeywordPane({
		el:'.xa-keywordBoxDiv-v2',
		add_keyword_btn:'.xa-add-badge-btn'
	});
	view.delegateCloseSingleBadge($el);
	$el.data('view', view);
	$(this).delegate('.xa-add-badge-btn', 'click', function(){
		view.show();
	});
	var that = this;
	W.getApi().call({
        app: 'apps/sign',
        resource: 'sign',
        method: 'get',
        args: {},
        success: function(data){
			view.updateData(data);
        },
        error: function(error){
            W.showHint('error', '获取关键字配置失败~');
        }
    });

});