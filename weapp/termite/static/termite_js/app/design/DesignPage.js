/**
 * @class W.mobile.Page
 * 页面
 */
W.design.isInFrame = (parent !== window);
W.design.DesignPage = Backbone.View.extend({
    events: {
        'click [data-ui-behavior="xub-selectable"]': 'onClickSelectableWidget'
    },

    initialize: function(options) {
        xlog('[design page]: init design page');
        this.$el = $(this.el);
        this.$body = $('body');
        this.$window = null;
        this.isEnableAction = options.isEnableAction || false;
        this.isEnableSort = options.isEnableSort || false;

        if (W.design.isInFrame) {
            W.Broadcaster.on('component:select', this.onSelectPage, this);
            W.Broadcaster.on('component:finish_create', this.onAfterCreateComponent, this);
            W.Broadcaster.on('mobilewidget:select', this.onSelectWidget, this);
            W.Broadcaster.on('mobilepage:before_reload', this.onBeforeReload, this);
	        W.Broadcaster.on('designpage:refresh', this.onRefreshPage, this);
	        W.Broadcaster.on('designpage:screenshot', this.onTakeScreenshot, this);

            this.page = parent.W.workbench.PageManagerView.currentActivePage; //初始化    
            parent.$M = $;
            parent.W.util.mobilePageDragComponentHandler = _.bind(this.onDragParentComponent, this);
            parent.W.util.getInsertIndicatorLayoutInMobilePage = _.bind(this.getInsertIndicatorLayout, this);
        }

        this.coverManager = new W.design.CoverManager({
            el: 'body',
            isEnableAction: this.isEnableAction
        });
        this.coverManager.on('widgetcover:delete-widget', this.onDeleteWidget, this);

        //获得尺寸数据
        this.clientWidth = $('body').width();
        this.clientHeight = $('body').height();
        xlog('[design page]: ' + this.clientWidth + ', ' + this.clientHeight);

        //开启拖动排序
        var enableSortTask = new W.DelayedTask(function() {
            this.enableSortComponent();
        }, this);
        enableSortTask.delay(500);

        if (W.design.isInFrame) {
            W.Broadcaster.trigger('designpage:finish_init');
        }

        $(document).click(function(event) {
            if (W.isSystemManager) {
                return;
            } else {
                if ((event.which === 1) && (event.currentTarget === document)) {
                    var task = new W.DelayedTask(function() {
                        xlog('[design page]: trigger designpage:select_page_component');
                        W.Broadcaster.trigger('designpage:select_page_component');
                    });
                    task.delay(100);
                }
            }
        })
    },

    /**
     * clearSelectedWidget: 清空当前widget的选中状态
     */
    clearSelectedWidget: function() {
        //this.hideWidgetCover();
        this.coverManager.hide();
        this.$('.xui-selectedWidget').removeClass('xui-selectedWidget');
    },

    /**
     * enableSortComponent: 开启拖动排序功能
     */
    enableSortComponent: function() {
        var _this = this;
        $("div.ui-content").sortable({
            axis: 'y',
            opacity: '0.2',
            snap: true,
            scroll: true,
            placeholder: "xui-state-highlight",
            items: '[data-ui-sortable="true"]',
            /*items: '[data-cid]',*/
            start: function() {
                xlog('[iframe]: start sort...');
                _this.clearSelectedWidget();
            },
            change: function(event, ui) {
                var placeHolderTop = ui.placeholder.offset().top;
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
            },
            stop: _.bind(function(event, ui) {
                xlog('[iframe]: stop now');

                //调整component关系, 如果$item继续在page下，则$container为空
                var $item = ui.item;
                //var $container = $item.parents('[data-ui-behavior~="xub-selectable"]').eq(0);
                var $container = $item.parents('[data-cid]').eq(0);
                var targetContainerCid = $container.length > 0 ? $container.attr('data-cid') : this.page.cid + '';
                W.Broadcaster.trigger('mobilepage:drag_widget', this.$el, $item.attr('data-cid'), targetContainerCid);

                //调整
                _this.coverManager.refresh();

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

    /**
     * onSelectPage: 选择page后的响应函数
     */
    onSelectPage: function(component, respond_to_event) {
        xlog('[design page]: receive component:select with argument as page');
        if (component.isRootPage()) {
            this.page = component;
            if (respond_to_event == 'designpage:finish_init' || respond_to_event == 'designpage:wait_for_page') {

            } else {
                //this.refreshPage();        
                /*
                if (this.isEnableAction) {

                } else {
                    var href = window.location.href;
                    window.location.href = href.replace(/page_id=\d/g, 'page_id='+this.page.cid);
                }
                */
                var href = window.location.href;
                window.location.href = href.replace(/page_id=\d+/g, 'page_id='+this.page.cid);
            }    
        }        
    },

    /**
     * onAfterCreateComponent: 创建完component后的响应函数
     */
    onAfterCreateComponent: function(page, component) {
        xlog('[design page]: finish create component, refresh page');
        this.refreshPage(_.bind(function() {
            this.onSelectWidget(component.cid, {autoScroll: true});
        }, this));
    },

    /**
     * onRefreshPage: 刷新mobile page
     */
    onRefreshPage: function(page, component) {
        xlog('[mobile page]: refresh page');
        this.refreshPage();
    },

    /**
     * onBeforeReload: mobilepage:before_reload事件的响应函数
     */
    onBeforeReload: function() {
        /*
        xlog('[mobile page]: off event handler');
        W.Broadcaster.off('component:select', this.onSelectPage, this);
        W.Broadcaster.off('component:finish_create', this.onAfterCreateComponent, this);
        W.Broadcaster.off('mobilewidget:select', this.onSelectWidget, this);
        W.Broadcaster.off('mobilepage:before_reload', this.onBeforeReload, this);
        this.coverManager.off('widgetcover:delete-widget', this.onDeleteWidget, this);

        this.coverManager.onBeforeReload();
        */
    },

    /**
     * onSelectWidget: 选中cid指定的mobile widget
     */
    onSelectWidget: function(cid, options) {
        xlog('[iframe]: select mobile widget with cid: ' + cid);
        var event = {};
        $('[data-cid="'+cid+'"]').each(function() {
            var $node = $(this);
            if ($node.hasClass('xui-selectedWidget')) {
                return;
            }
            event.currentTarget = $node;
        })

        event.stopPropagation = $.noop;
        event.preventDefault = $.noop;
        this.onClickSelectableWidget(event);

        //处理autoScroll
        if (options && options.autoScroll) {
            var $node = event.currentTarget;
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
    onClickSelectableWidget: function(event) {
        //调用changeComponentInDesignPageHandler
        var handlerCount = parent.W.util.changeComponentInDesignPageHandlers.length;
        for (var i = 0; i < handlerCount; ++i) {
            var handler = parent.W.util.changeComponentInDesignPageHandlers[i];
            if (!handler()) {
                //如果handler返回false，则不进行select操作
                return;
            }
        }

        event.stopPropagation();
        event.preventDefault();

        var $node = $(event.currentTarget);
        if ($node.hasClass('xui-selectedWidget')) {
            return;
        }

        //高亮边框
        this.$('.xui-selectedWidget').removeClass('xui-selectedWidget');
        $node.addClass('xui-selectedWidget');

        //显示cover
        this.coverManager.cover($node);
        
        //抛出component:select事件
        var cid = parseInt($node.attr('data-cid'));
        var component = this.page.getComponentByCid(cid);
        W.Broadcaster.trigger('component:select', component);
    },

    /**
     * onDeleteWidget: 收到cover manager的delete-widget event的响应函数
     */
    onDeleteWidget: function(cid) {
        this.page.removeComponent(cid);

        this.refreshPage();
        W.Broadcaster.trigger('mobilepage:delete-widget');
    },

    /**
     * onTakeScreenshot: 收到designpage:screenshot事件的响应函数
     */
    onTakeScreenshot: function(callback) {
        this.clearSelectedWidget();
        html2canvas(document.body, {
            onrendered: function(canvas) {
                if (callback) {
                    var dataUrl = canvas.toDataURL("image/jpg");
                    callback(dataUrl);
                    //var imgData = dataUrl.replace(/^data:image\/(png|jpg);base64,/, "");
                }
            },
            height: 480
        });
    },

    /**
     * onDragParentComponent: 收到cover manager的delete-widget event的响应函数
     */
    onDragParentComponent: function(event, x, y, options) {
        if (event === 'enter' || event === 'leave') {
            this.coverManager.handleDragParentComponent(event, x, y+scrollTop);
        } else if (event === 'drag') {
            if (!this.$window) {
                this.$window = $(window);
            }
            var $window = this.$window;
            var scrollTop = $window.scrollTop();
            if (options && !options.inScrollTriggerArea) {
                //显示insert indicator
                this.coverManager.handleDragParentComponent(event, x, y+scrollTop);
            } else {
                //滚动
                var clientHeight = $window.height()-30; //30是phoneSkin的上下个15px的margin造成的
                if (y >= clientHeight - 30 && options.inScrollTriggerArea === 'bottom') {
                    //向下滚动
                    $window.scrollTop(scrollTop + 30);
                }
                else if (scrollTop > 0 && options.inScrollTriggerArea === 'top') {
                    //向上滚动
                    scrollTop -= 30;
                    if (scrollTop < 0) {
                        scrollTop = 0;
                    }
                    $window.scrollTop(scrollTop);
                }
            }
        }
    },

    /**
     * getInsertIndicatorLayout: 获得insert indicator的布局信息
     */
    getInsertIndicatorLayout: function() {
        var layout = this.coverManager.getInsertIndicatorLayout();
        if (layout.pid === 'page') {
            layout.pid = this.page.cid + '';
        }
        return layout;
    }
});
