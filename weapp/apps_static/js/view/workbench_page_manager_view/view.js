/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * page manager
 * @class
 */
ensureNS('W.workbench');
W.workbench.PageManagerView = Backbone.View.extend({
	el: '',

	events: {
	},

	templates: {
		"viewTmpl": "#weixin-page-manager-tmpl-src"
	},

	initialize: function(options) {
		this.isSystemManager = true;
		if (options.hasOwnProperty('isSystemManager')) {
			this.isSystemManager = options.isSystemManager;
		}

		this.pages = [];
		this.currentActivePage = null;
		this.id2pageTemplate = {};

		//监听全局事件
		W.Broadcaster.on('component:create', this.onCreateComponent, this);
		W.Broadcaster.on('mobilepage:sort_widget', this.onSortWidget, this);
		W.Broadcaster.on('designpage:drag_widget', this.onDragWidget, this);
		W.Broadcaster.on('designpage:finish_init', this.onFinishInitDesignPage, this);
		W.Broadcaster.on('designpage:wait_for_page', this.onWaitForPage, this);
		W.Broadcaster.on('designpage:select_page_component', this.onSelectPageComponentInDesignPage, this);

		W.data.pageManager = this;
	},

	render: function() {
		return;
	},

	/**
	 * getPages: 获得page集合
	 */
	getPages: function() {
		return this.pages;
	},

	getPageByCid: function(cid) {
		cid = parseInt(cid);
		return _.findWhere(this.pages, {
			cid: cid
		});
	},

	/**
	 * getCurrentActivePage: 获得当前选中的page
	 */
	getCurrentActivePage: function() {
		return this.currentActivePage;
	},

	/***********************************************************
	 * activePage: 设置page为当前活动page
	 ***********************************************************/
	activePage: function(page, options) {
		var pageComponent = page;
		this.currentActivePage = pageComponent;

		W.workbench.PageManagerView.currentActivePage = pageComponent;
		W.Broadcaster.trigger('designpage:update_site_title', pageComponent.model.get('site_title'));
		W.Broadcaster.trigger('component:select', pageComponent);
		if (options && options.triggerSelectPageComponentEvent) {
			_.delay(function() {
				W.Broadcaster.trigger('designpage:select_page_component');
			}, 100);
		}
	},

	/***********************************************************
	 * addPage: 添加一个Page
	 ***********************************************************/
	addPage: function(title, page, options) {
		this.pages.push(page);
		return page;
	},

	exportPage: function(event) {
		window.open('/termite2/page_archive/?project_id=' + W.projectId);
	},

	importPage: function(event) {
		W.dialog.showDialog('W.dialog.termite.ImportPageDialog', {
			success: function(data) {
				xwarn(data);
			}
		})
	},

	/***********************************************************
	 * onCreateComponent: component:create事件的响应函数
	 ***********************************************************/
	onCreateComponent: function(component, relatedComponent) {
		if (this.currentActivePage) {
			xlog('[page manager]: insert ' + component.cid + '(' + component.type + ')' + ' to page');
			if (relatedComponent.type === 'wepage.componentadder') {
				//从"添加模块"component创建
				this.currentActivePage.addComponent(component, {position: -1});
			} else {
				//从其他component创建
				this.currentActivePage.insertComponentAfter(component, relatedComponent);
			}
			
			W.Broadcaster.trigger('component:finish_create', this.currentActivePage, component);
		}
	},

	/***********************************************************
	 * onSortWidget: mobilepage:sort_widget事件响应函数
	 ***********************************************************/
	onSortWidget: function(orderedCids) {
		xlog('[page manager]: sort widget after drag... ' + orderedCids);
		var index = 1;
		_.each(orderedCids, function(cid) {
			W.component.getComponent(cid).model.set('index', index++, {
				silent: true
			});
		})
	},

	/***********************************************************
	 * onDragWidget: mobilepage:drag_widget事件响应函数
	 ***********************************************************/
	onDragWidget: function($mobilePage, itemUid, targetContainerUid) {
		if (!targetContainerUid) {
			//在page内移动，直接返回
			return;
		}

		var sourceContainerUid = W.component.getComponent(itemUid).pid + '';
		if (sourceContainerUid === targetContainerUid) {
			//在同一个容器内移动，直接返回
			return;
		}

		//调整component之间的包含关系
		xlog('[page manager]: drag ' + itemUid + '(' + (typeof itemUid) + ')' + ' from ' + sourceContainerUid + '(' + (typeof sourceContainerUid) + ')' + ' to ' + targetContainerUid + '(' + (typeof targetContainerUid) + ')');
		var component = W.component.getComponent(itemUid);
		var sourceComponent = W.component.getComponent(sourceContainerUid);
		var targetComponent = W.component.getComponent(targetContainerUid);
		targetComponent.addComponent(component);
		sourceComponent.dropSubComponent(component);

		//调用source component, target component的drag sort handler
		var $itemNode = $mobilePage.find('[data-cid="' + component.cid + '"]').eq(0);
		var $sourceNode = $mobilePage.find('[data-cid="' + sourceComponent.cid + '"]').eq(0);
		sourceComponent.dragSortHandler.handleComponentLeave($sourceNode, $itemNode, component);
		var $targetNode = $mobilePage.find('[data-cid="' + targetComponent.cid + '"]').eq(0);
		targetComponent.dragSortHandler.handleComponentEnter($targetNode, $itemNode, component);
	},

	/***********************************************************
	 * onFinishInitDesignPage: design page的designpage:finish_init事件的响应函数
	 ***********************************************************/
	onFinishInitDesignPage: function() {
		if (this.currentActivePage) {
			W.Broadcaster.trigger('component:select', this.currentActivePage, 'designpage:finish_init');
		}
	},

	/***********************************************************
	 * onWaitForPage: design page的designpage:wait_for_page事件的响应函数
	 ***********************************************************/
	onWaitForPage: function() {
		xlog('[page manager]: receive designpage:wait_for_page');
		if (this.currentActivePage) {
			xlog('[page manager]: lalala')
			W.Broadcaster.trigger('component:select', this.currentActivePage, 'designpage:wait_for_page');
		} else {
			xlog('[page manager]: but no this.currentActivePage');
		}
	},

	/***********************************************************
	 * onSelectPageComponentInDesignPage: design page的designpage:select_page_component事件的响应函数
	 * TODO: 不刷新页面
	 ***********************************************************/
	onSelectPageComponentInDesignPage: function() {
		/*
		var event = {};
		event.currentTarget = $('#pageManager li.page').get(0);
		this.onClickPage(event);
		*/
		W.Broadcaster.trigger('component:select', this.currentActivePage, {top: -26});
	},
});