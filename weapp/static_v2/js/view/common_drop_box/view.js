/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/*
* 下拉弹出框
*/
ensureNS('W.view.common');
W.view.common.DropBox = Backbone.View.extend({
    tagName: 'div',
    
    className: 'dropdown-menu',
    
    isArrow: true,
    
    isTitle: true,
    
    position: 'top',
    
    initialize: function(options) {
        var _this = this;
        options = options || {};
        this.isTitle = (options.isTitle == false || options.isTitle == undefined)? false : true;
        this.isArrow = (options.isArrow || options.isArrow == undefined)? true : false;
        this.position = options.position || 'top';
        this.$el = $(this.el);
        this.$html = $('html');
        
        this.isInFileInput = false;
        this.$el.bind('click', function(event) {
            if('file' === event.target.type || 'checkbox' === event.target.type || 'radio' === event.target.type || 'checkbox' === event.target.className) {
                _this.isInFileInput = true;
                return;
            }
            var href = $(event.target).attr('href');
            if (href) {
                return true;
            } else {
                return false;
            }
        });
        this.$el.delegate('.xa-close', 'click', function(event) {
            _this.close(event);
        });
        
        this.$content = $('<div class="drop-box-content xa-drop-box-content"></div>');
        this.$arrow = $('<div class="drop-box-arrow"></div>');
        this.$title = $('<div class="drop-box-title"></div>');
        // this.$title = $('<div class="drop-box-title"><h2 class="tx_title"></h2><button class="close tx_close" type="button">×</button></div>');
        this.$loading = this.$content;
        this.buildHtml();
        if(options.width) {
            this.$el.css({'width': options.width+'px'});
        }if(options.height) {
            this.$el.css({'height': options.height+'px'});
        }
        $('body').append(this.$el);
        
        this.initializePrivate(options);
    },
    
    initializePrivate: function(options) {
    },
    
    bindLoading: function(isShow) {
        if(isShow) {
            this.$loading.addClass('drop-box-loading');
        }
        else {
            this.$loading.removeClass('drop-box-loading');
        }
    },
    
    buildHtml: function() {
        if(this.isArrow) {
            this.$el.append(this.$arrow);
            this.$arrow.addClass('drop-box-arrow-'+this.position);
        }
        if(this.isTitle) {
            this.$el.append(this.$title);
        }
        this.$el.append(this.$content);
    },
    setSize:function(width,height){
        if(width) {
            this.$el.css({'width': width+'px'});
        }if(height) {
            this.$el.css({'height': height+'px'});
        }
    },
    setPosition: function(position) {
        var $action = this.$action;
        var elOffset = $action.offset();
        var elWidth = parseInt($action.css('width'));
        var elHeight = $action.height();
        var currWidth = this.$el.width() || 0;
        var currHeight = parseInt(this.$el.css('height')) || 0;
        var isBtn = $action.hasClass('btn') || $action.hasClass('dropdown-toggle');
        // var widthCount = $action.hasClass('btn') ? 28 : 16;
        //elWidth = isBtn ? elWidth + widthCount : elWidth;
        elHeight =isBtn ? elHeight + 8 : elHeight - 5;
        var position = position || this.position;
        //console.log("elOffset.left",elOffset.left,"currWidth",currWidth,"arrowRight",arrowRight,"arrowWidth",arrowWidth,"position",position)
        if(this.isArrow){
            var arrowTop = parseInt(this.$arrow.css('top'));
            var arrowRight = parseInt(this.$arrow.css('right'));
            var arrowWidth = this.$arrow.width()/2;
            var arrowHeight = this.$arrow.height();
            switch(position) {

            case 'top':
                this.$el.css({
                    left: elOffset.left - currWidth + elWidth/2 + arrowRight + arrowWidth,
                    top: elOffset.top + arrowHeight + elHeight
                });
                break;

            case 'left':
                this.$el.css({
                    left: elOffset.left + elWidth + arrowWidth,
                    top: elOffset.top - arrowHeight/2 - arrowTop + elHeight/2
                });
                break;
            case 'right':
                this.$el.css({
                    left: elOffset.left - currWidth - arrowWidth,
                    top: elOffset.top - arrowTop - arrowHeight/2 + elHeight/2 
                });
                break;
            case 'right-middle':
                this.$el.css({
                    left: (elOffset.left - elWidth/3) - currWidth - arrowWidth + 10,
                    top: elOffset.top + elHeight/2 - arrowTop - arrowHeight/2
                });
                break;
            case 'down-right':
                this.$el.css({
                    left: (elOffset.left + elWidth/3*2) - currWidth,
                    top: elOffset.top + elHeight/3*2 + arrowHeight
                });
                break;
            case 'down-left':
                this.$el.css({
                    left: elOffset.left,
                    top: elOffset.top + elHeight + arrowHeight
                });
                break;
            }
            this.$arrow.addClass('drop-box-arrow-'+position);
        }else{
            switch(position) {

            case 'top':
                this.$el.css({
                    left: elOffset.left - currWidth + elWidth,
                    top: elOffset.top + elHeight + 10
                });
                break;

            case 'left':
                this.$el.css({
                    left: elOffset.left + elWidth,
                    top: elOffset.top
                });
                break;
            case 'right':
                this.$el.css({
                    left: elOffset.left - currWidth,
                    top: elOffset.top
                });
                break;
            case 'right-middle':
                this.$el.css({
                    left: elOffset.left - currWidth,
                    top: elOffset.top
                });
                break;
            case 'down-right':
                this.$el.css({
                    left: (elOffset.left + elWidth/2) - currWidth,
                    top: elOffset.top + elHeight
                });
                break;
            case 'down-middle':
                xlog(elOffset.left);
                xlog(elWidth);
                xlog(currWidth);
                this.$el.css({
                    left: elOffset.left - currWidth/2,
                    top: elOffset.top + elHeight + 5
                });
                break;
            case 'down-left':
                this.$el.css({
                    left: elOffset.left + elWidth/2,
                    top: elOffset.top + elHeight
                });
                break;
            }
        }
        
    },
    
    show: function(options) {
        if(this.isDisabledClose) {
            return;
        }
        this.minClickTime = options.minClickTime ? options.minClickTime : 0;
        // console.log('show bengin')
        this.bind('loading', this.bindLoading, this);
        this.close();
        this.trigger('show');

        if (options.msg) {
            if (_.isObject(options.msg)) {
                this.$('.xa-drop-box-content').empty().append(options.msg);
            } else {
                this.$('.xa-drop-box-content').html(options.msg);
            }
        }
        
        this.$action = options.locationElement || options.$action;        
        this.showPrivate(options);
        this.setSize(options.width, options.height);
        this.setPosition(options.position);
        this.$el.show();
        this.bindHtmlClickEvent();
    },
    
    bindHtmlClickEvent: function() {
        var _this = this;
        this.$html.off('click.dropdown.drop-box-weizhong');
        this.$html.bind('click.dropdown.drop-box-weizhong', function (event) {
            //console.log('click.dropdown',_this.isDisabledClose, _this.isInFileInput, event.target === _this.$action[0])
            if(_this.isInFileInput || _this.isDisabledClose) {
                _this.isInFileInput = false;
                return;
            }
            if(event.target === _this.$action[0]) {
                return;
            }
            if(_this.minClickTime > 0){
                return;
            }
            _this.isInFileInput = false;
            _this.hide();
        })
    },
    
    showPrivate: function(options) {
    
    },
    
    hide: function(event) {
        this.closePrivate(event);
        this.trigger('close');
        this.$el.hide();
        this.unbind();
        this.$html.off('click.dropdown.drop-box-weizhong');
        //console.log('hide end')
    },
    
    close: function(event) {
        // console.log('close',this.$el)
        this.$html.trigger('click.dropdown');
    },
    
    closePrivate: function() {}
});


W.popup = function(options) {
    //获得view
    var view = W.registry['common-popup-info-view'];
    if (!view) {
        xlog('create PopupView');
        view = new W.view.common.DropBox(options);
        view.render();
        W.registry['common-popup-info-view'] = view;
    }

    view.show({
        width:options.width,
        height:options.height,
        $action: options.$el,
        msg: options.msg,
    });
};
