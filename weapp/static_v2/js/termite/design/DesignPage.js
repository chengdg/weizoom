/**
 * @class W.mobile.Page
 * 页面
 */
W.design.isInFrame = (parent !== window);
W.design.DesignPage = Backbone.View.extend({
	events: {
		'click [data-ui-behavior="xub-selectable"]': 'onClickSelectableWidget',
		//'click a': 'onClickLink'
	},

	initialize: function(options) {
		xlog('[design page]: init design page');
		this.$el = $(this.el);
		this.$body = $('body');
		this.$window = null;
		this.isEnableSort = options.isEnableSort || false;
		
		if (W.design.isInFrame) {
			W.Broadcaster.on('component:select', this.onSelectPage, this);
			W.Broadcaster.on('component:finish_create', this.onAfterCreateComponent, this);
			W.Broadcaster.on('mobilewidget:select', this.onSelectWidget, this);
			W.Broadcaster.on('designpage:select_page_component', this.onSelectPageComponent, this);
			W.Broadcaster.on('designpage:cancel_delete', this.onCancelDelete, this);

			parent.$M = $;
		}

		this.coverManager = new W.design.CoverManager({
			el: 'body'
		});
		this.coverManager.on('widgetcover:delete-widget', this.onDeleteWidget, this);
		this.coverManager.on('widgetcover:add-widget', this.onAddWidget, this);

		//获得尺寸数据
		this.clientWidth = $('body').width();
		this.clientHeight = $('body').height();
		xlog('[design page]: ' + this.clientWidth + ', ' + this.clientHeight);

		//开启拖动排序
		_.delay(_.bind(function() {
			this.enableSortComponent();
		}, this), 500);

		this.$el.find('a').each(function() {
			var $link = $(this);
			$link.attr('href', 'javascript:void(0);')
		})

		if (W.design.isInFrame) {
			W.Broadcaster.trigger('designpage:finish_init');
			W.Broadcaster.trigger('designpage:resize');

			/*
			var $autoSelectComponent = $('[data-auto-select="true"]').eq(0);
			xwarn($autoSelectComponent);
			if ($autoSelectComponent) {
				var cid = $autoSelectComponent.data('cid');
				_.delay(function() {
					parent.W.Broadcaster.trigger('mobilewidget:select', cid);
				}, 200);
			}
			*/
		}
	},

	/**
	 * clearSelectedWidget: 清空当前widget的选中状态
	 */
	clearSelectedWidget: function() {
		//this.hideWidgetCover();
		this.coverManager.hide();
	},

	/**
	 * enableSortComponent: 开启拖动排序功能
	 */
	enableSortComponent: function() {
		var _this = this;
		$("div.wa-page").sortable({
			axis: 'y',
			opacity: '0.5',
			snap: true,
			scroll: true,
			placeholder: "xui-state-highlight",
			items: '[data-widget-sortable="true"]',
			/*items: '[data-cid]',*/
			start: function() {
				xlog('[design page]: start sort...');
				_this.clearSelectedWidget();
			},
			change: function(event, ui) {
				/*
				var placeHolderTop = ui.placeholder.offset().top;
				var clientHeight = document.body.clientHeight;
				var $window = $(window);
				var clientHeight = $window.height()-30; //30是phoneSkin的上下个15px的margin造成的
				var scrollTop = $window.scrollTop();
				if (placeHolderTop - scrollTop >= clientHeight - 30) {
					$window.scrollTop(scrollTop + 30);
				}
				if (placeHolderTop - scrollTop < 30) {
					var top = (scrollTop - 30);
					if (top < 0) {
						top = 0;
					}
					$window.scrollTop(top);
				}
				*/
			},
			sort: function(event, ui) {
				var $parent = $(parent.window);
				var parentScrollTop = $parent.scrollTop();
				var parentHeight = $parent.outerHeight();
				var marginTop = 303;
				var bottomDistanceThreshold = 90;
				var topDistanceThreshold = 40;
				var top = event.pageY;
				/*
				xwarn({
					parentScrollTop: parentScrollTop,
					parentHeight: parentHeight,
					top: top
				})
				xwarn('currentDistance:'+(parentHeight - (top + marginTop - parentScrollTop)) + ', targetDistance:' + bottomDistance);
				*/

				var bottomDistance = parentHeight - (top + marginTop - parentScrollTop);
				if (bottomDistance < bottomDistanceThreshold) {
					W.Broadcaster.trigger('designpage:reach_scroll_boundary', 'down');
				}

				var topDistance = top + marginTop - parentScrollTop;
				if (topDistance < topDistanceThreshold && (parentScrollTop > marginTop)) {
					W.Broadcaster.trigger('designpage:reach_scroll_boundary', 'top');
				}
			},
			stop: _.bind(function(event, ui) {
				xlog('[design page]: stop sort');

				//调整component关系, 如果$item继续在page下，则$container为空
				var $item = ui.item;
				//var $container = $item.parents('[data-ui-behavior~="xub-selectable"]').eq(0);
				var $container = $item.parents('[data-cid]').eq(0);
				var targetContainerCid = $container.length > 0 ? $container.attr('data-cid') : this.page.cid + '';
				var cid = $item.attr('data-cid');
				W.Broadcaster.trigger('designpage:drag_widget', this.$el, cid, targetContainerCid);
				W.Broadcaster.trigger('mobilewidget:select', cid);

				//调整顺序
				var orderedCids = [];
				_this.$('[data-ui-behavior~="xub-selectable"]').each(function() {
					var $widget = $(this);
					var cid = $widget.attr('data-cid');
					if (cid) {
						orderedCids.push(cid);
					}
				});
				W.Broadcaster.trigger('mobilepage:sort_widget', orderedCids);
			}, this)
		});
	},

	refreshPage: function(onPageFinished) {
		alert('请实现自己的refreshPage行为!');
	},

	renderComponentFromServer: function(component, onRenderFinished) {
		alert('请实现自己的renderComponentFromServer行为!');
	},

	/**
	 * onSelectPage: 选择page后的响应函数
	 */
	onSelectPage: function(component, respond_to_event) {
		xlog('[design page]: receive component:select with argument as page');
		W.Broadcaster.trigger('selectwidget:assert', component.cid);
		if (component.isRootPage()) {
			this.page = component;
			this.coverManager.setPage(this.page);

			//select auto_select component
			var $autoSelectComponent = $('[data-auto-select="true"]').eq(0);
			if ($autoSelectComponent) {
				var cid = $autoSelectComponent.data('cid');
				_.delay(function() {
					parent.W.Broadcaster.trigger('mobilewidget:select', cid);
				}, 200);
			}
		}        
	},

	onSelectPageComponent: function() {
		this.coverManager.hide();
	},

	insertComponentNode: function(component, $componentNode) {
		$componentNode.find('a').attr('href', 'javascript:void(0);');
		var $existedComponentNode = $('[data-cid="'+component.cid+'"]');
		if ($existedComponentNode.length > 0) {
			$existedComponentNode.eq(0).empty().append($componentNode.children());

			//this.coverManager.refresh();
			this.onSelectWidget(component.cid, {autoScroll:true, forceUpdatePropertyView:true});

			var height = document.body.clientHeight;
			W.Broadcaster.trigger('designpage:resize', height);
		} else {
			var prevComponent = this.page.getPrevComponentOf(component);
			if (prevComponent) {
				var $prevComponentNode = $('[data-cid="'+prevComponent.cid+'"]');
				xwarn('--------------1-------------------------');
				xwarn($prevComponentNode.length);
				xwarn($prevComponentNode);
				xwarn(prevComponent);
				$prevComponentNode.after($componentNode);
			} else {
				var nextComponent = this.page.getNextComponentOf(component);
				var $nextComponentNode = $('[data-cid="'+nextComponent.cid+'"]');
				xwarn('--------------2-------------------------');
				xwarn($nextComponentNode.length);
				xwarn(prevComponent);
				$nextComponentNode.before($componentNode);
			}
			//this.coverManager.refresh();
			this.onSelectWidget(component.cid, {autoScroll:true, forceUpdatePropertyView:true});

			var height = document.body.clientHeight;
			W.Broadcaster.trigger('designpage:resize', height);
		}
	},

	/**
	 * onAfterCreateComponent: 创建完component后的响应函数
	 */
	onAfterCreateComponent: function(page, component) {
		xlog('[design page]: finish create component, refresh page');
		var $componentAdder = $('.wa-componentadder');
		if ($componentAdder.is(':visible')) {
			$componentAdder.hide();
		}

		if (component.needServerRender) {
			parent.W.getLoadingView().show('加载后台数据');
			this.renderComponentFromServer(component, _.bind(function(componentHtml) {
				parent.W.getLoadingView().hide();
				var $componentNode = $(componentHtml);
				this.insertComponentNode(component, $componentNode);
			}, this));
		} else {
			var componentHtml = component.render();
			xwarn('=---------------------')
			xwarn(componentHtml);
			var $componentNode = $(componentHtml);
			this.insertComponentNode(component, $componentNode);
		}
	},

	selectWidgetNode: function($node, options) {
		if ($node.length === 0) {
			return;
		}

		var cid = parseInt($node.attr('data-cid'));
		var component = this.page.getComponentByCid(cid);

		//显示cover
		var isShowAction = true;
		if (component.hideSelectIndicator) {
			isShowAction = false;
		}
		this.coverManager.cover($node, {showAction: isShowAction});
		
		//抛出component:select事件
		if (options && options.silentForTriggerSelectComponent) {
		} else {
			if (component.onBeforeTriggerSelectComponent) {
				component.onBeforeTriggerSelectComponent($node);
			}
			var messageOptions = {};
			if (options && options.forceUpdatePropertyView) {
				messageOptions.forceUpdatePropertyView = options.forceUpdatePropertyView;
			}
			var offset = $node.offset();
			W.Broadcaster.trigger('component:select', component, offset, messageOptions);
		}
	},

	/**
	 * onSelectWidget: 选中cid指定的mobile widget
	 */
	onSelectWidget: function(cid, options) {
		xlog('[design page]: select mobile widget with cid: ' + cid);
		var $node = $('[data-cid="'+cid+'"]').eq(0);
		this.selectWidgetNode($node, options);

		//处理autoScroll
		if (options && options.autoScroll) {
			var $window = $(window);
			var clientHeight = $window.height()-30;
			var nodeTop = $node.offset().top;

			if (nodeTop < clientHeight) {
				//do nothing
			} else {
				$window.scrollTop(nodeTop - 100);
			}
			/*
			xlog('auto scroll to selected widget');
			xlog('clientHeight: ' + clientHeight);
			xlog('node top: ' + $node.offset().top);
			*/
		}
	},

	/**
	 * onClickSelectableWidget: 点击可选widget后的响应函数
	 */
	onClickSelectableWidget: function(event, options) {
		//调用changeComponentInDesignPageHandler
		if ($(event.target).hasClass('xa-action')) {
			//如果事件从action按钮发起，则忽略
			return;
		}

		var $node = $(event.currentTarget);
		this.selectWidgetNode($node);
	},

	/**
	 * onDeleteWidget: 收到cover manager的delete-widget event的响应函数
	 */
	onDeleteWidget: function(cid) {
		this.page.removeComponent(cid);
		$('[data-cid="'+cid+'"]').remove();
		if (!this.page.hasSubComponent()) {
			$('.wa-componentadder').show();
		}
		this.coverManager.hide();//.refresh();
		//this.refreshPage();
		W.Broadcaster.trigger('mobilepage:delete-widget');

		var height = document.body.clientHeight;
		W.Broadcaster.trigger('designpage:resize', height);
	},

	/**
	 * onAddWidget: 收到cover manager的add-widget event的响应函数
	 */
	onAddWidget: function(offset, relatedCid) {
		var componentAdders = _.filter(this.page.components, function(component) {
			return component.type.indexOf('.componentadder') !== -1;
		});
		if (componentAdders.length == 0) {
			return;
		}

		var componentAdder = componentAdders[0];
		this.onSelectWidget(relatedCid, {autoScroll:true, silentForTriggerSelectComponent:true});
		var relatedComponnet = this.page.getComponentByCid(relatedCid);
		W.Broadcaster.trigger('component:select', componentAdder, offset, {actionReferenceComponent:relatedComponnet, forceUpdatePropertyView:true});
	},

	/**
	 * onCancelDelete: 关闭删除弹层
	 */
	onCancelDelete: function(){
		var $dropdown = $('.dropdown-menu');
		if ($dropdown) {
			$dropdown.hide();
		}
	},

	onClickLink: function(event) {
		var $link = $(event.currentTarget);
		var href = $link.attr('href');
		if (href.indexOf('javascript:') === -1) {
			return false;
		}
	}
});
