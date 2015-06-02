/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.view.weixin');
ensureNS('W.model.weixin');

W.model.weixin.Menu = function() {
    this.menus = new Backbone.Collection();
    this.menus.comparator = 'index';
    this.menus.bind('change:name', function(menu, newName) {
        this.trigger('menu-name-changed', menu, newName)
    }, this);
}
_.extend(W.model.weixin.Menu.prototype, Backbone.Events, {
    __getDefaultAnswer: function() {
        var answer = {
            type: 'text',
            content: ''
        }
        return answer;
    },

    addMenu: function(value) {
        var items = new Backbone.Collection();
        items.comparator = 'index';
        items.bind('change:name', function(menuItem, newName) {
            this.trigger('menu-item-name-changed', menuItem, newName)
        }, this);

        var model = new Backbone.Model({
            type: 'menu',
            id: value.id,
            index: value.index,
            name: value.name,
            items: items,
            answer: value.answer || this.__getDefaultAnswer()
        });
        this.menus.add(model);       

        //如果items存在，添加items
        if (value.items && value.items.length > 0) {
            var menuId = value.id;
            _.each(value.items, function(item) {
                this.addMenuItem(menuId, item);
            }, this);
        }
    },

    deleteMenu: function(menuId) {
        var menu = this.getMenu(menuId);
        this.menus.remove(menu);
    },

    addMenuItem: function(menuId, value) {
        var model = new Backbone.Model({
            type: 'menuitem',
            id: value.id,
            index: value.index,
            name: value.name,
            answer: value.answer || this.__getDefaultAnswer()
        });

        var menu = this.menus.findWhere({id: menuId});
        menu.get('items').add(model);
    },

    deleteMenuItem: function(menuId, menuItemId) {
        var items = this.getMenuItems(menuId);
        var item = this.getMenuItem(menuId, menuItemId);
        items.remove(item);
    },

    getMenus: function() {
        return this.menus;
    },

    getMenu: function(menuId) {
        return this.menus.findWhere({id: menuId});
    },

    getMenuItems: function(menuId) {
        return this.menus.findWhere({id: menuId}).get('items');
    },

    getSortedMenuItems: function(menuId) {
        xlog('menuId: ' + menuId + ' ' + typeof(menuId));
        var items = this.menus.findWhere({id: menuId}).get('items');
        items.sort()
        return items;
    },

    getMenuItem: function(menuId, itemId) {
        var items = this.getMenuItems(menuId);
        return items.findWhere({id: itemId});
    },

    getMenuData: function() {
        var menusJson = this.menus.toJSON();
        _.each(menusJson, function(menuJson) {
            menuJson.items = menuJson.items.toJSON();
        });

        return menusJson;
    }
});


/**
 * 微信模拟器中的菜单条
 *  menu: 菜单
 *  menuItem: 菜单项
 *
 *  菜单条一共有两种模式：
 *   edit: 用于编辑菜单
 *   action: 用于在simulator中模拟真实环境下的菜单行为
 *
 * @class
 */
W.view.weixin.EmbededPhoneMenuBar = Backbone.View.extend({
    el: '',

    events: {
        'click .x-addMenuBtn': 'onClickAddMenuButton',
        'click .oneMenu': 'onClickMenuButton',
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.onBeforeChangeMenu = options.onBeforeChangeMenu;

        this.menuId = 1;
        this.mode = options.mode || 'edit';

        this.$menuContainer = this.$('.x-menus').eq(0);
        if (this.mode === 'edit') {
            this.$menuContainer.sortable({
                axis: 'x',
                helper: 'clone',
                opacity: 0.5,
                stop: _.bind(this.sortMenus, this)
            }).disableSelection();
        }

        this.$menuItemContainer = $('.x-menuItemContainer').eq(0);
        var _this = this;
        this.$menuItemContainer.find('.x-addMenuItemButton').click(function(event) {
            _this.onClickAddMenuItemButton(event);
        });
        this.$menuItemContainer.delegate('.oneMenuItem', 'click', _.bind(this.onClickMenuItemButton, this));
        if (this.mode === 'edit') {
            this.$menuItemContainer.find(".x-menuItems").sortable({
                axis: 'y',
                placeholder: "ui-state-highlight",
                opacity: 0.5,
                stop: _.bind(this.sortMenuItems, this)
            }).disableSelection();
        }

        this.menuTemplate = new W.Template('<a class="btn oneMenu" style="width: ${width};" data-menu-id="${id}">${name}</a>');
        this.menuItemTemplate = new W.Template('<h3 class="popover-title oneMenuItem" data-menu-id="${id}">${name}</h3>');
        this.activeMenuId = -1;
        this.activeMenuItemId = -1;

        this.weixinMenu = new W.model.weixin.Menu();
        this.weixinMenu.bind('menu-name-changed', _.bind(this.onChangeMenuName, this));
        this.weixinMenu.bind('menu-item-name-changed', _.bind(this.onChangeMenuItemName, this));
    },

    /**
     * deleteMenu: 删除菜单或菜单项
     */
    deleteMenu: function(model) {
        if (model.get('type') == 'menu') {
            var menuId = model.get('id');
            this.weixinMenu.deleteMenu(menuId);

            this.$menuContainer.find('[data-menu-id="'+menuId+'"]').remove();
            this.hideMenuItems();

            this.refresh();
        } else if (model.get('type') == 'menuitem') {
            var menuItemId = model.get('id');
            this.weixinMenu.deleteMenuItem(this.activeMenuId, menuItemId);

            this.$menuItemContainer.find('[data-menu-id="'+menuItemId+'"]').remove();
        }
    },

    getMenuData: function() {
        return this.weixinMenu.getMenuData();
    },

    refresh: function() {
        this.$menuContainer.empty();
        this.$menuItemContainer.find('.x-items').empty();

        var menus = this.weixinMenu.getMenus();
        var _this = this;
        var width = this.getNewMenuWidth(menus.length);

        if (this.mode === 'action') {
            this.$menuContainer.append('<a class="btn oneMenu" style="width: 10%;" data-menu-id="0"><span style="position: relative; left: -100px;">*</span><i class="icon-edit"></i></a>');
        }
        menus.each(function(menu) {
            //添加menu的ui元素
            var menuId = menu.get('id');
            if (_this.menuId <= menuId) {
                _this.menuId = menuId+1;
            }
            var $node = $(_this.menuTemplate.render({
                name: menu.get('name'),
                width: width,
                id: menuId
            }));
            _this.$menuContainer.append($node);

            //添加menu item的ui元素
            var items = _this.weixinMenu.getMenuItems(menuId);
            items.each(function(item) {
                var itemId = item.get('id');
                if (_this.menuId <= itemId) {
                    _this.menuId = itemId+1;
                }
                var $node = $(_this.menuItemTemplate.render({
                    name: item.get('name'),
                    id: itemId
                }));
                _this.$menuItemContainer.find('.x-menuItems').prepend($node);
            })
        });
    },

    /**************************************************************
     * menu部分操作
     **************************************************************/
    /**
     * getMenuCount: 获得menu的数量
     */
    getMenuCount: function() {
        return this.$menuContainer.find('.oneMenu').length;
    },

    /**
     * getMenuCount: 获得menu的数量
     */
    getNewMenuWidth: function(newMenuCount) {
        var width = '100%';
        if (this.mode === 'action') {
            if (newMenuCount === 1) {
                width = '89%';
            } else if (newMenuCount === 2) {
                width = '44.5%';
            } else if (newMenuCount === 3) {
                width = '29.5%'
            }
        } else {
            if (newMenuCount === 1) {
                width = '100%';
            } else if (newMenuCount === 2) {
                width = '49.0%';
            } else if (newMenuCount === 3) {
                width = '32.6%'
            }
        }

        return width;
    },

    /**
     * adjustExistedMenuWidth: 调整已存在menu的宽度
     */
    adjustExistedMenuWidth: function(width) {
        this.$menuContainer.find('.oneMenu').each(function() {
            var $menu = $(this);
            $menu.css('width', width);
        });
    },

    /**
     * addMenus: 添加菜单数据
     */
    addMenus: function(menus) {
        xwarn(menus);
        for (var i = 0; i < menus.length; ++i) {
            var menu = menus[i];
            //记录数据
            this.weixinMenu.addMenu(menu);
        }

        this.refresh();
    },

    /**
     * addNewMenu: 添加新的menu
     */
    addNewMenu: function(width) {
        var id = this.menuId++;
        var menuName = '菜单' + id;

        //记录数据
        this.weixinMenu.addMenu({
            id: id,
            index: id,
            name: menuName
        })

        //更新ui
        var $node = $(this.menuTemplate.render({
            name: menuName,
            width: width,
            id: id
        }));
        this.$menuContainer.append($node);

        return id;
    },

    selectMenu: function(idOrMenu) {
        if (this.onBeforeChangeMenu) {
            if (!this.onBeforeChangeMenu()) {
                //没有通过检验，不能切换menu
                return;
            }
        }

        var $menu = null;
        var id = 0;
        if ($.isNumeric(idOrMenu)) {
            id = idOrMenu;
            if (id === -1) {
                return;
            }
            $menu = this.$menuContainer.find('[data-menu-id="'+id+'"]');
        } else {
            $menu = idOrMenu;
            id = parseInt($menu.attr('data-menu-id'));
        }

        this.$menuItemContainer.find('.active').removeClass('active');
        this.$menuContainer.find('.oneMenu.active').removeClass('active');
        $menu.addClass('active');
        this.showMenuItems(id);

        var menuModel = this.weixinMenu.getMenu(id);
        this.trigger('select-menu', menuModel);
    },

    /**
     * onClickAddMenuButton: 点击“添加菜单”按钮的响应函数
     */
    onClickAddMenuButton: function(event) {
        var menuCount = this.getMenuCount();
        if (menuCount >= 3) {
            W.getErrorHintView().show('最多只能创建3个一级菜单！');
            return;
        }

        var newMenuCount = menuCount + 1;
        var width = this.getNewMenuWidth(newMenuCount);
        this.adjustExistedMenuWidth(width);

        var newMenuId = this.addNewMenu(width);
        this.selectMenu(newMenuId);
    },

    /**
     * onClickMenuButton: 点击menu的响应函数
     */
    onClickMenuButton: function(event) {
        var $menu = $(event.currentTarget);
        if (this.mode === 'action') {
            //在action模式下，检查是否点击了返回编辑模式的按钮
            var id = parseInt($menu.attr('data-menu-id'));
            if (id === 0) {
                this.hideMenuItems();
                this.$menuContainer.find('.active').removeClass('active');
                this.trigger('click-menubar-edit-button');
                return;
            } else {
                if (!$menu.hasClass('active')) {
                    var id = parseInt($menu.attr('data-menu-id'));
                    var menuItems = this.weixinMenu.getMenuItems(id);
                    if (menuItems.length > 0) {
                        //有菜单项，显示菜单项
                        this.selectMenu(id);
                    } else {
                        //无菜单项，激发事件
                        this.trigger('click-menu', id);
                    }
                } else {
                    this.hideMenuItems();
                    this.$menuContainer.find('.active').removeClass('active');
                }
            }
        } else {
            if (!$menu.hasClass('active')) {
                var id = parseInt($menu.attr('data-menu-id'));
                this.selectMenu(id);
            } else {
                xlog('menu already active');
            }
        }
    },

    /**
     * sortMenus: 对menus进行排序
     */
    sortMenus: function() {
        if (this.mode === 'action') {
            return;
        }
        var menus = this.weixinMenu.getMenus();
        var index = 1;
        var _this = this;
        this.$menuContainer.find('.oneMenu').each(function() {
            var $menu = $(this);
            var menuId = parseInt($menu.attr('data-menu-id'));
            var menu = _this.weixinMenu.getMenu(menuId);
            menu.set('index', index);
            index++;
        });
        this.selectMenu(this.activeMenuId);
    },

    /**
     * onChangeMenuName: weixinMenu中menu-name-changed事件的响应函数
     */
    onChangeMenuName: function(menuModel, newName) {
        var id = menuModel.get('id');
        var $menu = this.$menuContainer.find('[data-menu-id="'+id+'"]');
        $menu.text(newName);
    },

    /**************************************************************
     * menu item 部分操作
     **************************************************************/
    /**
     * addNewMenuItem: 添加新的
     */
    addNewMenuItemTo: function(menuId) {
        var itemId = this.menuId++;
        var itemName = '菜单项' + itemId;

        //记录数据
        this.weixinMenu.addMenuItem(menuId, {
            id: itemId,
            index: itemId,
            name: itemName
        });

        //更新ui
        var $node = $(this.menuItemTemplate.render({
            name: itemName,
            id: itemId
        }));
        this.$menuItemContainer.find('.x-menuItems').prepend($node);
        this.selectMenuItem(this.activeMenuId, $node);
    },

    /**
     * showMenuItems: 显示菜单项
     */
    showMenuItems: function(menuId) {
        //清空旧的内容
        this.$menuItemContainer.find('.x-menuItems').empty();

        //更新menu items
        var menuItems = this.weixinMenu.getSortedMenuItems(menuId);
        xlog('show items');
        menuItems.each(function(item) {
            xlog(item.toJSON());
            this.$menuItemContainer.find('.x-menuItems').prepend(this.menuItemTemplate.render({
                name: item.get('name'),
                id: item.get('id')
            }));
        }, this);

        /*
         * 设置位置信息
         */
        var $menu = this.$menuContainer.find('[data-menu-id="'+menuId+'"]');
        //获得新加menu的尺寸信息
        var menuLeft = $menu.offset().left;
        var menuWidth = $menu.outerWidth();
        //获得第一个menu的尺寸信息
        var $firstMenu = this.$menuContainer.find('.oneMenu').eq(0);
        var firstMenuLeft = $firstMenu.offset().left;
        //获得menu container的宽度
        var popoverWidth = this.$menuItemContainer.outerWidth();
        //获得menu item的左边距
        var popoverLeft = menuLeft - firstMenuLeft + (menuWidth - popoverWidth)/2
        //显示menu item
        this.$menuItemContainer.css('left', popoverLeft);
        this.$menuItemContainer.hide().slideDown(200);

        this.activeMenuId = menuId;
    },

    /**
     * hideMenuItems: 隐藏菜单项
     */
    hideMenuItems: function() {
        this.$menuItemContainer.find('.active').removeClass('active');
        this.$menuItemContainer.hide();
    },

    selectMenuItem: function(menuId, idOrItem) {
        var $menuItem = null;
        var itemId = 0;
        if ($.isNumeric(idOrItem)) {
            itemId = idOrItem;
            $menuItem = this.$menuItemContainer.find('[data-menu-id="'+itemId+'"]');
        } else {
            $menuItem = idOrItem;
            itemId = parseInt($menuItem.attr('data-menu-id'));
        }

        this.$menuContainer.find('.oneMenu.active').removeClass('active');
        this.$menuItemContainer.find('.active').removeClass('active');
        $menuItem.addClass('active');

        var menuItemModel = this.weixinMenu.getMenuItem(menuId, itemId);
        this.trigger('select-menu-item', menuItemModel);
    },

    /**
     * onClickAddMenuItemButton: 点击“添加菜单项”按钮的响应函数
     */
    onClickAddMenuItemButton: function(event) {
        var menuItems = this.weixinMenu.getMenuItems(this.activeMenuId);
        var menuItemCount = menuItems.length;
        if (menuItemCount >= 5) {
            W.getErrorHintView().show('最多只能创建5个二级菜单！');
            return;
        }

        this.addNewMenuItemTo(this.activeMenuId);
    },

    /**
     * onClickMenuItemButton: 点击一个menu item的响应函数
     */
    onClickMenuItemButton: function(event) {
        var $menuItem = $(event.currentTarget);
        if (this.mode === 'action') {
            var id = parseInt($menuItem.attr('data-menu-id'));
            this.trigger('click-menu', id);
            this.hideMenuItems();
            this.$menuContainer.find('.active').removeClass('active');
        } else {
            if (!$menuItem.hasClass('active')) {
                this.selectMenuItem(this.activeMenuId, $menuItem);
            } else {
                xlog('already active');
            }
        }
    },

    /**
     * sortMenuItems: menu items的排序函数
     */
    sortMenuItems: function() {
        var $items = this.$menuItemContainer.find('.oneMenuItem');
        var index = $items.length;
        var _this = this;
        $items.each(function() {
            var $item = $(this);
            var itemId = parseInt($item.attr('data-menu-id'));
            var menuItem = _this.weixinMenu.getMenuItem(_this.activeMenuId, itemId);
            menuItem.set('index', index);
            index--;
        });
        xlog('finish sort menu items');
    },

    /**
     * onChangeMenuItemName: weixinMenu中menu-item-name-changed事件的响应函数
     */
    onChangeMenuItemName: function(menuItemModel, newName) {
        var id = menuItemModel.get('id');
        var $menuItem = this.$menuItemContainer.find('[data-menu-id="'+id+'"]');
        $menuItem.text(newName);
    },

});


/**
 * 用于嵌入到页面中的微信模拟器
 * @class
 */
W.view.weixin.EmbededPhoneView = Backbone.View.extend({
	el: '',

	events: {
        'mouseenter .wx-news-container': 'onShowActionBar',
		'mouseleave .wx-news-container': 'onHideActionBar',
		'click div.wx-action-bar': 'onSelectNews',
		'click #create-news-btn': 'onCreateNews',
        'click #back-weixin-btn': 'onClickBackBtn',
        'click #screen a': 'onClickLink'
	},

    compileTemplate: function() {
        $('#small-phone-tmpl-src').template('small-phone-tmpl');
        $('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
        $('#text-message-tmpl-src').template('text-message-tmpl');
    },
	
	initialize: function(options) {
		this.$el = $(this.el);

        this.messages = new W.model.weixin.Messages();//options.messages || [];
        this.messages.bind('change', _.bind(this.onChangeMessage, this));
        this.id2message = {};
        this.id2element = {};

		this.mode = options.mode || "weixin";
        this.onBeforeChangeNews = options.onBeforeChangeNews;
        this.onBeforeCreateNews = options.onBeforeCreateNews;
		this.shopName = options.shopName || "";
        this.initBrowserUrl = options.initBrowserUrl || '/m/shop/'+this.shopName+'/?embed=1';

        this.deleteIds = [];

		if (this.mode == "weixin") {
			this.reset(this.messages);
            this.enableWeixin = true;
            this.enableBrowser = true;
            this.initBrowserUrl = '/loading/';
		} else if (this.mode == 'webapp') {
			xlog('enter webapp mode');
            this.enableWeixin = false;
            this.enableBrowser = true;
            if (options.initBrowserUrl) {
                this.initBrowserUrl = options.initBrowserUrl;
            }
		} else {
            this.enableWeixin = true;
            this.enableBrowser = true;
        }

		this.enableAction = options.enableAction || false;
		this.container = null;
        this.enableAddNews = options.enableAddNews || false;
        //菜单栏
        this.enableMenu = options.enableMenu || false;
        this.onBeforeChangeMenu = options.onBeforeChangeMenu || null;
        this.menubar = null;

		this.isBrowserVisible = false;
        this.autoRefreshEnabled = true;

        this.messageIndex = 0; //用于计算message序号，对于多图文消息，我们会将多条message视为一条message

        this.compileTemplate();
        console.log('EmbededPhoneView', this.messages)
    },

    /**
     * 禁止自动refresh
     */
    disableRefresh: function() {
        this.autoRefreshEnabled = false;
    },

    /**
     * 开启自动refresh
     */
    enableRefresh: function() {
        this.autoRefreshEnabled = true;   
    },

    /**
     * 获取一个新的message index
     */
    getNewMessageIndex: function() {
        this.messageIndex += 1;
        return this.messageIndex;
    },

    getMessageIndex: function() {
        return this.messageIndex;
    },

    openBrowser: function(link) {
        if (link) {
            $('#mobile-browser').attr('src', link);
        }
        $('#timeline-zone').hide();
        $('#browser-zone').animate({
            left: '0'
        }, 400);
	    this.isBrowserVisible = true;
    },

    refreshBrowser: function(link) {
        xlog('refresh browser');

        var browser = $('#mobile-browser');
        if (!link) {
            link = browser.attr('src');
        }
        browser.attr('src', '/loading/');

        var task = new W.DelayedTask(function() {
            browser.attr('src', link);
        });
        task.delay(300);
    },

    closeBrowser: function() {
        $('#browser-zone').animate({
            left: '100%'
        }, 400);
        $('#timeline-zone').show();
	    this.isBrowserVisible = false;
    },

	isViewWebapp: function() {
		return this.isBrowserVisible;
	},

	/**
	 * 判断是否有新创建的news
	 */
	hasNewCreatedNews: function() {
        var count = this.messages.length;
        for (var i = 0; i < count; ++i) {
            var message = this.messages[i];
            if (message.type == 'news' && message.id < 0) {
                return true;
            }
        }

        return false;
	},

	/**
	 * 获得新增news
	 * @return {*}
	 */
	getNewCreatedNewses: function() {
		return _.filter(this.messages.toJSON(), function(message) {
//			return message.type == 'news' && message.id < 0;
            return message.type == 'news';
		}, this);
	},

    /**
     * 获得删除的id集合
     * @return {*}
     */
    getDeletedNewsIds: function() {
        return this.deleteIds.join(',')
    },

    /**
     * 渲染html结果
     */
	render: function() {
        //创建html
        this.$el.html($.tmpl('small-phone-tmpl', {
            enableWeixin: this.enableWeixin,
            enableBrowser: this.enableBrowser,
            enableMenu: this.enableMenu,
            shopName: this.shopName,
            title: W.previewName,
            initBrowserUrl: this.initBrowserUrl
        }));
		this.container = this.$el.find('#timeline-zone');
        //处理menubar
        var $menubar = this.$('#menubar-zone');
        if ($menubar.length > 0) {
            this.menubar = new W.view.weixin.EmbededPhoneMenuBar({
                el: $menubar,
                onBeforeChangeMenu: this.onBeforeChangeMenu
            });
            this.menubar.bind('all', function(event, model) {
                xlog('[embededPhone]: receive menubar event ' + event);
                this.trigger(event, model);
            }, this)
        }

		this.refresh();
	},

	/**
	 * 重新绘制消息区域
	 */
	refresh: function() {
        if (!this.container) {
            //DOM还没有准备好，返回
		    return;
        }

        this.container.html('');
        console.log('cccccccccccccccccc', this.messages.length)
		if (this.messages.length == 0) {
			return;
		}

        //merge messages, change message model to message  JSON
        var mergedMessages = [];
        var curMessageIndex = -1;
        var count = this.messages.length;
        var tempMessages = [];
        for (var i = 0; i < count; ++i) {
            var message = this.messages.at(i);
            var messageIndex = message.get('metadata').messageIndex;
            if (messageIndex != curMessageIndex) {
                curMessageIndex = messageIndex;
                if (tempMessages.length != 0) {
                    mergedMessages.push(tempMessages);
                    tempMessages = [];
                }
            }

            tempMessages.push(message.toJSON());
        }
        if (tempMessages.length != 0) {
            mergedMessages.push(tempMessages); //处理最后一条消息
        }

        //render messages
        var count = mergedMessages.length;
        console.log('count2222', count);
        for (var i = 0; i < count; ++i) {
            var messages = mergedMessages[i];
            if (messages.length == 1) {
                var message = messages[0];
                //text or single_news
                if (message.type == 'text') {
                    this.container.append($.tmpl('text-message-tmpl', {
                        extraClass: message.metadata.direction == 'send' ? 'shop-service' : 'customer',
                        texts: message.text.split('\n'),
                        imagePath: message.pic_url,
                        id: message.id
                    }));
                } else {
                    this.container.append($.tmpl('single-news-tmpl', {
                        news: message,
                        enableAddNews: this.enableAddNews
                    }));
                }
            } else {
                //multi_news
                var mainNews = messages[0];
                var subNewses = messages.slice(1);
	            this.enableAddNews = (subNewses.length == 9 ? false : true);
                this.container.append($.tmpl('multi-newses-tmpl', {
                    mainNews: mainNews,
                    subNewses: subNewses,
                    enableAddNews: this.enableAddNews
                }));
            }
        }
        
        //cache message's DOM element
        this.messages.each(function(message) {
            message.element = null;
            var selector = 'div[data-id="'+message.id+'"]';
            message.element = this.$(selector);
        });
	},

	/**
	 * 添加一条新建的news message
	 * @param news
	 */
	addNews: function(news) {
        var message = news;
        var metadata = message.get('metadata');
        metadata.messageIndex = this.getNewMessageIndex();
		this.messages.push(message);
        this.refresh();

        if (message.get('metadata') && message.get('metadata').autoSelect) {
            this.selectNews(message.id);
        }
	},

    /**
     * 向最后一条message中附加一条额外的message
     */
    appendNews: function(news) {
        var message = news;
        var metadata = message.get('metadata');
        metadata.messageIndex = this.getMessageIndex();

        this.messages.push(message);
        this.refresh();

        this.selectNews(message.id);
    },

    /**
     * 添加一组新建的news message
     */
    addNewses: function(messages) {
        this.messages.add(messages);
        this.refresh();

        var count = this.messages.length;
        for (var i = 0; i < count; ++i) {
            var message = this.messages.at(i);
            var metadata = message.get('metadata');
            if (0 == i) {
                metadata.messageIndex = this.getNewMessageIndex();
            } else {
                metadata.messageIndex = this.getMessageIndex();
            }
            if (message.get('metadata') && message.get('metadata').autoSelect) {
                this.selectNews(message.id);
            }
        }
    },

	deleteNews: function(news) {
        this.messages.remove(news);
        if(news.id > 0){
            this.deleteIds.push(news.id);
        }
		this.refresh();
	},

    checkNews: function() {
        xlog('check newses...');
        if (this.messages.length == 0) {
            this.trigger('start-create-news');
        }
    },

    /**
     * 添加一条“发送”方向的文本消息
     */
    addTextMessage: function(message) {
        var metadata = message.get('metadata');
        metadata.direction = 'send';
        metadata.messageIndex = this.getNewMessageIndex();
        message.set('pic_url', W.previewImage);
        this.messages.push(message);
        this.refresh();
    },

    /**
     * 收到一条文本消息
     * @param text
     */
    receiveTextMessage: function(message, options) {
        var metadata = message.get('metadata');
        metadata.direction = 'receive';
        metadata.messageIndex = this.getNewMessageIndex();
        message.set('pic_url', '/static/img/weixin-customer.jpg');
        this.messages.push(message);
        if (options && options.silent) {
            // silent, do nothing
        } else {
            this.refresh();
        }
    },

    /**
     * 选择一条news
     */
    selectNews: function(id) {
        if (this.enableAction) {
            var message = this.messages.get(id);
            var newsEl = message.element;
            $('div.wx-action-bar').attr('data-pin', 'false').hide();
            
            var actionBar = newsEl.find('div.wx-action-bar');
            actionBar.attr('data-pin', 'true');
            actionBar.show();

            this.trigger('select-news', message, this.messages.length);
        }
    },

    /**
     * 根据index选择一条
     */
    selectNewsByIndex: function(index) {
        var message = this.messages.at(index);
        if (message) {
            this.selectNews(message.id);
        }
    },

    /**
     * deleteMenu: 删除菜单或菜单项
     */
    deleteMenu: function(model) {
        this.menubar.deleteMenu(model);
    },

    /**
     * getMenuData: 获得menu的数据
     */
    getMenuData: function() {
        return this.menubar.getMenuData();
    },

    /**
     * addMenus: 添加菜单数据
     */
    addMenus: function(menus) {
        if (this.menubar) {
            this.menubar.addMenus(menus);
        } else {
            xlog('[embeded phone]: no menubar but called addMenus function');
        }
    },

    /**
     * 点击微信消息中链接的响应函数
     */
    onClickLink: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var url = $(event.target).attr('href');
        this.openBrowser(url);
    },

    /**
     * 点击左上角"微信"按钮的响应函数
     */
    onClickBackBtn: function(event) {
        this.closeBrowser();
    },

	onShowActionBar: function(event) {
        if (this.enableAction) {
    		var news = $(event.currentTarget);
    	   	var actionBar = news.find('div.wx-action-bar');
    		if ('false' == actionBar.attr('data-pin')) {
    			actionBar.show();
    		}
        }
	},

	onHideActionBar: function(event) {
        if (this.enableAction) {
    		var news = $(event.currentTarget);
    		var actionBar = news.find('div.wx-action-bar');
    		if ('false' == actionBar.attr('data-pin')) {
    			actionBar.hide();
    		}
        }
	},

	onSelectNews: function(event) {
        if (this.onBeforeChangeNews) {
            if (!this.onBeforeChangeNews()) {
                return;
            }
        }
        var newsEl = $(event.target).parents('div.wx-news-container');
        var id = newsEl.attr('data-id');
        this.selectNews(parseInt(id));
	},

    onChangeMessage: function(message) {
        _.each(message.changed, function(value, key) {
            // value = value == null ? '' : value
            // if (!value.hasOwnProperty('replace')){
            //     value = '';
            // }
            
            if (message.get('type') == 'text') {
                var selector = 'div.content';
                message.element.find(selector).html(value.replace(/\n/g, "<br />"));
            } else {
                if (key === 'pic_url') {
                    var selector = 'img[name="picture"]';
                    if (value.length == 0) {
                        value = '/static/img/empty_image.png';
                    }
                    message.element.find(selector).attr('src', value);
                } else {
                    var selector = 'span[name="'+key+'"]';
                    message.element.find(selector).html(value.replace(/\n/g, "<br />"));
                }
            }
        });
    },

	/**
	 * 添加图文消息的区域的点击事件的响应函数
	 * @param event
	 */
	onCreateNews: function(event) {
        if (this.onBeforeCreateNews) {
            //进行表单验证
            if (!this.onBeforeCreateNews()) {
                return;
            }
        }

        //确认是否可创建新的图文消息: 检查第二条图文是否已创建
        var message = this.messages.at(1);
        if (!message.get('title') 
            || !message.get('pic_url') 
            || !(message.get('link_target') || message.get('text'))
            ) {
            W.getErrorHintView().show('请添加第二条图文信息');
            this.selectNewsByIndex(1); //选中第二条图文信息
            return;
        }


		this.trigger('start-create-news');
	},

	/**
	 * 重置message集合
	 */
	reset: function(messages) {
        if (messages) {
    		this.messages = messages;
        } else {
            //this.messages = new W.model.weixin.Messages();;
            this.messages.reset();
        }
        _.each(this.messages.models, function(message) {
            this.id2message[message.id] = message;
        }, this);
        this.refresh();
	}
});