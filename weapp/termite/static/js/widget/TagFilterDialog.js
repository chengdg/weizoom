/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.TagFilterDialog = function(options) {
	this.$body = $(options.body);
	var _this = this;
    this.language = options.language || 'Chinese';
    this.fetchArgs = options.fetchArgs;
    options.title = this.language === 'English' ? 'Filter' : (options.title || '筛选');
    this.initialize(options);
    if(options.button) {
        this.$body.delegate(options.button, 'click', function() {
            _this.open();
            return;
        });
    }
}

W.TagFilterDialog.prototype = {
    getTemplate: function(options) {
        return '<div class="xui-dialog">\
                    <div class="xui-dialog-title tx_close"><span class="ui-icon ui-icon-arrow-r"></span><h2>'+options.title+'</h2></div>\
                    <div class="xui-dialog-content tx_content"></div>\
                </div>';
    },
    
    bindEvents: function() {
        var _this = this;
        this.$el.delegate('.tx_close', 'click', function() {
            _this.close();
            return;
        });
        this.$el.delegate('.tx_filter', 'click', function(event) {
            var $el = $(event.currentTarget);
            var value = $el.attr('value');
            _this.$el.find('li a').removeClass('active');
            $el.addClass('active');          
            if(_this.filter) {
                setTimeout(function() {
                    _this.filter(value);
                }, 0)
            }
            return false;
        });
        this.$over.unbind();
        this.$over.click(function() {
            _this.close();
            return;
        })
    },
    
    initialize: function(options) {
        this.activeId = options.activeId;
        this.options = options;
        this.$el = $(this.getTemplate(options));
        this.$over = $('<div class="xui-dialog-over" style="display:none;"></div>');
        this.$over.css({
            position:'absolute',
            top:'0',
            left:'0',
            width:'100%',
            height:'100%',
            background:'rbga(255,255,255,0)',    
            'z-index':98
        })
        this.$body.append(this.$over);
        this.$body.append(this.$el);
        this.$el.css({
            right:-this.$el.width()+'px',
            display:'none',
            'z-index':99
        })
        this.$content = this.$el.find('.tx_content');
        this.templateId = options.templateId;
        this.bindEvents();
        this.render();
    },
    
    render: function(data) {
        var _this = this;
        var options = {
            $el: this.$content,
            templateId: this.templateId,
            activeId: this.activeId,
            language: this.language,
            model: this.options.model
        };
        var key;
        for(key in this.fetchArgs) {
            options[key] = this.fetchArgs[key];
        }
        var tagFilterView = new W.TagFilterView(options);
    },
	open: function() {
        this.$over.css({display: 'block'});
        this.$el.css({display: 'block'});
        this.$content.css({
            height:$(window).height() - this.$el.find('.tx_close')[0].clientHeight + 'px',
            right:parseInt(-this.$el.width(), 10)+'px'
        });
        var _this = this;
        setTimeout(function() {
            _this.$el.css({
                right:'0px',
                '-moz-transition': 'right 0.5s',
                '-webkit-transition': 'right 0.51s',
                '-o-transition':  'right 0.5s',
                'transition':  'right 0.5s'
            })
        }, 100);
        
        //this.animate(parseInt(-this.$el.width(), 10), 0, true);
    },
    close: function() {
        var _this = this;
        _this.$el.css({
            right:parseInt(-this.$el.width(), 10)+'px',
            '-moz-transition': 'right 0.5s',
            '-webkit-transition': 'right 0.5s',
            '-o-transition':  'right 0.5s',
            'transition':  'right 0.5s'
        })
        this.$over.css({display: 'none'});
        /* this.animate(0, parseInt(-this.$el.width(), 10), true, function() {
            _this.$el.css({display: 'none'});
            _this.$over.css({display: 'none'});
        }); */
    },
    
    getAnimateStart: function(start, end) {
        var newStart = this.isToUp ? start + this.speedRight : start + this.speedRight;
        newStart = this.isToUp && newStart >= end ? end : newStart;
        newStart = false === this.isToUp && newStart <= end ? end : newStart;
        return newStart;
    },
    
    animate: function(start, end, first, fn) {
        var _this = this;
        if(this.timeoutValue) {
            clearTimeout(this.timeoutValue);
            this.timeoutValue = null;
        }
        if(first) {
            this.isToUp = start < end ? true : false;
            this.speedRight = (end-start)/8;
            this.animateComplete = fn;
        }
        var newStart = this.getAnimateStart(start, end);
        this.timeoutValue = setTimeout(function() {
            clearTimeout(_this.timeoutValue);
            _this.timeoutValue = null;
            _this.$el.css({
                right: newStart + 'px'
            });
            if(newStart === end) {
                if(_this.animateComplete) {
                    _this.animateComplete();
                }
                return;
            }
            _this.animate(newStart, end);
        }, 70);
    }
}