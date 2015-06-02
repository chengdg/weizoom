/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 自定义菜单列表
 * @class
 */
W.customerMenu.EditListCustomerMenuView = Backbone.View.extend({
	el: '#list-customer-menu-box',

	events: {
		'click .customer_menu_add': 'onAddStart',
		'click .customer_menu_delete': 'onDeleteStart',
		'click .customer_menu_sort': 'onSort',
		'click span.name': 'onUpdateStart',
		'click input[name=isActive]': 'onChangeActive',
		'click #isAllActive': 'onChangeAllActive'
	},

	getTemplate: function(){
		$('#list-customer-menu-view-tmpl-src').template('list-customer-menu-view-tmpl');
		return 'list-customer-menu-view-tmpl'
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.isActive = options.isActive;


		this.template = this.getTemplate();
		this.$el.html($.tmpl(this.template, {
			isActive: this.isActive,
			patterns: this.patterns,
			showPattern: this.showPattern
		}));
		this.menus = new W.customerMenu.CustomerMenus();

		this.deleteIds = [];
	},

	onAddStart: function(event){
		event.stopPropagation();
		event.preventDefault();

		var fatherId = $(event.target).parents("li").attr('data-id');
		var size = 0;
		$.each(this.menus.models,function(idx,item){
			if(parseInt(item.get('father_id')) == fatherId){
				size += 1;
			}
		});
		if(parseInt(fatherId) == 0 && size == 3){
			W.getErrorHintView().show('一级菜单只能添加3个');
			$('form').hide();
		}else if(parseInt(fatherId) != 0 && size == 5){
			W.getErrorHintView().show('二级菜单只能添加5个');
			$('form').hide();
		}else{
			this.trigger('onAddStart', fatherId);
		}
	},

	getItem:function(item) {
		item = item || {};
		var checked = item.get("is_active")===1 ? 'checked="checked"' : '';

		var html = '<li data-id="'+ item.get('id') +'"><p class="zoom">\
					<span class="ico_arrow fl"></span>\
					<span class="name fl">'+item.get('name')+'</span>\
					<span class="fr mr10">\
					<span class="fl btnLay"><a href="javascript:void(0)" class="tx_sort btnAdd customer_menu_sort">↑</a></span>\
					<span class="checkbox fl"><input name="isActive" type="checkbox" '+checked+' value="checkbox"></span>\
					<span class="fl btnLay"><a href="javascript:void(0)" class="tx_add btnAdd customer_menu_add">+</a></span>\
					<span class="fl btnLay"><a href="javascript:void(0)" class="tx_delete btnDelete customer_menu_delete">×</a></span>\
					</span></p></li>';
		return html;
	},

	addItem: function(item){
		this.menus.push(item);
		var $parentLi = this.$el.find('li[data-id="'+item.get("father_id")+'"]');

		if(!$parentLi.find('ul').size()){
			$parentLi.append('<ul></ul>');
		}

		var html = this.getItem(item);
		$parentLi.children('ul').append(html);

		if(item.get("father_id") == 0){//一级
			xlog('一级')
		}else{  //二级
			$parentLi.find('li[data-id="'+item.get('id')+'"] .ico_arrow').hide();
			$parentLi.find('li[data-id="'+item.get('id')+'"] .tx_add').hide();
			$parentLi.find('p:first .tx_delete').hide();
			xlog('二级')
		}
		// 排序的显示状态
		this.updateSortStatus();
	},

	updateItem: function(item){
		var original_item = this.menus.get(item);
		original_item.set('name', item.get('name'));
		this.$el.find('li[data-id="'+item.get('id')+'"]>p>span.name').html(item.get('name'));
	},

	/**
	 * 获得数据
	 * @return {*}
	 */
	getNewCreatedItems: function() {
		console.log(11111,this.menus.toJSON());
		this.setDisplayIndex();
		return this.menus.toJSON()
	},
	/**
	 * 修改display顺序
	 */
	setDisplayIndex: function(){
		var $one = $('li[data-id="0"] > ul > li');
		var data = [];
		var first_index = 1,second_index = 1;
		var _this = this;
		$one.each(function() {
			var id = $(this).attr('data-id');
			var item = _this.menus.get(id);
			item.set('display_index', first_index);
			first_index ++;
			second_index = 1;
			$(this).find('li').each(function() {
				id = $(this).attr('data-id');
				item = _this.menus.get(id);
				item.set('display_index', second_index);
				second_index ++;
			});
		});
		xlog(this.menus);
	},

	onDeleteStart: function(event){
		event.stopPropagation();
		event.preventDefault();
		var _this = this;
		var $el = $(event.target);
		var deleteCommentView = W.getItemDeleteView();
		deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
			var $el = $(event.target);
			var id = $el.parents('li').attr('data-id');
			var item = _this.menus.get(id);
			_this.menus.remove(item);
			var parentUl =$el.parents('p').parent('li').parent('ul').parent('li');
			$el.parents('p').parent('li').remove();

			// 显示父类的删除按钮
			if(parentUl.find('li').size() == 0){
				parentUl.find('.customer_menu_delete').show();
			}
			if(id > 0){
				_this.deleteIds.push(id);
			}
			deleteCommentView.hide();
			_this.trigger('end_delete_item');
		}, this);

		deleteCommentView.show({
			$action: $el,
			info: '确定删除吗?'
		});
	},

	onUpdateStart: function(event){
		var $el = $(event.currentTarget);
		var id = $el.parents('li').attr('data-id');
		if(id != 0){
			var item = this.menus.get(id);
			this.trigger('start_update_item', item);
		}
	},

	updateSortStatus: function() {
		this.$('li[data-id="0"] > ul > li').each(function(i) {
			if(i === 0) {
				$(this).find('.tx_sort').css({display: 'none'});
			}else {
				$(this).find('.tx_sort').css({display: 'block'});
			}
			$(this).find('li').find('.tx_sort').css({display: 'block'});
			$(this).find('li').eq(0).find('.tx_sort').css({display: 'none'});
		});
	},

	/**
	 * 排序
	 * @param event
	 */
	onSort: function(event){
		var $ul = this.$('li[data-id="0"]>ul');
		var $el = $(event.currentTarget);
		var $currentLi = $el.parents('p').parent('li');
		var $prevLi = $currentLi.prev('li');
		$prevLi.before($currentLi);

		// 排序的显示状态
		this.updateSortStatus();
	},
	/**
	 * 获得删除的id集合
	 * @return {*}
	 */
	getDeletedItemIds: function() {
		return this.deleteIds.join(',')
	},
	/**
	 * 给变状态
	 * @param event
	 */
	onChangeActive: function(event){
		var $el = $(event.currentTarget);
		var id = $el.parents('p').parent('li').attr('data-id');
		var item = this.menus.get(id);
		item.set('is_active',item.get('is_active') === 1 ? 0 : 1);
	},
	/**
	 * 改变所以的状态
	 * @param event
	 */
	onChangeAllActive: function(event){
		xlog('onChangeAllActive')
		var $el = $(event.currentTarget);
		var isChicked = $el.attr('checked') ? true : false;
		this.$("input[name='isActive']").attr('checked', isChicked);
		$.each(this.menus.models,function(n,item) {
			item.set('is_active', isChicked ? 1 : 0);
		});
	}
});