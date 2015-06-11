/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.view.weixin');
W.view.weixin.MenuEditor = Backbone.View.extend({
	el: '',

	events: {
		'click #submit-btn': 'onSubmitCustomMenus',
		'click .xa-add-one-menu': 'onAddOneMenu',
		'click .xa-tab-custom-menu': 'onTabCustomMenu',
	},

    getTemplate: function(){
        $('#weixin-custom-menu-editor-tmpl-src').template('weixin-custom-menu-editor-tmpl');
        return 'weixin-custom-menu-editor-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        
        this.template = this.getTemplate();
        
        this.is_certified_service = $('.xui-editMaterialPage').attr('is_certified_service');
        this.$el.html($.tmpl(this.template, {status: options.status || '0', is_certified_service: this.is_certified_service}));

        /**
         * 初始化模拟器
         */
        this.phone = new W.view.weixin.EmbededPhoneView({
            el: this.$('.xa-simulator-box').get(),
            mode: 'action',
            menubarMode: 'nosort',
            enableAction: false,
            enableMenu: true,
            enableAddMenu: true
        });
        this.phone.render();
		W.menuPhone = this.phone;
		
		var _this = this;
		//加载菜单数据
		W.getLoadingView().show();
		W.resource.new_weixin.Menu.get({
			success: function(data) {
				W.getLoadingView().hide();
				_this.phone.addMenus(data);
				_this.initMenus(data);
				
		        var menuData = W.menuPhone.getMenuData();
				$.each(menuData, function(i, n) {
					if (n.items.length > 0) {
						var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + n.id + '"]');
						$menuItem.prepend('<img src="/static_v2/img/weixin/menu_item.png" class="mr5 mb3">');
					}
				});
			},
			error: function(resp) {
				W.getLoadingView().hide();
				W.showHint('error', '加载菜单数据失败!');
			}
		});
    },
    
    //初始化自定义菜单
    initMenus: function(menus) {
    	var length = menus ? menus.length : 0;
        for (var i = 0; i < length; ++i) {
			this.$('.xui-i-menu').append('<div class="xui-i-menu-item"></div>');
			var menuItem = new W.view.weixin.MenuItem({
		        el: this.$("div[class=xui-i-menu-item]:last")
		    });
		    menuItem.addMenuItem(menus[i]);
        }
        var $lastOneMenuItemDiv = $("div[class=xui-i-menu-item]:last");
        if ($lastOneMenuItemDiv.length > 0) {
	        var top = $("div[class=xui-i-menu-item]:last").offset().top;
			if (top + 260 <= 810) {
				this.$('.xui-i-editor-panel').css('height', 810);
			} else {
				this.$('.xui-i-editor-panel').css('height', top + 260);
			}
		}
    },
    
    render: function() {
        //创建html
        return this;
    },
	
	//添加一级菜单导航
	onAddOneMenu: function(event) {
		var length = parseInt(this.$('.xui-i-menu-item').length);
		if (length >= 3) {
			W.showHint('error', '最多只能创建3个一级菜单！');
			return;
		}
    	
    	var $menu = this.$('.xui-i-menu').append('<div class="xui-i-menu-item"></div>');
	    var $oneMenuDiv = $("div[class=xui-i-menu-item]:last");
    	var menuItem = new W.view.weixin.MenuItem({
	        el: $oneMenuDiv
	    });
	    
		var $input = $oneMenuDiv.find('input');
		$input.removeAttr('readonly');
		
		var top = $oneMenuDiv.offset().top;
		if (top + 260 <= 810) {
			this.$('.xui-i-editor-panel').css('height', 810);
		} else {
			this.$('.xui-i-editor-panel').css('height', top + 260);
		}
		
		var width = W.menuPhone.menubar.getNewMenuWidth(length);
		var menuId = W.menuPhone.menubar.addNewMenu(width);
		$input.attr('data-menu-id', menuId);
		W.menuPhone.menubar.getMenu(menuId).set('name', $input.val());
		W.menuPhone.menubar.refresh();
		if (W.menuPhone.menubar.activeMenuId) {
			W.menuPhone.menubar.selectMenu(W.menuPhone.menubar.activeMenuId);
		}
		
		menuItem.changeEditMessagePanel($oneMenuDiv.find('.xui-one-menu'), 1);
		
		var menuData = W.menuPhone.getMenuData();
		$.each(menuData, function(i, n) {
			if (n.items.length > 0) {
				var $menuItem = W.menuPhone.menubar.$menuContainer.find('a[data-menu-id="' + n.id + '"]');
				$menuItem.prepend('<img src="/static_v2/img/weixin/menu_item.png" class="mr5 mb3">');
			}
		});
	},
	
	onSubmitCustomMenus: function(event) {
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
			return;
		} else if (tipType === 1) {
			W.showHint('error', '二级菜单不能为空');
			menuItem.changeEditMessagePanel($inputParentDiv, 2);
			return;
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
			
			return;
		} else if (tipType === 4 || tipType === 5) {
			W.showHint('error', '回复内容不能为空');
			menuItem.changeEditMessagePanel($inputParentDiv, tipType - 3);
			
			return;
		} else {
			W.getLoadingView().show();
			
			W.resource.new_weixin.Menu.post({
				data: {menus: JSON.stringify(data)},
				success: function(result) {
					W.getLoadingView().hide();
			    	W.showHint('success', '更新菜单成功');
				},
				error: function(resp) {
					W.getLoadingView().hide();
					W.showHint('error', '更新菜单失败');
				}
			});
		}
	},
	
	onTabCustomMenu: function(event) {
		var $current = $(event.currentTarget);
		var status = 1;
		if ($current.hasClass('btn-danger')) {
			status = 0;
		}
		var $tabState = $current.parents('.xui-i-tab-state');
		
		var _this = this;
		W.resource.new_weixin.MenuStatus.post({
			data: {
				status: status
			},
			success: function(data) {
				W.getLoadingView().hide();
				if (status === 1) {
		    		W.showHint('success', '启用菜单成功');
		    		if (_this.is_certified_service == 'True') {
		    			$tabState.find('div[name="stopMenu"]').find('.xui-i-state-tip').css('margin-top', '-10px');
		    		}
		    		$tabState.find('div[name="stopMenu"]').removeClass('hidden');
		    		$tabState.find('div[name="startMenu"]').addClass('hidden');
		    	} else if (status === 0) {
		    		W.showHint('success', '停用菜单成功');
		    		$tabState.find('div[name="stopMenu"]').addClass('hidden');
		    		$tabState.find('div[name="startMenu"]').removeClass('hidden');
		    	} else {
		    		W.showHint('success', '未知操作成功');
		    	}
			},
			error: function(resp) {
				W.getLoadingView().hide();
				if (status === 1) {
		    		W.showHint('error', '启用菜单失败');
		    	} else if (status === 0) {
		    		W.showHint('error', '停用菜单失败');
		    	} else {
		    		W.showHint('error', '未知操作失败');
		    	}
			}
		});
	},
});