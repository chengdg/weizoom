 /**
 * cover管理器
 * @class
 */
W.design.CoverManager = Backbone.View.extend({
    events: {
        'click #selectedWidgetCover_actionPanel_deleteButton': 'onClickDeleteWidgetButton'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.isEnableAction = options.isEnableAction || false;

        if ($('#selectedWidgetCover').length == 0) {
            xlog('create widget cover');
            var coverHtml = '<div id="selectedWidgetCover">' +
                '<div id="selectedWidgetCover_actionPanel">' + 
                '    <a href="javascript:void(0);" id="selectedWidgetCover_actionPanel_deleteButton" class="actionIcon actionIconPlus"></a>' + 
                '</div>' + 
            '</div>' + 
            '<div id="selectedWidgetHighlighter">' + 
            '</div>';
            this.$el.append(coverHtml);
        }
        xlog('[cover manager]: create cover');

        this.$selectedWidgetCover = $('#selectedWidgetCover');
        if (!this.isEnableAction) {
            this.$selectedWidgetCover.find('#selectedWidgetCover_actionPanel').hide();
        }
        this.$selectedWidgetHighlighter = $('#selectedWidgetHighlighter');

        this.cid2position = {}; //记录<widget.cid, position>的关系
        this.currentCidUnderMouse = null; //记录当前鼠标下的widget
        this.$insertIndicator = $('<div id="insertIndicator" data-ui-behavior="xub-selectable" data-cid="insert" class="xui-state-highlight" style="height: 5px; margin: 5px 0px;"></div>');
        this.insertIndicatorAttachedWidget = null;

        this.mouseMoveHandler = _.bind(this.onMouseMove, this);
        this.initMouseTracker();

        this.refresh();

        //监听component:resize事件
        W.Broadcaster.on('component:resize', this.onResizeComponent, this);
    }, 

    /**
     * 初始化鼠标移动监控机制
     */
    initMouseTracker: function() {
        //处理鼠标正常移动
        $(document).on('mousemove', this.mouseMoveHandler);
        //TODO: 优化变量位置
        this.NO_MOUSE_BUTTON_DOWN = 0;
        this.LEFT_MOUSE_BUTTON_DOWN = 1;
        this.RIGHT_MOUSE_BUTTON_DOWN = 2;
    },

    render: function() {

    },

    /**
     * updateWidgetPosition: 更新widget位置信息
     */
    updateWidgetPosition: function() {
        xlog('[cover manager]: update widget position')
        var cid2position = {}
        $('[data-cid]').each(function() {
            var $node = $(this);
            var isCircumInsertable = $node.attr('data-circum-insertable');
            if (!isCircumInsertable || "true" === isCircumInsertable) {
                var position = _.extend({}, $node.offset());
                position.width = $node.outerWidth();
                position.height = $node.outerHeight();
                cid2position[$node.attr('data-cid')] = position;
            }
        });
        this.cid2position = cid2position;

        parent.W.data.mobile.cid2position = cid2position;
    },

    /**
     * refresh: 更新cover
     */
    refresh: function() {
        var coveredCid = this.$selectedWidgetCover.attr('data-target-cid');
        var isCoverDisplayed = !!(coveredCid && parseInt(coveredCid) !== -1);
        var originalWidgetPosition = null;

        if (isCoverDisplayed) {
            var originalWidgetPosition = this.cid2position[coveredCid];
        }

        this.updateWidgetPosition();

        if (isCoverDisplayed) {
            var newWidgetPosition = this.cid2position[coveredCid];
            if (isCoverDisplayed) {
                if (newWidgetPosition.top !== originalWidgetPosition.top ||
                    newWidgetPosition.left !== originalWidgetPosition.left ||
                    newWidgetPosition.width !== originalWidgetPosition.width ||
                    newWidgetPosition.height !== originalWidgetPosition.height) {
                    this.coverWidget(coveredCid);
                }
            }
        }
    },

    /**
     * hide: 隐藏cover
     */
    hide: function() {
        this.$selectedWidgetCover.css({
            top: '-1000px'
        }).attr('data-target-cid', '-1');
        this.$selectedWidgetHighlighter.css({
            top: '-1000px'
        }).attr('data-target-cid', '-1');

        this.$('.xui-selectedWidget').removeClass('xui-selectedWidget');
    },

    /**
     * cover: 覆盖$node
     */
    cover: function($node) {
        var cid = $node.attr('data-cid');
        xlog('[cover manager]: cover ' + cid);
        if (cid) {
            xlog('[cover manager]: cover ' + cid);
            this.coverWidget(cid);
        }
    },

    /**
     * coverWidget: 覆盖cid指定的widget
     */
    coverWidget: function(cid, options) {
        if (options && options.ignoreHighlighter) {
            //do nothing
        } else {
            this.$selectedWidgetHighlighter.css({
                top: '-1000px'
            }).attr('data-target-cid', '-1');
        }

        var position = this.cid2position[cid];
        this.$selectedWidgetCover.css({
            top: position.top + 'px',
            left: position.left + 'px',
            width: position.width - 4 + 'px',
            height: position.height - 2 + 'px'
        }).attr('data-target-cid', cid);
    },

    /**
     * highlightWidget: 显示cid指定的widget的高亮选中框
     */
    highlightWidget: function(cid) {
        var $node = $('[data-cid="' + cid + '"]');
        if ($node) {
            var position = this.cid2position[cid];
            this.$selectedWidgetHighlighter.css({
                top: position.top + 'px',
                left: position.left + 'px',
                width: position.width - 4 + 'px',
                height: position.height + 'px'
            }).attr('data-target-cid', $node.attr('data-cid'));
        }
    },

    /**
     * onClickDeleteWidgetButton: 点击删除widget按钮的响应函数
     */
    onClickDeleteWidgetButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var cid = this.$selectedWidgetCover.attr('data-target-cid');
        this.trigger('widgetcover:delete-widget', cid);
    },

    /**
     * getWidgetUnderMouse: 遍历widget的position，获得鼠标下的widget
     */
    getWidgetUnderMouse: function(mousePosition, options) {
        var targetCid = null;
        var distance = 99999999;
        _.each(this.cid2position, function(position, cid) {
            var top = position.top;
            var left = position.left;
            var right = left + position.width;
            var bottom = top + position.height;
            if (options && options.ignoreWidgetWidth) {
                //如果设置了忽略widget的width，则将边界放宽
                left = -1;
                right = 100000;
            }
            if (mousePosition.x >= left && mousePosition.x <= right) {
                if (mousePosition.y >= top && mousePosition.y <= bottom) {
                    var currentDistance = (mousePosition.x-left)*(mousePosition.x-left) + (mousePosition.y-top)*(mousePosition.y-top);
                    if (currentDistance < distance) {
                        distance = currentDistance;
                        targetCid = cid;
                    }
                }
            }
        });

        return targetCid;
    },

    /**
     * getFirstWidgetOnTopOfMouse: 遍历widget的position，获得沿y轴在鼠标上方，离鼠标最近的widget
     */
    getFirstWidgetOnTopOfMouse: function(mousePosition) {
        var targetCid = null;
        var targetInsertPosition = null;
        var targetYDistance = 100000;
        var targetXDistance = 100000;
        _.each(this.cid2position, function(position, cid) {
            var x = mousePosition.x;
            var y = mousePosition.y;
            var left = position.left;
            var right = position.left + position.width;
            var top = position.top;
            var height = position.height;

            if (mousePosition.y < top) {
                //widget在鼠标下方，忽略
                return;
            } if (x < left || x > right) {
                //鼠标不在widget的x轴范围内，忽略
                return;
            }else {
                if (top + height < mousePosition.y) {
                    //鼠标在widget之外
                    var currentYDistance = mousePosition.y - top - height;
                    var insertPosition = 'after';
                } else {
                    //鼠标在widget之内
                    var currentYDistance = mousePosition.y - top;
                    var insertPosition = "before";
                }
                if (currentYDistance < targetYDistance) {
                    targetCid = cid;
                    targetInsertPosition = insertPosition;
                    targetYDistance = currentYDistance;
                }
                /*
                if (currentYDistance === targetYDistance) {
                    var x = mousePosition.x;
                    var left = position.left;
                    var right = position.left + position.width;
                    if (left <= x && x <= right) {
                        targetCid = cid;
                        targetInsertPosition = insertPosition;
                    }
                }
                */
            }
        });
        xlog('[cover manager]: found first top widget ' + targetCid + ' with distance (' + targetYDistance + ')');
        return {cid: targetCid, insertPosition: targetInsertPosition};
    },

    /**
     * handleDragParentComponent: 拖动component img时，显示mobile page中的insert indicator的处理函数
     */
    handleDragParentComponent: function(event, x, y) {
        if (event === 'drag') {
            //TODO: 将getWidgetUnderMouse改为寻找离y值最近的widget
            var widget = this.getFirstWidgetOnTopOfMouse({x:x, y:y});
            var cid = widget.cid;
            if (cid) {
                if (this.insertIndicatorAttachedWidget &&
                    this.insertIndicatorAttachedWidget.cid === cid && 
                    this.insertIndicatorAttachedWidget.insertPosition === widget.insertPosition) {
                    xlog('skip. keep ' + cid);
                    return;
                } else {
                    this.insertIndicatorAttachedWidget = widget;
                    this.hide();
                    var $node = $('[data-cid="' + cid + '"]');
                    if (widget.insertPosition === 'before') {
                        xlog('insert before widget ' + cid);
                        this.$insertIndicator.insertBefore($node);
                    } else {
                        xlog('insert after widget ' + cid);
                        this.$insertIndicator.insertAfter($node);
                    }
                }
            } else {
                xlog('cid is null');
            }
        } else if (event === 'leave') {
            this.insertIndicatorAttachedWidget = null;
            this.$insertIndicator.hide().detach();
        } else if (event === 'enter') {
            this.$insertIndicator.show();
            this.insertIndicatorAttachedWidget = null;
            this.hide();
        }
    },

    /**
     * getInsertIndicatorLayout: 获得insert indicator的布局信息
     */
    getInsertIndicatorLayout: function() {
        xlog('getInsertIndicatorLayout...');
        var layout = {$mobilePage: $('div.ui-page')};
        var $container = this.$insertIndicator.parents('[data-component-container="true"]').eq(0);
        layout.pid = $container.length > 0 ? $container.attr('data-cid') : 'page';

        //调整顺序
        var orderedCids = [];
        $('[data-ui-behavior~="xub-selectable"]').each(function() {
            var $widget = $(this);
            var cid = $widget.attr('data-cid');
            if (cid) {
                orderedCids.push(cid);
            }
        });
        layout.orderedCids = orderedCids;

        return layout;
    },

    /**
     * onMouseOverSelectableWidget: 鼠标移入selectable widget
     */
    onMouseMove: function(event) {
        if (event.buttons !== this.NO_MOUSE_BUTTON_DOWN) {
            return;
        }

        var mouseX = event.pageX;
        var mouseY = event.pageY;
        var cid = this.getWidgetUnderMouse({x:mouseX, y:mouseY});
        if (cid !== this.currentCidUnderMouse) {
            this.currentCidUnderMouse = cid;

            if (!cid) {
                return;
            }
        
            //忽略已选中的component
            var currentSelectedWidgetCid = parseInt(this.$selectedWidgetCover.attr('data-target-cid'));
            if (cid == currentSelectedWidgetCid) {
                return;
            }

            //对component进行高亮
            this.highlightWidget(cid);
        }
    },

    /**
     * onResizeComponent: 监听到component:resize event的响应函数
     */
    onResizeComponent: function(component) {
        this.refresh();
    },

    /**
     * onBeforeReload: mobilepage:before_reload事件的响应函数
     */
    onBeforeReload: function() {
        /*
        console.log('[cover manager]: off event handlers');
        W.Broadcaster.off('component:resize', this.onResizeComponent, this);
        $(document).off('mousemove', this.mouseMoveHandler);
        */
    }
});