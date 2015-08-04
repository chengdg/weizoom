/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.view.webapp');
W.view.webapp.GlobalNavbarEditor = Backbone.View.extend({
	el: '',

	events: {
		'click #submit-btn': 'onSubmitNews',
		'input input[name="menuText"]': 'onChangeMenuText',
		'click #editMenuPanel-deleteLink': 'onClickDeleteMenuLink',
		'click .xa-selectWebappPage': 'onClickSelectWebappPageLink'
	},

    getTemplate: function(){
        $('#weixin-global-navbar-editor-tmpl-src').template('weixin-global-navbar-editor-tmpl');
        return 'weixin-global-navbar-editor-tmpl';
    },
	
	initialize: function(options) {
		this.$el = $(this.el);

        this.template = this.getTemplate();

        this.$el.html($.tmpl(this.template, {
        }));

        this.model = null;
        this.newses = null;

        /**
		 * 初始化模拟器
		 */
		this.phone = new W.view.weixin.EmbededPhoneView({
			el: this.$('#small-phone-box').get(),
			enableMenu: true,
			onBeforeChangeMenu: _.bind(this.onBeforeChangeMenu, this)
		});
		this.phone.bind('select-menu', _.bind(this.onSelectMenu, this));
		this.phone.bind('select-menu-item', _.bind(this.onSelectMenu, this));
		this.phone.render();

		var menus = options.menus || [];
		this.phone.addMenus(menus);

		//加载菜单数据
		W.getLoadingView().show();
		W.getApi().call({
			app: 'webapp',
			api: 'global_navbar/get',
			args: {},
			scope: this,
			success: function(data) {
				W.getLoadingView().hide();
				this.phone.addMenus(data.menus);

				if (data.is_enable) {
					this.$('.xa-enableGlobalNavbar').attr('checked', 'checked');
				} else {
					this.$('.xa-notEnableGlobalNavbar').attr('checked', 'checked');
				}
			},
			error: function(resp) {
				W.getLoadingView().hide();
				alert('加载菜单数据失败!');
			}
		});
	},

    render: function(){
        //创建html
        return this;
    },

    /**
     * onBeforeChangeMenu: phone中menubar上改变menu前的回调函数。
     *   返回false，阻止menubar改变menu；
     *   返回true，允许menubar改变menu
     */
    onBeforeChangeMenu: function() {
    	var $menuForm = this.$('#editMenuForm');

    	if (!$menuForm.is(':visible')) {
    		//form没有显示时，允许切换menu
			return true;
		}

		if (!W.validate()) {
			return false;
		}

		return true;
    },

    /**
     * onChangeMenuText: menu文本改变时的响应函数
     */
    onChangeMenuText: function(event) {
    	var $input = $(event.currentTarget);
    	
    	this.model.set('name', $input.val());
    },

    /**
     * onSelectMenu: embeded phone中select-menu事件的响应函数
     */
    onSelectMenu: function(menuModel) {
    	var data = menuModel.get("answer")['data'];
    	if (!data) {
    		menuModel.get("answer")['data'] = "javascript:void(0);";
    		menuModel.get("answer")['workspace'] = "";
    	}
    	
		var $menuForm = this.$('#editMenuForm');

		var $maxWordCount = $menuForm.find('.x-editMenuView-maxInputWordCount');
		var $menuTextInput = $menuForm.find('input[name="menuText"]');

		var type = menuModel.get('type');
		if (type == 'menu') {
			$maxWordCount.text('5');
			$menuTextInput.attr('maxlength', '5');
		} else if (type == 'menuitem') {
			$maxWordCount.text('7');
			$menuTextInput.attr('maxlength', '7');
		}
		
		if (!$menuForm.is(':visible')) {
			$menuForm.show();
		}
		this.model = menuModel;
		$('.xa-webappPageName').val(this.model.get('answer').data_path)
		$menuTextInput.focus().val(menuModel.get('name'));
    },

    /**
     * onClickDeleteMenuLink: 点击“删除”按钮的响应函数
     */
    onClickDeleteMenuLink: function(event) {
    	this.phone.deleteMenu(this.model);
    	this.model = null;
    	this.$('#editMenuForm').hide();
    },

	/**
	 * onClickSelectWebappPageLink: 点击“选择微站页面”按钮的响应函数 
	 */
	onClickSelectWebappPageLink: function(event) {
		event.stopPropagation();
		event.preventDefault();

		var $link = $(event.currentTarget);
		var _this = this;
		var currentLinkTarget = this.model.get('answer');
		xlog('currentLinkTarget');
		xlog(currentLinkTarget);
		W.dialog.showDialog('W.dialog.workbench.SelectLinkTargetDialog', {
            currentLinkTarget: currentLinkTarget,
            success: function(data) {
            	data = $.parseJSON(data);
            	_this.model.set('answer', data);
            	$link.parent().find('.xa-webappPageName').val(data.data_path)
            	xlog(_this.model.toJSON());
            }
        });
	},

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmitNews: function(event) {
		var $menuForm = this.$('#editMenuForm');

    	if ($menuForm.is(':visible')) {
    		if (!W.validate()) {
				return false;
			}
		}

		W.getLoadingView().show();
		var data = JSON.stringify(this.phone.getMenuData());
		var isEnable = this.$('[name="enable_global_navbar"]:checked').val();
		W.getApi().call({
			app: 'webapp',
			api: 'global_navbar/update',
			args: {
				is_enable: isEnable,
				data: data
			},
			method: 'post',
			success: function(data) {
				W.getLoadingView().hide();
				W.getSuccessHintView().show('更新全局导航成功');
			},
			error: function(resp) {
				W.getLoadingView().hide();
				W.getErrorHintView().show('更新全局导航失败');
			}
		});
	},
});