/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <input name="area" data-ui-role="area" type="text" value="1_1_2">
 * value属性的值:省_城市_区
 * author: tianyanrong
 */
(function($, undefined) {
    $.widget("mobile.templateView", $.mobile.widget, {
        _getLoading: function() {
            var tagName = this.$content[0].tagName;
            var loadingHtml = '';
            if('UL' === tagName) {
                loadingHtml = '<li class="xui-fetch-loading tx_loading" style="display:hidden;"><span class="xui-fetch-loading-span">loading...</span></li>';
            }
            else if('TBODY' === tagName) {
                var count = this.$content.parents('table').find('thead th, thead td').length;
                loadingHtml = '<tr class="xui-fetch-loading tx_loading" style="display:hidden;"><td colspan="'+count+'"><span class="xui-fetch-loading-span">loading...</span></td></tr>';
            }
            else {
                loadingHtml = '<div class="xui-fetch-loading tx_loading" style="display:hidden;"><span class="xui-fetch-loading-span">loading...</span></div>';
            }
            return loadingHtml;
        },
        
        _create: function() {
            this.$el = this.element;
            this.tempate = this._getTemplate();
            this.$content = this.$el.find('script').parent();
            this.$loading = $(this._getLoading());
            
            this.$el.addClass('xui-template')
            
            var _this = this;
            this.$el.delegate('.tx_prev', 'click', function(event) {
                _this.$el.attr('type', 'prev');
                _this.$el.trigger('event-fetch');
            });
            this.$el.delegate('.tx_next', 'click', function(event) {
                _this.$el.attr('type', 'next');
                _this.$el.trigger('event-fetch');
            });
            
            this.$el.bind('event-success', function() {
                _this._render();
            });
            this.$el.bind('event-loading', function() {
                _this._setLoading();
            });
            
            //this._bindSwipe();
        },
        
        _bindSwipe: function() {
            $(document).bind('scrollstart', function(event) {
                $('.ui-btn-text').html(window.scrollY+',')
            });
            $(document).bind('scrollstop', function(event) {
                //alert($(event.target).offset().top)
                $('.ui-btn-text').append(window.scrollY+'=='+document.body.scrollHeight)
            });
        },
        
        _getTemplate: function() {
            var templateId = this.$el.find('script').attr('id');
            var tmplId = templateId + '-tmpl';
            $('#' + templateId).template(tmplId);
            return tmplId;
        },
        
        _setTools: function(pageInfo) {
            if(!this.$el.attr('data-icon')) {
                return;
            }
            this.$prev = this.$el.find('.tx_prev');
            this.$next = this.$el.find('.tx_next');
            if(!this.$prev.length) {
                var button = '<a class="btn-prev tx_prev" type="prev" data-role="button"></a>\
                            <a class="btn-next tx_next" type="next" data-role="button"></a>';
                this.$el.prepend(button);
                this.$el.find('.tx_prev').button();
                this.$el.find('.tx_next').button();
                this.$prev = this.$el.find('.tx_prev');
                this.$next = this.$el.find('.tx_next');
            }
            
            if(pageInfo.is_first_page) {
                this.$prev.addClass('ui-btn-desibled');
            }
            else {
                this.$prev.removeClass('ui-btn-desibled');
            }
            if(pageInfo.is_end_page) {
                this.$next.addClass('ui-btn-desibled');
            }
            else {
                this.$next.removeClass('ui-btn-desibled');
            }
            if(pageInfo.is_first_page && pageInfo.is_end_page) {
                this.$next.css({'display': 'none'});
                this.$prev.css({'display': 'none'});
            }
        },        
        
        _setLoading: function() {
            var args = this.$el.data('fetch-args');
            var direction = args && args.direction ? args.direction : 0;
            var offsetTop = parseInt(this.$el.offset().top, 10);
            switch(direction) {
            case 0:
                this.$loading.appendTo(this.$content);
                this.$loading.show();
                break;
            case 1:
                this.$loading.prependTo(this.$content);
                this.$loading.show();
                break;
            case 2:
                this.$loading.appendTo(this.$content);
                this.$loading.show();
                break;
            }
        },
        
        _render: function() {
            var data = this.$el.data('success-data');
            this._setTools(data.page_info);
            this.$content.html($.tmpl(this.tempate, data));
        }
    });
	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
        var $el = $(":jqmData(ui-role=fetch)", e.target);
        var templateView = $el.attr('template-view');
        if($el[templateView] && 'function' === typeof $el[templateView]) {
            $el[templateView]();
        }
	});
})(jQuery);
