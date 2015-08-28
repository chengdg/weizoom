/**
 * cover管理器
 * @class
 */
W.design.CoverManager = Backbone.View.extend({
    events: {
        'click .xa-delete': 'onClickDeleteWidgetButton',
        'click .xa-add': 'onClickAddWidgetButton',
        'mouseenter .xa-componentContainer': 'onEnterSelectableWidget',
        'mouseleave .xa-componentContainer': 'onLeaveSelectableWidget'
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.initMouseTracker();

        this.$coveredWidget = null;
        this.currentSelectedWidgetCid = -1;

        //监听component:resize事件
        W.Broadcaster.on('component:resize', this.onResizeComponent, this);
    }, 

    /**
     * 初始化鼠标移动监控机制
     */
    initMouseTracker: function() {
        //处理鼠标正常移动
        xlog("[cover manager]: init mouse tracker");
        //$(document).on('mousemove', this.mouseMoveHandler);
        //TODO: 优化变量位置
        this.NO_MOUSE_BUTTON_DOWN = 0;
        this.LEFT_MOUSE_BUTTON_DOWN = 1;
        this.RIGHT_MOUSE_BUTTON_DOWN = 2;
    },

    render: function() {

    },

    setPage: function(page) {
        this.page = page;
    },

    /**
     * hide: 隐藏cover
     */
    hide: function() {
        xlog('[cover manager]: hide cover');

        if (this.$coveredWidget) {
            this.$coveredWidget.find('.xa-actionPanel').hide();
            this.$coveredWidget.find('.xa-selectIndicator').hide();
        }
        this.$coveredWidget = null;
        this.currentSelectedWidgetCid = -1;
        return this;
    },

    /**
     * cover: 覆盖$node
     */
    cover: function($node, options) {
        var cid = $node.attr('data-cid');
        if (!cid) {
            return;
        }

        cid = parseInt(cid);
        if (cid == this.currentSelectedWidgetCid) {
            xwarn('return directly');
            return;
        }

        xwarn('current: ' + this.currentSelectedWidgetCid);
        xwarn('new: ' + cid);
        if (this.$coveredWidget) {
            xwarn(this.$coveredWidget.find('.xa-actionPanel').get(0));
        xwarn(this.$coveredWidget.find('.xa-selectIndicator').get(0));
            this.$coveredWidget.find('.xa-actionPanel').hide();
            this.$coveredWidget.find('.xa-selectIndicator').hide();
        }

        this.$coveredWidget = $node;
        this.currentSelectedWidgetCid = parseInt(cid);
        xlog('[cover manager]: cover ' + cid);
        this.coverWidget(options);
    },

    /**
     * coverWidget: 覆盖cid指定的widget
     */
    coverWidget: function(options) {
        var showAction = true;
        if (options.hasOwnProperty('showAction')) {
            showAction = options.showAction;
        }
        if (showAction && this.$coveredWidget) {
            xwarn('show action panel');
            var $actionPanel = this.$coveredWidget.find('.xa-actionPanel');
            $actionPanel.show();
            /*
            if (!$actionPanel.is(':visible')) {
                $actionPanel.show();
            }
            */
        }
        //活动报名不显示新增，删除
        if ((window.location.href).indexOf('event') != -1){
            this.$coveredWidget.find('.xa-add').hide();
            this.$coveredWidget.find('.xa-delete').hide();
        }
        this.$coveredWidget.find('.xa-selectIndicator').show();
    },

    refresh: function() {
        if (this.$coveredWidget) {
            //活动报名不显示新增，删除
            if ((window.location.href).indexOf('event') != -1) {
                this.$coveredWidget.find('.xa-add').hide();
                this.$coveredWidget.find('.xa-delete').hide();
            } else {
            this.$coveredWidget.find('.xa-actionPanel').show();
            this.$coveredWidget.find('.xa-selectIndicator').show();
            }
        }
    },

    /**
     * onClickDeleteWidgetButton: 点击删除widget按钮的响应函数
     */
    onClickDeleteWidgetButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var _this = this;
        W.requireConfirm({
            $el: $(event.currentTarget),
            width: 240,            
            position: 'top',
            isTitle: false,
            show_icon: false,
            isArrow: false,
            msg: '确认删除？',
            confirm: function() {      
                this.close();          
                //var cid = _this.$selectedWidgetCover.attr('data-target-cid');
                var $button = $(event.currentTarget);
                var $componentContainer = $button.parents('.xa-componentContainer');
                var cid = $componentContainer.attr('data-cid');
                _this.trigger('widgetcover:delete-widget', cid);
            }
        });
    },

    /**
     * onClickAddWidgetButton: 点击添加widget按钮的响应函数
     */
    onClickAddWidgetButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $button = $(event.currentTarget);
        var offset = $button.offset();
        if (offset) {
            offset.top += 20; //添加按钮的高度为20px
        }

        var $componentContainer = $button.parents('.xa-componentContainer');
        var cid = $componentContainer.attr('data-cid');
        this.trigger('widgetcover:add-widget', offset, cid);
    },

    /**
     * onResizeComponent: 监听到component:resize event的响应函数
     */
    onResizeComponent: function(component) {
        xlog('[cover manager]: handle component:resize...');
        W.Broadcaster.trigger('designpage:resize');
    },

    /**
     * onBeforeReload: mobilepage:before_reload事件的响应函数
     */
    onBeforeReload: function() {
        console.log('[cover manager]: off event handlers');
        W.Broadcaster.off('component:resize', this.onResizeComponent, this);
        //$(document).off('mousemove', this.mouseMoveHandler);
    },

    onEnterSelectableWidget: function(event) {
        if (event.which !== this.NO_MOUSE_BUTTON_DOWN) {
            //有鼠标键按下，直接返回
            return;
        }

        var $componentContainer = $(event.currentTarget);
        var cid = $componentContainer.data('cid');
        if (!cid) {
            return; 
        }

        //忽略已选中的component
        if (cid == this.currentSelectedWidgetCid) {
            return;
        }

        if (this.page) {
            var component = this.page.getComponentByCid(cid);
            if (component.hideSelectIndicator) {
                return;
            }
        }
        //活动报名不显示新增，删除
        if ((window.location.href).indexOf('event') != -1){
            $componentContainer.find('.xa-add').hide();
            $componentContainer.find('.xa-delete').hide();
        }
        else{
            $componentContainer.find('.xa-actionPanel').show();
            $componentContainer.find('.xa-selectIndicator').show();
            //this.highlightWidget(cid);
        }

    },


    onLeaveSelectableWidget: function(event) {
        if (event.which !== this.NO_MOUSE_BUTTON_DOWN) {
            //有鼠标键按下，直接返回
            return;
        }
        xlog('[cover manager] leave widget');
        var $componentContainer = $(event.currentTarget);

        var leavedCid = parseInt($componentContainer.attr('data-cid'));
        if (leavedCid != this.currentSelectedWidgetCid) {
            $componentContainer.find('.xa-actionPanel').hide();
            $componentContainer.find('.xa-selectIndicator').hide();
        }
    },
});