/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信自定义菜单消息编辑器
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.MenuEditorPanel = Backbone.View.extend({
	el: '',

	events: {
		'click .xa-text': 'onClickTextMessageTab',
		'click .xa-news': 'onClickNewsMessageTab',
		'click .xa-url': 'onClickUrlMessageTab',
		'click .xa-changeNews': 'onClickChangeNewsLink',
		
		'input input[name="menuUrlDisplayValue"]': 'onChangeUrlDisplayValue',
	},

	getTemplate: function() {
		$('#weixin-menu-eidtor-panel-tmpl-src').template('weixin-menu-eidtor-panel-tmpl');
		return 'weixin-menu-eidtor-panel-tmpl';
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		//图文
		this.materialId = options.materialId || 0;
		this.material = options.material || null;
		//文本
		this.answer = options.answer || '';
		//跳转链接
		this.url = options.url || '';
		this.currentMenuId = options.currentMenuId || '';
		this.render();
		
		//选择内部链接
		this.menuLinkView = new W.view.weixin.MenuLinkView({
			el: this.$('.xa-urlMessageZone')
		});
		this.bind('customer-url-handler', this.handlerCustomerUrl);
		
		//创建富文本编辑器
		var width = this.$el.outerWidth();
		this.editor = new W.view.common.RichTextEditor({
			el: this.$el.find('textarea'),
			type: 'text',
			maxCount: 600,
			width: width
		});
		this.editor.setContent(this.answer);
		this.editor.render();
		
		this.editor.bind('contentchange', function() {
		 	this.trigger('custom-menu-change', this.editor.getContent(), 'text');
		}, this);
		this.$('.errorHint').hide();

		if(this.materialId > 0){
			//有material，显示图文消息
			this.displayNews(this.material);
		} else if (this.url) {
			// 修改链接
			this.menuLinkView.setEditHtml(this.url.toString(), true);
			this.$('.xa-url').tab('show');
		}
    },

    getCurrentMenuId: function(){
    	return this.currentMenuId
    },

    
    /**
	 * 处理外部链接
	 */
	handlerCustomerUrl: function(){
		this.menuLinkView.handlerCustomerUrl();
	},

	render: function() {
		var index = this.currentMenuId;
		var dataId = this.currentMenuId;
		if (!index) {
			index = $('.xui-i-menu-item').length;
		}
		var $editMaterialPage = $('.xui-editMaterialPage');
		var is_weizoom_mall = $editMaterialPage.attr('is_weizoom_mall');
		var is_certified_service = $editMaterialPage.attr('is_certified_service');
		this.$el.html($.tmpl(this.template, {index: index, is_weizoom_mall: is_weizoom_mall, is_certified_service: is_certified_service}));
		return this;
	},

	displayNews: function(material) {
		var newsView = new W.view.weixin.NewsView({
			material: material
		});
		var $el = newsView.render();
		var $newsMessageZone = this.$('.xa-newsMessageZone');
		$newsMessageZone.html($el);
		this.$('.xa-news').tab('show');
		
		var height = $newsMessageZone.height();
		if (height > 215) {
			$newsMessageZone.css('height', '215px');
			$newsMessageZone.css('overflow-y', 'auto');
			$newsMessageZone.css('overflow-x', 'hidden');
		} else {
			$newsMessageZone.css('height', 'auto');
			$newsMessageZone.css('overflow-y', 'hidden');
			$newsMessageZone.css('overflow-x', 'hidden');
		}
	},

	/**
	 * onClickTextMessageTab: 点击“文字”tab的响应函数 
	 */
	onClickTextMessageTab: function(){

		this.materialId = 0;
	},
	
	/**
	 * onClickUrlMessageTab: 点击“跳转链接”tab的响应函数 
	 */
	onClickUrlMessageTab: function(){
		this.materialId = 0;
	},

	/**
	 * onClickChangeNewsLink: 点击“更换”图文消息的链接
	 */
	onClickChangeNewsLink: function(event){
		this.onClickNewsMessageTab(event);
	},

	/**
	 * onClickNewsMessageTab: 点击“图文”tab的响应函数 
	 */
	onClickNewsMessageTab: function(event){
		event.stopPropagation();
		event.preventDefault();
		
		var _this = this;
		W.dialog.showDialog('W.dialog.weixin.SelectMaterialDialog', {
			materialId: this.materialId,
			success: function(data) {
				_this.material = data;
				_this.materialId = _this.material.id;
				_this.displayNews(_this.material);
				
				_this.trigger('custom-menu-change', _this.materialId, 'news');
			}
		})
	},
	
	onChangeUrlDisplayValue: function(event) {
		var $current = $(event.currentTarget);
		var value = $current.parent('div').find('#menuLinkTarget').val();
		if (!value || value.length == 0) {
			value = $current.val();
		}
		this.trigger('custom-menu-change', value, 'url');
	},

	getMenuModel: function(currentMenuId) {
		//alert(W.currentMenuId)
		var items = currentMenuId.toString().split('-');
		var model;
		if (items.length >= 2) {
			model = W.menuPhone.menubar.getMenuItem(parseInt(items[0]), parseInt(items[1]));
		} else {
			model = W.menuPhone.menubar.getMenu(parseInt(items[0]));
		}
		
		return model;
	},

	setContentData: function(currentId, content ,type){
		var model = this.getMenuModel(currentId);
		model.set('answer', {content: content, type: type});
		console.log('---set:',currentId,model.get('answer'))
	}
});