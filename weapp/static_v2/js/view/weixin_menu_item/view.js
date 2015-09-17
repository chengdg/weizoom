/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信消息编辑器
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.MenuItem = Backbone.View.extend({
	el: '',

	events: {
		'click .xa-edit-one-menu': 'onEditOneMenu',
		'click .xa-add-one-menu-item': 'onAddOneMenuItem',
		'click input[name="oneMenuText"]': 'onClickOneMenuText',
		'click input[name="oneMenuItemText"]': 'onClickOneMenuItemText',
		'input input[name="oneMenuText"]': 'onChangeOneMenuText',
		'input input[name="oneMenuItemText"]': 'onChangeOneMenuItemText',
	},

	getTemplate: function() {
		$('#weixin-menu-item-tmpl-src').template('weixin-menu-item-tmpl');
		return 'weixin-menu-item-tmpl';
	},
	
	getOneMenuItemTemplate: function() {
		$('#weixin-one-menu-item-tmpl-src').template('weixin-one-menu-item-tmpl');
		return 'weixin-one-menu-item-tmpl';
	},
	
	oneMenuHelper: function(event, ui) {
		ui.find('.xui-menu-left-item').css('width', '33.8%');
		return ui;
	},

	initialize: function(options) {
		if (options.el.length == 0) {
			this.$messageEl = $(options.messageEl);
			return;
		}
		this.$el = $(this.el);
		this.template = this.getTemplate();
		
		this.render();
		
		//动态设置右侧编辑框位置
		var $menuRightDiv = this.$el.find('.xui-menu-right-item');
        
        this.$el.delegate('.xa-close', 'click', _.bind(this.onCloseOneMenu, this));
        
        $( ".xui-one-menu-item div" ).css({cursor:'move'});
		$( ".xui-one-menu-item" ).sortable({
			axis: 'y',
			stop: _.bind(function(event, ui, options) {
				this.submitForOneMenuItemSort(ui.item.parents('.xui-i-menu-item'));
			}, this)
		});
		
		$( ".xui-i-menu-item" ).css({cursor:'move'});
		$( ".xui-i-menu" ).sortable({
			axis: 'y',
			helper: this.oneMenuHelper,
			stop: _.bind(function(event, ui, options) {
		        ui.item.find('.xui-menu-left-item').css('width', '20%');
				this.submitForOneMenuSort(ui.item);
			}, this)
		});
    },
    
	render: function() {
		this.$el.html($.tmpl(this.template, {}));
		return this;
	},
	
	onEditOneMenu: function(event) {
		$('input').attr('readonly', 'readonly');
		this.$('.xui-one-menu-item div').removeClass('active');
		
		var $menuDiv = this.$('.xui-one-menu');
		$menuDiv.addClass('active');
		var $input = $menuDiv.find('input');
    	$input.removeAttr("readonly");
    	$input.focus();
    },
    
	onAddOneMenuItem: function(event) {
    	var $current = $(event.currentTarget);
    	var $oneMenuItemDiv = this.$('.xui-one-menu-item');
    	var length = $oneMenuItemDiv.find('.form-control').length;
    	if (length >= 5) {
			W.showHint('error', '最多只能创建5个二级菜单！');
			return;
		}
    	$('input').attr('readonly', 'readonly');
    	this.$('.xui-menu-left-item div.active').removeClass('active');
    	
    	$oneMenuItemDiv.append($.tmpl(this.getOneMenuItemTemplate()));
		$oneMenuItemDiv.delegate('.xa-edit-one-menu-item', 'click', _.bind(this.onEditOneMenuItem, this));
		$oneMenuItemDiv.delegate('.xa-del-one-menu-item', 'click', _.bind(this.onDelOneMenuItem, this));
		$oneMenuItemDiv.delegate('input', 'input',  _.bind(this.onChangeOneMenuItemText, this));
		
		var $lastOneMenuItemDiv = $oneMenuItemDiv.find('div:last');
		var $input = $lastOneMenuItemDiv.find('input');
		$input.val((length + 1) + '.标题');
		$lastOneMenuItemDiv.addClass('active');
		$input.removeAttr('readonly');
		$input.focus();
		
		var menuId = parseInt(this.$('.xui-one-menu').find('input').attr('data-menu-id'));
		if (W.menuPhone.menubar.activeMenuId !== menuId) {
			W.menuPhone.menubar.selectMenu(menuId);
		}
		var itemId = W.menuPhone.menubar.addNewMenuItemTo(menuId);
		var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + menuId + '"]');
		if ($menuItem.find('img').length === 0) {
			$menuItem.prepend('<img src="/static_v2/img/weixin/menu_item.png" class="mr5 mb3">');
		}
		$input.attr('data-menu-id', itemId);
		W.menuPhone.menubar.getMenuItem(menuId, itemId).set('name', $input.val());
		
		this.submitForOneMenuItemSort($oneMenuItemDiv.parents('.xui-i-menu-item'));
		
		this.changeEditMessagePanel($lastOneMenuItemDiv, 2);
    },
    
    onEditOneMenuItem: function(event) {
    	$('input').attr('readonly', 'readonly');
    	this.$('.xui-menu-left-item div.active').removeClass('active');
    
    	var $oneMenuItemDiv = $(event.currentTarget).parent('div');
    	var $input = $oneMenuItemDiv.find('input');
    	$input.removeAttr("readonly");
		$oneMenuItemDiv.addClass('active');
    	$input.focus();
	},
	
	onDelOneMenuItem: function(event) {
		this.$('.xui-menu-left-item div.active').removeClass('active');
		
		var $current = $(event.currentTarget)
		
		var $oneMenuItemDiv = $current.parent('div');
		var $oneMenuItemPanel = $oneMenuItemDiv.parents('.xui-one-menu-item');
		var $prevMenuItemDiv = $oneMenuItemDiv.prev();
		if ($prevMenuItemDiv.length > 0) {
			$prevMenuItemDiv.addClass('active');
		} else {
			var $oneMenuDiv = $current.parents('.xui-menu-left-item').find('.xui-one-menu');
			$oneMenuDiv.addClass('active');
		}
		$oneMenuItemDiv.remove();
		
		if ($prevMenuItemDiv.length > 0) {
			this.changeEditMessagePanel($prevMenuItemDiv, 2);
		} else {
			this.changeEditMessagePanel($oneMenuDiv, 1);
		}
		
		var menuId = parseInt(this.$('.xui-one-menu').find('input').attr('data-menu-id'));
		var itemId = parseInt($oneMenuItemDiv.find('input').attr('data-menu-id'));
		var menuItem = W.menuPhone.menubar.getMenuItem(menuId, itemId);
	
		if (W.menuPhone.menubar.activeMenuId !== menuId) {
			W.menuPhone.menubar.selectMenu(menuId);
		}
		W.menuPhone.menubar.deleteMenu(menuItem);
		if ($oneMenuItemPanel.find('div').length <= 0) {
			W.menuPhone.menubar.$menuItemContainer.hide();
			var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + menuId + '"]');
			$menuItem.find('img').remove();
		}
	},
	
	onCloseOneMenu: function(event) {
    	var $oneMenuItemDiv = $(event.currentTarget).parents('.xui-i-menu-item');
    	$oneMenuItemDiv.remove();
    	
        var $lastOneMenuItemDiv = $(".xui-i-menu-item:last");
        if ($lastOneMenuItemDiv.length > 0) {
        	var top = $lastOneMenuItemDiv.offset().top;
        	if (top + 260 <= 810) {
        		$('.xui-i-editor-panel').css('height', 810);
        	} else {
        		$('.xui-i-editor-panel').css('height', top + 260);
        	}
        }
    	
    	var menuId = parseInt(this.$('.xui-one-menu').find('input').attr('data-menu-id'));
		var menu = W.menuPhone.menubar.getMenu(menuId);
		
		W.menuPhone.menubar.deleteMenu(menu);
		if (W.menuPhone.menubar.activeMenuId !== menuId) {
			W.menuPhone.menubar.selectMenu(W.menuPhone.menubar.activeMenuId);
		} else {
			W.menuPhone.menubar.activeMenuId = null;
		}
		var menuData = W.menuPhone.getMenuData();
		$.each(menuData, function(i, n) {
			if (n.items.length > 0) {
				var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + n.id + '"]');
				$menuItem.prepend('<img src="/static_v2/img/weixin/menu_item.png" class="mr5 mb3">');
			}
		});
	},
	
	onChangeOneMenuText: function(event) {
		var $current = $(event.currentTarget);
		
		var menuId = parseInt($current.attr('data-menu-id'));
		W.menuPhone.menubar.getMenu(menuId).set('name', $current.val());
	},
	
	onChangeOneMenuItemText: function(event) {
		var $current = $(event.currentTarget);
		
		var menuId = parseInt(this.$('.xui-one-menu').find('input').attr('data-menu-id'));
		var itemId = parseInt($current.attr('data-menu-id'));
		W.menuPhone.menubar.getMenuItem(menuId, itemId).set('name', $current.val());
		if (W.menuPhone.menubar.activeMenuId !== menuId) {
			W.menuPhone.menubar.selectMenu(menuId);
		}
	},
	
	onClickOneMenuItemText: function(event) {
		var $current = $(event.currentTarget);

		//this.$('.xa-no-panel').removeClass('xui-editCover')
		$current.parents('.xui-i-menu-item').find('.xa-no-panel').removeClass('xui-editCover');
		if ($current.attr('readonly')) {
			$('.xa-menu-content').html('<label class="xui-i-unvalid">点击左侧编辑</label>')
			$('input').attr('readonly', 'readonly');
	    	this.$('.xui-menu-left-item div.active').removeClass('active');
			
			var $oneMenuItemDiv = $current.parent('div');

			$oneMenuItemDiv.addClass('active');
			console.log('active-class:',$oneMenuItemDiv)
			this.changeEditMessagePanel($oneMenuItemDiv, 2);
		}
	},
	
	onClickOneMenuText: function(event) {
		var _this = this;
		var $current = $(event.currentTarget);
    	var $oneMenuItemDiv = this.$('.xui-one-menu-item');
    	var length = $oneMenuItemDiv.find('.form-control').length;

    	if (length > 0) {
			$('.xa-no-panel').addClass('xui-editCover').html('点击左侧编辑');
			
			//$('.xa-menu-content').html('<label class="xui-i-unvalid">点击左侧编辑</label>')
		} else {
			$('.xa-no-panel').removeClass('xui-editCover')
			$('.xa-no-panel').text('')
		}
		//$current.parents('.xui-i-menu-item').find('.xa-no-panel').removeClass('xui-editCover');
		if ($current.attr('readonly')) {
			//$('.xa-menu-content').html('<label class="xui-i-unvalid">点击左侧编辑</label>')
			$('input').attr('readonly', 'readonly');
	    	_this.$('.xui-menu-left-item div.active').removeClass('active');
			//$current.parents('.xui-i-menu-item').find('.xa-no-panel').removeClass('xui-editCover');
			//var $menuDiv = _this.$('.xui-one-menu');
			var $menuDiv = $current.parents('.xui-i-menu-item').find('.xui-one-menu');
			$menuDiv.addClass('active');
			
			_this.changeEditMessagePanel($menuDiv, 1);
		}
	},
	
	addPhoneNewses: function(materialId, material) {
	//	alert(W.currentMenuId+':addPhoneNewses')
        var menuEditor = new W.view.weixin.MenuEditorPanel({
	        el: this.$('#edit-message-panel'),
	        materialId: materialId,
	        material: material,
	        currentMenuId: W.currentMenuId
	    });
	    this.bindMenuEditorHandler(menuEditor);
	},
	
	addPhoneUrl: function(url) {
		//alert(W.currentMenuId+':addPhoneUrl')
        var menuEditor = new W.view.weixin.MenuEditorPanel({
	        el: this.$('#edit-message-panel'),
	        url: url,
	        currentMenuId: W.currentMenuId
	    });
	    //alert('addPhoneUrl')
	    this.bindMenuEditorHandler(menuEditor);
	},
	
	addPhoneText: function(answer) {
		var $messageEl;
		if (this.$messageEl && this.$messageEl.length > 0) {
			$messageEl = this.$messageEl;
		} else {
			$messageEl = this.$('#edit-message-panel');
		}
		//alert(W.currentMenuId+':addPhoneText')
        var menuEditor = new W.view.weixin.MenuEditorPanel({
	        el: $messageEl,
	        answer: answer,
	        currentMenuId: W.currentMenuId
	    });
	    this.bindMenuEditorHandler(menuEditor);
	},
	
	addMenuItem: function(menuItem) {
		//添加一级菜单
		
		var $oneMenuDiv = this.$('.xui-one-menu');
		
		var $input = $oneMenuDiv.find('input');
		$input.attr('data-menu-id', menuItem.id);
		$input.val(menuItem.name);
		
		var $editMessagePanel = this.$('#edit-message-panel');
		$editMessagePanel.attr('index', menuItem.index);
		//添加二级菜单
		var length = menuItem.items ? menuItem.items.length : 0;
		if (length > 0) {
			//$editMessagePanel.html('<label class="xui-i-unvalid">使用二级菜单后主回复已失效</label>');
			
	       	var $oneMenuItemDiv = this.$('.xui-one-menu-item');
	        for (var i = 0; i < length; ++i) {
		    	$oneMenuItemDiv.append($.tmpl(this.getOneMenuItemTemplate()));
	        	var oneMenuItem = menuItem.items[i]
				var $lastMenuItemDiv = $oneMenuItemDiv.find("div:last");
				var $input = $lastMenuItemDiv.find('input');
				$input.val(oneMenuItem.name);
				$input.attr('data-menu-id', oneMenuItem.id)
				
				$lastMenuItemDiv.delegate('.xa-edit-one-menu-item', 'click', _.bind(this.onEditOneMenuItem, this));
				$lastMenuItemDiv.delegate('.xa-del-one-menu-item', 'click', _.bind(this.onDelOneMenuItem, this));
	        }
		} else {
	    	this.changeEditMessagePanel($oneMenuDiv, 1);
	    }
	},

	validateItem: function(){
		var data = W.menuPhone.getMenuData();
		var tipType = -1;
		var tipId = -1;
		// 提交数据前判断类型是url的内容未以http://开头，自动添加http://开头
		$.each(data, function(i, n) {
			if (tipType !== -1) {
				return false;
			}
			tipId = n.id;
			if (n.name.length == 0 && tipType == -1) {
				tipType = 0;
				return false;
			}
			if (n.answer.type === 'text' && n.answer.content.length > 600){
				tipType = 2;
				return false;
			}

			if (n.items.length == 0 && n.answer.content.length == 0) {
				tipType = 4;
				return false;
			}
			n.name = W.getString().cut(n.name, 16, 0);
			$.each(n.items, function(j, m) {
				tipId = m.id;
				if (m.name.length == 0 && tipType == -1) {
					tipType = 1;
					return false;
				}
				if (m.answer.type === 'text' && m.answer.content.length > 600){
					tipType = 3;
					return false;
				}
				if (m.answer.content.length == 0) {
					tipType = 5;
					return false;
				}
				m.name = W.getString().cut(m.name, 40, 0);
				/*
				if(m.answer && m.answer.type === 'url' && m.answer.content.indexOf('http://') === -1) {
					m.answer.content = 'http://'+m.answer.content;
				}
				*/
			});
		});
		this.$('input').attr('readonly', 'readonly');
		var $input = $('input[data-menu-id="' + tipId + '"]');
		var $inputParentDiv = $input.parent('div');
		var $menuItemDiv = $inputParentDiv.parents('.xui-i-menu-item');
		var $editMessagePanel = $menuItemDiv.find('#edit-message-panel');
		$menuItemDiv.find('.xui-menu-left-item div.active').removeClass('active');
		$inputParentDiv.addClass('active');
		$input.focus();
		var menuItem = new W.view.weixin.MenuItem({el: '', messageEl: $editMessagePanel});
		if (tipType === 0) {
			W.showHint('error', '一级菜单不能为空');
			menuItem.changeEditMessagePanel($inputParentDiv, 1);
			return false;
		} else if (tipType === 1) {
			W.showHint('error', '二级菜单不能为空');
			menuItem.changeEditMessagePanel($inputParentDiv, 2);
			return false;
		} else if (tipType === 2 || tipType === 3) {
			W.showHint('error', '内容不能超过600字');
			menuItem.changeEditMessagePanel($inputParentDiv, tipType - 1);
			var $iframe = $editMessagePanel.find('iframe');
			var tid = setInterval(function() {
				var $iframeBody = $iframe.contents().find('body');
				if ($iframeBody.length > 0) {
					$iframeBody.css('overflow-y', 'auto');
					$iframeBody.css('height', '184px');
					
					clearInterval(tid);
				}
			}, 100); 
			
			return false;
		} else if (tipType === 4 || tipType === 5) {
			W.showHint('error', '回复内容不能为空');
			menuItem.changeEditMessagePanel($inputParentDiv, tipType - 3);
			
			return false;
		}
		return true;
	},
	
	submitForOneMenuSort: function($oneMenuDiv) {
		var $oneMenuItemDiv = $oneMenuDiv.parents('.xui-i-menu').find('.xui-i-menu-item');
		$oneMenuItemDiv.each(function(index){
			var oneMenuId = parseInt($(this).find('.xui-one-menu input').attr('data-menu-id'));
			var newIndex = index + 1;
			W.menuPhone.menubar.getMenu(oneMenuId).set('index', newIndex);
		});
		W.menuPhone.menubar.hideMenuItems();
		W.menuPhone.menubar.refresh();
		var menuData = W.menuPhone.getMenuData();
		$.each(menuData, function(i, n) {
			if (n.items.length > 0) {
				var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + n.id + '"]');
				$menuItem.prepend('<img src="/static_v2/img/weixin/menu_item.png" class="mr5 mb3">');
			}
		});
		
		$('input[name="menuUrlDisplayValue"]').removeAttr('readonly');
	},
	
	submitForOneMenuItemSort: function($oneMenuItemDiv) {
		var menuId = parseInt($oneMenuItemDiv.find('.xui-one-menu input').attr('data-menu-id'));
		var $oneMenuItemDiv = $oneMenuItemDiv.find('.xui-one-menu-item div');
		var length = $oneMenuItemDiv.length;
		$oneMenuItemDiv.each(function(index){
			var itemId = parseInt($(this).find('input').attr('data-menu-id'));
			var newIndex = length - index;
			W.menuPhone.menubar.getMenuItem(menuId, itemId).set('index', newIndex);
		});
		
		W.menuPhone.menubar.selectMenu(menuId);
	},
	
	displayEditMessagePanel: function(menu) {
		var menuContent = menu.answer.content;
    	var menuType = menu.answer.type;
    	
    	var _this = this;
    	
    	$('#edui_fixedlayer').remove();
    	//alert('1'+menuType)
    	if (menuType === 'news') {
	    	W.getLoadingView().show();
			W.resource.new_weixin.MenuMaterial.get({
				data: {
					id: menu.answer.content
				},
				success: function(data) {
					W.getLoadingView().hide();
			    	var material = {'id': menu.answer.content, 'newses': data.items}
			    	_this.addPhoneNewses(menu.id, material);
				},
				error: function(resp) {
					W.getLoadingView().hide();
					alert('加载菜单数据失败!');
				}
			});
		} else if (menuType === 'url') {
			var content = menuContent;
			if (content.indexOf('"data":') <= 0) {
				content = '{"data": "' + menuContent + '", "workspace": "custom", "data_category":"外部链接"}';
			}
			_this.addPhoneUrl(content);
		} else {
			_this.addPhoneText(menuContent);
		}
	},
	
	changeEditMessagePanel: function($menuDiv, menuType) {
    	var menuId = parseInt($menuDiv.parents('.xui-menu-left-item').find('.xui-one-menu input').attr('data-menu-id'));
    	W.currentMenuId = menuId;
    	var menu;
    	// 一级菜单
    	if (menuType === 1) {
    		var $menuItemPanel = $menuDiv.parents('.xui-i-menu-item');
    		var $editMessagePanel = $menuItemPanel.find('#edit-message-panel');
	    	if ($menuItemPanel.find('.xui-one-menu-item div').length > 0) {
	    		//$editMessagePanel.html('<label class="xui-i-unvalid">使用二级菜单后主回复已失效</label>')
	    	} else {
	    		menu = W.menuPhone.menubar.getMenu(menuId).toJSON();
	    	}
    	} else if (menuType === 2) {
    		var itemId = parseInt($menuDiv.find('input').attr('data-menu-id'));
			W.currentMenuId = W.currentMenuId + '-' + itemId;
	    	menu = W.menuPhone.menubar.getMenuItem(menuId, itemId).toJSON();
	    	//console.log(menu)
    	}
    	if (menu) {
    		this.displayEditMessagePanel(menu);
    	}
	},
	
	getMenuModel: function() {
		//alert(W.currentMenuId)
		var items = W.currentMenuId.toString().split('-');
		var model;
		if (items.length >= 2) {
			model = W.menuPhone.menubar.getMenuItem(parseInt(items[0]), parseInt(items[1]));
		} else {
			model = W.menuPhone.menubar.getMenu(parseInt(items[0]));
		}
		
		return model;
	},
	
	bindMenuEditorHandler: function(menuEditor) {
		//var _this = this;
		var currentId = menuEditor.getCurrentMenuId()
		menuEditor.bind("custom-menu-change", function(content, type) {
			if (type === 'text') {
				var $iframeBody = this.$('iframe').contents().find('body');
				if ($iframeBody.css('overflow-y') != 'auto') {
					if ($iframeBody.css('height') === '184px') {
						$iframeBody.css('overflow-y', 'auto');
					}
					$iframeBody.css('height', '184px');
				}
			}
			//var menuId = parseInt(menuEditor.$el.parents('.xui-menu-left-item').find('.xui-one-menu input').attr('data-menu-id'));
			//alert(menuId)
			//console.log("menuEditor:",menuEditor.$el.find('.xa-menu-content').attr('data-id'))
				//find('.xa-menu-content').attr('dat.fa-id'))
			//console.log("menuEditor:")
			//W.currentMenuId = menuEditor.$el.find('.xa-menu-content').attr('data-id')
			 
			//alert(W.currentMenuId+':bindMenuEditorHandler')
			console.log(W.currentMenuId,'==',menuEditor.getCurrentMenuId(), '==',currentId)
			//if (W.currentMenuId==menuEditor.getCurrentMenuId()) {
			//	var model = menuEditor.getMenuModel(currentId);
		//		model.set('answer', {content: content, type: type});
		//		console.log('---set:',currentId,model.get('answer'))
			if(W.currentMenuId == currentId){
				menuEditor.setContentData(currentId, content, type);
				}
			//}
			
		});
	},
});