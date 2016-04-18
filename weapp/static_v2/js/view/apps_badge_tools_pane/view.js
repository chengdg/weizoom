/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.apps');
W.view.apps.BadgeToolsPane = Backbone.View.extend({
	el: '',
	templates: {
		viewTmpl: "#apps-badge-tools-pane-src",
		badgeTmpl: "#apps-badge-src"
	},

	initialize: function(options) {

		if(!$('.xa-badge-box')[0]){
			$('body').append(this.renderTmpl('viewTmpl', {}));
			this.$el = $(options.el);
			this.$el.find('.xa-add-badge').on('click', _.bind(this.onAddBadge, this));
			this.$el.find('.xa-cancel').on('click', _.bind(this.onClickClose, this));
		}
		this.$el = $(options.el);

		this.maxcount = options.maxcount; //可添加数量
		this.maxlen = options.maxlen; //名称最大长度

		this.add_btn = options.add_btn;

		this.badgeArr = options.keywords || [];
	},

	updateData: function(data){
		this.badgeArr = data;
		W.badgesData = data;
		this.render();
	},

	render: function() {
		var data, $add_btn = $(this.add_btn);
		if($.isEmptyObject(this.badgeArr)){
			data = W.badgesData;
			this.badgeArr = W.badgesData;
		}else{
			data = this.badgeArr;
		}
		var badgeHtml = this.renderTmpl('badgeTmpl', {badges: data});
		$add_btn.siblings().remove();
		$(badgeHtml).insertBefore($add_btn);

		this.trigger('add_badges', data);
	},

	delegateCloseSingleBadge: function($component_el){
		var that = this;
		$component_el.delegate('.xa-close', 'click', function(){
			var need_removed_key = $(this).parent().find('.data-keyword').attr('data-keyword');
			that.badgeArr.splice(that.badgeArr.indexOf(need_removed_key), 1);
			W.badgesData = that.badgeArr;
			that.render();
		});
	},

	onAddBadge: function () {
		var i_length = this.badgeArr.length;
		if (i_length >= this.maxcount){
			W.showHint('error', '关键词个数不能超过' + this.maxcount + '个');
			return false;
		}
		//替换相邻多个空格为一个
		var keyword = $.trim(this.$el.find('.xa-app-add').val());
		if(keyword == '') {
			W.showHint('error','关键字不能为空！');
			return false;
		}
		if(keyword.length > this.maxlen) {
			W.showHint('error','单个关键词字数不能超过' + this.maxlen + '个字');
			return false;
		}
		if(keyword in this.badgeArr){
			W.showHint('error','关键字不能重复');
			return false;
		}
		this.badgeArr.push(keyword);
		W.badgesData = this.badgeArr;
		this.$el.find('.xa-app-add').val('');
		this.render();
	},

	onClickClose: function() {
		this.hide();
	},

	show: function() {
		var $add_btn = $(this.add_btn);
		var offset = $add_btn.offset();
		this.$el.css({
			'top': offset.top+50 + 'px',
			'left': offset.left+50 + 'px',
			'display': 'block',
			'z-index': 9999
		});
		this.$el.removeClass('xui-hide');
	},

	hide: function() {
		this.$el.hide();
	}
});


W.registerUIRole('[data-ui-role="apps-badge-tools-pane"]', function() {
    var $el = $(this);
	var view = new W.view.apps.BadgeToolsPane({
		el:'.xa-badge-box',
		add_btn:'.xa-add-badge-btn',
		maxcount: $el.attr('data-maxcount'),
		maxlen: $el.attr('data-maxlen')
	});
	view.delegateCloseSingleBadge($el);
	$el.data('view', view);
	$(this).delegate('.xa-add-badge-btn', 'click', function(){
		view.show();
	});
	var that = this;
	//初始化数据
	if(!W.badgesData || W.badgesData.length <= 0){
		W.getApi().call({
			app: 'apps/shvote',
			resource: 'shvote',
			method: 'get',
			args: {
				"record_id": W.activityId
			},
			success: function(data){
				view.updateData(data);
			},
			error: function(error){
				W.showHint('error', '获取关键字配置失败~');
			}
		});
	}else{
		view.render();
	}


});