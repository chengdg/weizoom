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

	events: {
		'keypress .xa-app-add': 'onPressEnter',
		'click .xa-mistiness': 'onClickMistinessRadio',
		'click .xa-exact': 'onClickExactRadio',
		'click .xa-cancel': 'onClickClose'
	},

	templates: {
		viewTmpl: "#apps-prize-keywordpane-src",
		badgeTmpl: "#apps-prize-badge-src"
	},

	initialize: function(options) {
		$('body').append(this.renderTmpl('viewTmpl', {}));
		this.$el = $(options.el);
		this.$component_el = options.component_el;
        this.type = "accurate";

		this.$add_keyword_btn = $(options.add_keyword_btn);
		this.xx= 0;
		this.yy= 0;
		this.keywords_obj = options.keywords || {};
		this.render();
		var that = this;
		this.$component_el.delegate('.xa-close', 'click', function(){
			var need_removed_key = $(this).parent().siblings().find('.data-keyword').attr('data-keyword');
			$(this).parent().parent().remove();
			delete that.keywords_obj[need_removed_key];
			this.trigger('add_keywords', that.keywords_obj);
		});
	},
	render: function() {
		var badgeHtml = this.renderTmpl('badgeTmpl', {keywords: this.keywords_obj});
		this.$add_keyword_btn.siblings().remove();
		$(badgeHtml).insertBefore(this.$add_keyword_btn);
	},

	onPressEnter: function (e) {
		if (e.keyCode == 13) {
			var _this = this;
			//判断关键词个数是否超过8个
			var i_length=0;
			for(var i in this.keywords_obj){
				i_length++;
			}
			if (i_length >=8){
				W.showHint('error', '关键词个数不能超过8个');
				return;
			}
			//替换相邻多个空格为一个
			var keyword = this.$('.xa-app-add').val();
			if(keyword == '') {
				W.showHint('error','关键字不能为空！');
				return;
			}
			if(keyword.length > 5) {
				W.showHint('error','单个关键词字数不能超过5个字');
				return;
			}

			//关键字·组_检查
			//var keywords = [];//关键字组
			//var keywords_obj = [];//关键字组对象
			//this.$add_keyword_div.find('.xa-data-patterns').each(function(){
			//	var key_tmp = $(this).find('.data-keyword').text().replace(/\n/g,'').replace(/\r/g,'').replace(/\r\n/g,'').replace(/\s+/g, '').trim();
			//	var mode_tmp = $(this).find('.xa-data-type').attr('data-type').trim();
			//	keywords.push(key_tmp);
			//	keywords_obj.push({'keyword':key_tmp,'mode':mode_tmp});
			//});

			this.keywords_obj[_this.$('.xa-app-add').val()] = _this.type;

			this.trigger('add_keywords', this.keywords_obj);
			this.$('.xa-app-add').val('');
			this.render();
		}

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
		var offset = this.$add_keyword_btn.offset();
		this.$el.css('position','absolute');
		this.$el.css('top', offset.top+50 + 'px');
		this.$el.css('left', offset.left+100 + 'px');
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	}
});


W.registerUIRole('[data-ui-role="apps-prize-keyword-pane"]', function() {
    var $el = $(this);
	var view = $el.data('view') || void 0;
	if(view) return;
	W.getApi().call({
        app: 'apps/sign',
        resource: 'sign',
        method: 'get',
		async: false,
        args: {},
        success: function(data){
			view = new W.view.apps.PrizeKeywordPane({
				el:'.xa-keywordBoxDiv-v2',
				add_keyword_btn:'.xa-add-keyword-btn',
				keywords: data,
				component_el: $el
			});
			$el.data('view', view);
        },
        error: function(error){
            W.showHint('error', '获取关键字配置失败~');
        }
    });

	$(this).delegate('.xa-add-keyword-btn', 'click', function(){
		view.show();
	});

});