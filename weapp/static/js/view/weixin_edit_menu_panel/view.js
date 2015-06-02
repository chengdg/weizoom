/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * News编辑面板
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.EditMenuPanel = Backbone.View.extend({
	el: '',

	events: {
		'click #submit-btn': 'onSubmitNews',
		'input input[name="menuText"]': 'onChangeMenuText',
		'input input[name="url_answer"]': 'onChangeUrlText',
		'click #editMenuPanel-deleteLink': 'onClickDeleteMenuLink',
		'click a[data-type="text"]': 'onClickTextMessageTab',
		'click a[data-type="news"]': 'onClickNewsMessageTab',
		'click a[data-type="url"]': 'onClickUrlMessageTab',
		'click .xa-embededPhone-showBtn': 'onClickNewsMessageTab'
	},

    getTemplate: function(){
        $('#weixin-edit-menu-view-tmpl-src').template('weixin-edit-menu-view-tmpl');
        return 'weixin-edit-menu-view-tmpl';
    },
	
	initialize: function(options) {
		this.$el = $(this.el);

        this.template = this.getTemplate();

        this.$el.html($.tmpl(this.template, {
        }));

        this.model = null;
        this.newses = null;

		/**
		 * 创建news editor
		 * @type {W.NewsEditorView}
		 */
		/*
		this.newsEditor = new W.view.weixin.NewsEditor({
			el: this.$('#news-editor-box').get(),
			enableAnimation: true
		});
        if (options.mode == 'single-news') {
            this.newsEditor.preserveNewsUnder(1);
        } else if(options.mode == 'multi-news') {
            this.newsEditor.preserveNewsUnder(2);
        }
        */

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

		//创建富文本编辑器
		this.editor = new W.view.common.RichTextEditor({
			el: 'textarea',
			type: 'text',
			maxCount: 600
		});
		this.editor.bind('contentchange', function() {
			if (this.model) {
				var content = this.editor.getContent();
				var answer = {
					type: 'text',
					content: content
				}
				this.model.set('answer', answer);
			}
		}, this);
		this.editor.render();

		/*
		 * 创建material的display view
		 */
		this.$textMessageTab = $('a[href="#weixinMessageEditer-textMessageZone"]');
		this.$newsMessageTab = $('a[href="#weixinMessageEditer-newsMessageZone"]');
		this.$urlMessageTab = $('a[href="#weixinMessageEditer-urlMessageZone"]');
		this.materialDisplayView = new W.view.weixin.MaterialDisplayView({
			el: '#weixinMessageEditer-newsMessageZone',
			enableEdit: true,
			enableChangeMaterial: true
		});
		this.materialDisplayView.bind('material-after-display', function(newses){
			xlog('newses...');
			xlog(newses);
			var height = 406 + 19 * newses.length;
			$('.mask').css('height', height+'px');

		}, this);
		this.materialDisplayView.render();

		//加载菜单数据
		W.getLoadingView().show();
		W.getApi().call({
			app: 'weixin/manage/customized_menu',
			api: 'menus/get',
			args: {},
			scope: this,
			success: function(menus) {
				W.getLoadingView().hide();
				this.phone.addMenus(menus);
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
     * onSelectMenu: embeded phone中select-menu事件的响应函数
     */
    onSelectMenu: function(menuModel) {

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
		$menuTextInput.focus().val(menuModel.get('name'));
		var answer = menuModel.get('answer');
		if (answer.type == 'text') {
			this.$textMessageTab.tab('show');
			this.editor.setContent(answer.content);
			$('.mask').css('height','394px');
		} else if (answer.type == 'url'){
			$('#url_answer').val(answer.content);
			this.$urlMessageTab.tab('show');
			$('.mask').css('height','394px');
		}
		else {
			this.materialDisplayView.showMaterial(answer.content);
			this.$newsMessageTab.tab('show');
		}
		if (menuModel.get("type") ===  "menu"){
			var item_length = menuModel.get('items').length;
			if (item_length > 0){
				$('.mask').css('display','table');
			} else {
				$('.mask').css('display','none');
			}
		} else {
			$('.mask').css('display','none');
		}

    },

    /**
     * onChangeMenuText: menu文本改变时的响应函数
     */
    onChangeMenuText: function(event) {
    	var $input = $(event.currentTarget);
    	
    	this.model.set('name', $input.val());
    },


    /**
     * onChangeUrlText: menu URL改变时的响应函数
     */
    onChangeUrlText: function(event) {
    	var $input = $(event.currentTarget);
    	var answer = {
				type: 'url',
				content: $input.val()
			}
		this.model.set('answer', answer);
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
	 * onClickTextMessageTab: 点击“文字”tab的响应函数 
	 */
	onClickTextMessageTab: function() {
	},

	onClickUrlMessageTab: function(){
		// 自定义菜单--跳转链接--外部链接地址 默认值改为http://
		$('#url_answer').val('http://');
	},

	/**
	 * onClickNewsMessageTab: 点击“图文”tab的响应函数 
	 */
	onClickNewsMessageTab: function(event) {
		event.stopPropagation();
		event.preventDefault();

		var _this = this;
		W.dialog.showDialog('W.dialog.weixin.SelectMaterialDialog', {
			success: function(ids) {
				if (ids.length > 0) {
					var materialId = ids[0];
					xlog('news answer: ' + ids[0]);
					var answer = {
						type: 'news',
						content: materialId
					}
					_this.model.set('answer', answer);
					_this.materialDisplayView.showMaterial(materialId);
					_this.$newsMessageTab.tab('show');
				}
			}
		})
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

		// 解决需求16，迭代19，编号002407修改外部链接输入框自动加入http://
		// 当前选择外部链接未以http://开头，点击提交按钮回显添加http://后的结果
		var lis=$menuForm.find('li');
		var url_answer=$menuForm.find('#url_answer');
		if (lis.length>2 && $(lis[2]).hasClass('active')// 判断当前激活是否是跳转链接选项卡
			&& url_answer.val().indexOf('http://') === -1) 
			url_answer.val('http://'+url_answer.val());
		// 提交数据前判断类型是url的内容未以http://开头，自动添加http://开头
		$.each(this.phone.getMenuData(),function(i,n){
			$.each(n.items,function(j,m){
				if(m.answer && m.answer.type=='url' && m.answer.content.indexOf('http://') === -1)
					m.answer.content='http://'+m.answer.content;
			});
		});
		
		/*var answer = this.model.get('answer');
		if (answer.type == 'url'){
			var answer_url = {
				type: 'url',
				content: $('#url_answer').val()
			}
			this.model.set('answer', answer_url);
		}*/

		W.getLoadingView().show();
		var data = JSON.stringify(this.phone.getMenuData());
		W.getApi().call({
			app: 'weixin/manage/customized_menu',
			api: 'update',
			args: {
				data: data
			},
			method: 'post',
			success: function(data) {
				W.getLoadingView().hide();
				W.getSuccessHintView().show('更新菜单成功');
			},
			error: function(resp) {
				W.getLoadingView().hide();
				W.getErrorHintView().show('更新菜单失败');
			}
		});
	},
});