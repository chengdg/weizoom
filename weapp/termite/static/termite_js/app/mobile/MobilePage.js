/**
 * @class W.mobile.Page
 * 页面
 */
W.mobile.isInFrame = (parent !== window);
W.mobile.MobilePage = Backbone.View.extend({
    events: {
        'click [data-ui-behavior~="xub-selectable"]': 'onClickSelectableWidget'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$body = $('body');
        xlog('init mobile page');

        if (W.mobile.isInFrame) {
            W.ParentBroadcaster.on('component:select', this.onSelectPage, this);
            W.ParentBroadcaster.on('component:finish_create', this.onAfterCreateComponent, this);
            W.ParentBroadcaster.on('mobilewidget:select', this.onSelectWidget, this);
            W.ParentBroadcaster.on('mobilepage:before_reload', this.onBeforeReload, this);
            W.ParentBroadcaster.on('mobilepage:refresh', this.onRefreshPage, this);

            this.page = parent.W.workbench.PageManagerView.currentActivePage; //初始化    
            parent.$M = $;
            parent.W.util.mobilePageDragComponentHandler = _.bind(this.onDragParentComponent, this);
            parent.W.util.getInsertIndicatorLayoutInMobilePage = _.bind(this.getInsertIndicatorLayout, this);
            xlog('set parent.$M');
        }

        this.coverManager = new W.mobile.CoverManager({
            el: 'body'
        });
        this.coverManager.on('widgetcover:delete-widget', this.onDeleteWidget, this);

        //获得尺寸数据
        this.clientWidth = $('body').width();
        this.clientHeight = $('body').height();
        xlog('[mobile page]: ' + this.clientWidth + ', ' + this.clientHeight);

        if (W.mobile.isInFrame) {
            W.ParentBroadcaster.trigger('mobilepage:finish_init');
        }

        this.$window = null;
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
                var clientHeight = $window.height() - 30; //30是phoneSkin的上下个15px的margin造成的
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
                W.ParentBroadcaster.trigger('mobilepage:drag_widget', this.$el, $item.attr('data-cid'), targetContainerCid);

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
                W.ParentBroadcaster.trigger('mobilepage:sort_widget', orderedCids);
            }, this)
        });
    },

    refreshPage: function(onPageFinished) {
        this.coverManager.hide();

        this.$el.detach();
        xlog('[iframe]: destroy page');
        $('div.ui-content').sortable('destroy');
        this.$el.page('destroy');
        this.$el.find('*').remove();

        var _this = this;
        W.getApi().call({
            app: 'workbench',
            api: 'mobile_page/create',
            method: 'post',
            args: {
                page: JSON.stringify(this.page.toJSON())
            },
            success: function(data) {
                _this.$el.append(data);
                _this.$el.prependTo($('body'));
                _this.$el.page();

                //_this.coverManager.updateWidgetPosition();
                _this.coverManager.refresh();
                _this.enableSortComponent();

                if (onPageFinished) {
                    onPageFinished();
                }
            },
            error: function(resp) {
                //console.error("Error: in ViperDesignPage. Msg: " + resp);
                alert('渲染页面失败');
            }
        });
    },

    /**
     * onSelectPage: 选择page后的响应函数
     */
    onSelectPage: function(component) {
        xlog('[iframe]: receive component:select');
        if (component.type.indexOf('.page') === -1) {
            return;
        }

        this.page = component;
        this.refreshPage();
    },

    /**
     * onAfterCreateComponent: 创建完component后的响应函数
     */
    onAfterCreateComponent: function(page, component) {
        xlog('[iframe]: finish create component, refresh page');
        this.refreshPage(_.bind(function() {
            this.onSelectWidget(component.cid, {
                autoScroll: true
            });
        }, this));
    },

    /**
     * onRefreshPage: 刷新mobile page
     */
    onRefreshPage: function(page, component) {
        alert('ha');
        xlog('[mobile page]: refresh page');
        this.refreshPage();
    },

    /**
     * onBeforeReload: mobilepage:before_reload事件的响应函数
     */
    onBeforeReload: function() {
        xlog('[mobile page]: off event handler');
        W.ParentBroadcaster.off('component:select', this.onSelectPage, this);
        W.ParentBroadcaster.off('component:finish_create', this.onAfterCreateComponent, this);
        W.ParentBroadcaster.off('mobilewidget:select', this.onSelectWidget, this);
        W.ParentBroadcaster.off('mobilepage:before_reload', this.onBeforeReload, this);
        this.coverManager.off('widgetcover:delete-widget', this.onDeleteWidget, this);

        this.coverManager.onBeforeReload();
    },

    /**
     * onSelectWidget: 选中cid指定的mobile widget
     */
    onSelectWidget: function(cid, options) {
        xlog('[iframe]: select mobile widget with cid: ' + cid);
        var event = {};
        $('[data-cid="' + cid + '"]').each(function() {
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
            var clientHeight = $window.height() - 30;
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
        W.ParentBroadcaster.trigger('component:select', component);
    },

    /**
     * onDeleteWidget: 收到cover manager的delete-widget event的响应函数
     */
    onDeleteWidget: function(cid) {
        this.page.removeComponent(cid);

        this.refreshPage();
        W.ParentBroadcaster.trigger('mobilepage:delete-widget');
    },

    /**
     * onDragParentComponent: 收到cover manager的delete-widget event的响应函数
     */
    onDragParentComponent: function(event, x, y, options) {
        if (event === 'enter' || event === 'leave') {
            this.coverManager.handleDragParentComponent(event, x, y + scrollTop);
        } else if (event === 'drag') {
            if (!this.$window) {
                this.$window = $(window);
            }
            var $window = this.$window;
            var scrollTop = $window.scrollTop();
            if (options && !options.inScrollTriggerArea) {
                //显示insert indicator
                this.coverManager.handleDragParentComponent(event, x, y + scrollTop);
            } else {
                //滚动
                var clientHeight = $window.height() - 30; //30是phoneSkin的上下个15px的margin造成的
                if (y >= clientHeight - 30 && options.inScrollTriggerArea === 'bottom') {
                    //向下滚动
                    $window.scrollTop(scrollTop + 30);
                } else if (scrollTop > 0 && options.inScrollTriggerArea === 'top') {
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
