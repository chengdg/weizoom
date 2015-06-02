/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * CustomerMenu编辑面板
 * @class
 */

W.customerMenu.EditCustomerMenuPanel = Backbone.View.extend({
	el: '',

	events: {
		'click #submit-btn': 'onSubmitNews'
	},

	getTemplate: function(){
		$('#edit-customer-menu-view-tmpl-src').template('edit-customer-menu-view-tmpl');
		return 'edit-customer-menu-view-tmpl';
	},

	initialize: function(options) {
		this.submitCount = 0;
		this.$el = $(this.el);
		this.isActive = options.isActive;
		this.webappId = options.webappId;
		this.app = options.app || 'school';
		this.runType = options.runType || '';

		this.template = this.getTemplate();

		this.$el.html($.tmpl(this.template, {
			patterns: this.patterns,
			showPattern: this.showPattern
		}));

		this.listMenu = new W.customerMenu.EditListCustomerMenuView({
			el: '#list-customer-menu-box',
			isActive: this.isActive
		});
		this.listMenu.bind('onAddStart', this.onAddStart, this);
		this.listMenu.bind('start_update_item', function(item) {
			xlog('start_update_item')
			this.menuItem.showForm({
				fatherId: item.get('father_id'),
				item:item
			});
		}, this);
		//删除后隐藏form表单
		this.listMenu.bind('end_delete_item', function(item) {
			xlog('end_delete_item')
			this.menuItem.hideForm();
		}, this);



		this.menuItem = new W.customerMenu.EditCustomerMenuItemView({
			el: '#customer-menu-editor-box'
		});
		this.menuItem.bind('end_create_item', this.onAddButton, this);
		this.menuItem.bind('end_update_item', this.onUpdateButton, this);

		//初始化微信消息
		var itemCount = options.items ? options.items.length : 0;
		for (var i = 0; i < itemCount; ++i) {
			var item = options.items[i];
			var itemMessage = W.customerMenu.CustomerMenu.createKeyWordMessage();
			itemMessage.set(item);
			this.listMenu.addItem(itemMessage);
		}
	},

	render: function(){
		//创建html
		return this;
	},

	onAddStart: function(fatherId){
		this.menuItem.showForm({
			fatherId: fatherId,
			item:null
		});
	},

	onAddButton: function(item){
		this.listMenu.addItem(item);
		this.menuItem.hideForm();
	},

	onUpdateButton: function(item){
		this.listMenu.updateItem(item);
		this.menuItem.hideForm();
	},

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmitNews: function(event) {
		if (!W.validate()) {
			return false;
		}
		if(this.submitCount === 0){
			this.submitItem();
		}
		this.submitCount += 1;
	},

	submitItem: function(){
		W.getLoadingView().show();
		var _this = this;
		var items = this.listMenu.getNewCreatedItems();
		var task = new W.DelayedTask(function() {
			/**
			 * 如果为“test”为测试环境，就不与微信做交互，方便测试
			 */
			if(_this.runType == 'test'){
				_this.fetchLocalDataApi(items);
				return;
			}
			_this.sendInteractiveAPI(items);
		}, this);
		task.delay(100);
	},

	getDataItem: function(item){
		var itemData = {};
		if(parseInt(item.get('type')) == 1){
			itemData.type = 'click';
			itemData.key = this.menuItem.getKeyWordName(item.get('rule_id'));
		}else{
			itemData.type = 'view';
			itemData.url = item.get('url');
		}
		itemData.name = item.get('name').trim();
		return itemData;
	},

	getMenuItemJson: function(){
		var menu_json = {button: []};
		var _this = this;
		var menus = this.listMenu.menus;
		var $one = $('li[data-id="0"] > ul > li');
		if(this.$("#isAllActive").attr('checked') ? true : false){
			console.log('启用', menus)
			$one.each(function() {
				var id = $(this).attr('data-id');
				var first_item = menus.get(id);
				if(parseInt(first_item.get("is_active")) == 1){
					var size = 0;
					var sub_button = [];
					$(this).find('li').each(function() {
						id = $(this).attr('data-id');
						var second_item = menus.get(id);
						if(parseInt(second_item.get("is_active"), 10) === 1){
							size += 1;
							sub_button.push(_this.getDataItem(second_item));
						}
					});
					if(size > 0){
						console.log('有子菜单');
						menu_json.button.push({name: first_item.get('name').trim(),sub_button:sub_button})
					}else{
						console.log('没有子菜单',_this.getDataItem(first_item));
						menu_json.button.push(_this.getDataItem(first_item));
					}
				}
			});
		}else{
			xlog('全部不启用')
		}
		console.log("menu_json", menu_json);
		return menu_json;
	},

	/**
	 * 发送与微信api交互请求
	 */
	sendInteractiveAPI: function(items){
		var _this = this;
		var menu_json = this.getMenuItemJson();
		/*
		var menu_json = {button: []};
		if(this.$("#isAllActive").attr('checked') ? true : false){
			console.log('启用', this.listMenu.menus)
			$.each(this.listMenu.menus.models,function(idx,item){
				var father_id = parseInt(item.get("id"), 10);
				if(parseInt(item.get("father_id")) == 0 && parseInt(item.get("is_active")) == 1){
					var size = 0;
					var sub_button = [];
					$.each(_this.listMenu.menus.models,function(idx,item){
						if(parseInt(item.get("father_id"), 10) == father_id && parseInt(item.get("is_active"), 10) === 1){
							size += 1;
							sub_button.push(_this.getDataItem(item));
						}
					});
					if(size > 0){
						console.log('有子菜单');
						menu_json.button.push({name: item.get('name').trim(),sub_button:sub_button})
					}else{
						console.log('没有子菜单',_this.getDataItem(item));
						menu_json.button.push(_this.getDataItem(item));
					}
				}
			});
		}else{
			xlog('全部不启用')
		}
		console.log("menu_json", menu_json);*/
		W.getApi().call({
			app: 'tools',
			api: 'customerized_menu/update',
			method: 'post',
			args: {
				menu_json: JSON.stringify(menu_json)
			},
			success: function(data) {
				_this.fetchLocalDataApi(items);
			},
			error: function(response) {
				alert('操作失败，请稍后重试，或联系客户人员！');
				W.getLoadingView().hide();
				this.submitCount = 0;
			},
			scope: this
		});
	},

	/**
	 * 发送本地存储请求
	 */
	fetchLocalDataApi: function(items){
		var app = this.app;
		var api = 'update_local';
		var itemData = JSON.stringify(items);
		var delete_ids = this.listMenu.getDeletedItemIds();

		W.getApi().call({
			app: app,
			api: api,
			method: 'post',
			args: {
				delete_ids: delete_ids,
				data: itemData
			},
			success: function(data) {
				W.getErrorHintView().show('更新菜单成功！');
				W.getLoadingView().hide();
				window.location.href = '/'+app;
			},
			error: function(response) {
				alert('添加菜单项失败');
				W.getLoadingView().hide();
			},
			scope: this
		});
	}


});