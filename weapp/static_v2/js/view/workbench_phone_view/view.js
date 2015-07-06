/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 手机模拟器
 * @class
 */
ensureNS('W.workbench');
W.workbench.PhoneView = Backbone.View.extend({
	el: '',

	events: {
        'click .xa-title': 'onClickTitle'
	},
	
	initialize: function(options) {
        this.$el = $(this.el);

        this.$cover = this.$('#phoneSkinCover');

        //W.Broadcaster.on('component:start_drag', this.onStartDragComponent, this);
        //W.Broadcaster.on('component:stop_drag', this.onStopDragComponent, this);
        //W.Broadcaster.on('component:drag', this.onDraggingComponent, this);
        W.Broadcaster.on('designpage:resize', this.onResizeDesignPage, this);
        W.Broadcaster.on('designpage:update_site_title', this.onUpdateSiteTitle, this);

        //this.enableDroppable();

        this.isDragWithinPhone = false; //鼠标拖动是否在phone的范围内

        //初始化offset
        var $iframe = this.$('#phoneSkin > iframe');
        var offset = $iframe.offset();
        this.left = offset.left;
        this.top = offset.top;
        this.height = $iframe.outerHeight();
        this.width = $iframe.outerWidth();
        this.bottom = this.top + this.height;
        this.right = this.left + this.width;
        this.compareTmpl = _.template('[phone view]: compare (<%=x%>, <%=y%>) to phone top(<%=top%>), left(<%=left%>), width(<%=width%>), height(<%=height%>)');
        this.$skin = this.$('.xui-i-skin');
        this.$title = this.$('.xa-title');
	},

    render: function() {
        //this.$el.append($.tmpl(this.getTemplate(), {}));
        this.onResizeDesignPage();
        this.startMonitor();
        return this;
    },

    startMonitor: function() {
        var _this = this;
        var monitor = function() {
            var frameHeight = window.frames['phoneFrame'].document.body.clientHeight;
            var phoneHeight = _this.$skin.height();
            if (phoneHeight <= frameHeight+45) {
                _this.$skin.height(frameHeight+50+'px');    
            }       
        }
        setInterval(monitor, 200);
    },

    /**
     * onStartDragComponent
     */
    /*
    onStartDragComponent: function() {
        xlog('onStartDragComponent...');
        this.$cover.show();
    },
    *.

    /**
     * onStopDragComponent
     */
    /*
    onStopDragComponent: function(event, ui) {
        xlog('onStopDragComponent...');
        this.$cover.hide();
        this.isDragWithinPhone = false;
    },
    */

    /**
     * shouldTriggerMobilePageToHandleDrag: 是否触发mobile page处理drag
     */
    /*
    shouldTriggerMobilePageToHandleDrag: function(x, y) {
        if (x <= 0) { return false;} //超出左边界
        if (this.width - x <= 20) { return false; } //超出右边界
        if (y <= 0) { return false; } //超出上边界

        if (!this.isDragWithinPhone) {
            //jquery ui判断不在phone内
            var distanceToBottom = (this.height - y);
            if (distanceToBottom > 1 && distanceToBottom < 50) {
                return true;
            } else {
                return false;
            }
        }

        return true;
    },
    */

    /**
     * checkInScrollTriggerArea: 检查是否在scroll触发区内
     */
    /*
    checkInScrollTriggerArea: function(x, y) {
        if (y > 0 && y <=10) { 
            return 'top'; 
        }

        var distanceToBottom = (this.height - y);
        if (distanceToBottom > 0 && distanceToBottom < 20) {
            return 'bottom';
        }

        return null;
    },
    */

    /**
     * onDraggingComponent: 鼠标拖动时的响应函数
     */
    /*
    onDraggingComponent: function(event, ui) {
        var x = event.originalEvent.clientX - this.left;
        var y = event.originalEvent.clientY - this.top;
        var info = this.compareTmpl.render({
            x: x,
            y: y,
            top: this.top,
            left: this.left,
            width: this.width,
            height: this.height
        });

        if (this.shouldTriggerMobilePageToHandleDrag(x, y)) {
            var options = {inScrollTriggerArea: this.checkInScrollTriggerArea(x, y)};
            if (!options.inScrollTriggerArea) {
                console.warn('trigger mobile page, but NOT trigger scroll');    
            } else {
                console.warn('trigger mobile page and scroll');
            }
            W.util.mobilePageDragComponentHandler('drag', x, y, options);            
        } else {
            console.warn('NOT trigger mobile page');
        }
    },
    */

    onResizeDesignPage: function(height) {
        if (!height) {
            if (!window.frames['phoneFrame'].document.body) {
                return;
            }
            height = window.frames['phoneFrame'].document.body.clientHeight;
        }
        xlog("[phone view]: change height to " + height + 'px');
        this.$skin.height(height+50+'px');
    },

    onUpdateSiteTitle: function(title) {
        this.$title.text(title);
    },

    /**
     * enableDroppable: 开启droppable功能
     */
    /*
    enableDroppable: function() {
        var _this = this;
        var dropOptions = {
            accept: function(el) {
                return el.hasClass('xui-component');
            },
            activeClass: 'xui-droppable-active',
            over: function() {
                xlog('over phone...');
                _this.isDragWithinPhone = true;
                W.util.mobilePageDragComponentHandler('enter');
            },
            out: function(event, ui) {
                xlog('out phone...');
                _this.isDragWithinPhone = false;
                var x = event.originalEvent.clientX - _this.left;
                var y = event.originalEvent.clientY - _this.top;
                xlog('call leave');
                W.util.mobilePageDragComponentHandler('leave', x, y);
            },
            drop: function(event, ui) {
                xlog('drop now...');
                var componentType = ui.draggable.attr('data-component-type');
                xlog('create component with type ' + componentType);
                var component = W.component.Component.create(componentType);
                W.Broadcaster.trigger('component:create', component);
                // _this.$newElementIndicator.css({visibility: 'hidden'});

                // var component = W.getComponent(ui.draggable);
                // if (!component) {
                //     return;
                // }

                // //绑定component的model的change事件
                // component.model.on('change', function(model) {
                //     xlog('handle change event, re render component');
                //     this.activeComponentNode.find('.control-group').remove();
                //     this.activeComponentNode.prepend($.tmpl(component.template, model.toJSON()));
                // }, _this);

                // var node = $('<div class="componentContainer xui-oneComponent">');
                // node.data('component', component);
                // node.append($.tmpl(component.template, component.model.toJSON()));
                // node.append('<div class="componentOverlay"><a href="#" class="formPage_removeComponentBtn btn btn-danger btn-mini"><i class="icon-remove icon-white"></i></a></div>')
                // if (component.extraClass) {
                //     node.addClass(component.extraClass);
                // }
                // _this.$form.append(node);

                // //将新建node设置为active的node
                // var event = {};
                // event.currentTarget = node.find('.componentOverlay');
                // _this.onClickComponent(event);

                // //更新所有component的index
                // var index = 1;
                // _this.$('.componentContainer').each(function() {
                //     //使用silent，以避免激发change事件
                //     $(this).data('component').model.set({index: index++}, {silent: true});
                // });

                // _this.$form.parent().scrollTop(100000);
            }
        }

        this.$cover.droppable(dropOptions);
    },
    */

    getRightBorderOffset: function() {
        var $phone = this.$('#phone');
        var offset = $phone.offset();
        var width = $phone.outerWidth();
        return offset.left + width;
    },

    onClickTitle: function(event) {
        W.Broadcaster.trigger('designpage:select_page_component');
    }
});