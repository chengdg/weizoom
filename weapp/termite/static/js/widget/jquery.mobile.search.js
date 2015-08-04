/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * author: tianyanrong
 */
(function($, undefined) {
    SearchView = function(options) {
        this.$el = $(options.el);
        this.$search = this.$el.find('.tx_search_input');
        this.$searchButton = this.$el.find('.tx_btnSeach');
        this.defaultValue = this.$search.attr('default-value');
        this.bindEvents();
        this.setSearchButtonStatus();
    };
    SearchView.prototype = {
        bindEvents: function() {
            var _this = this;
            this.$searchButton.bind('click', function() {
                _this.search();
                return false;
            });
        },
        
        setLinkAttr: function($link, value) {
            value = value ? value : '';
            var href = $link.attr('href');
            if(!value) {
                href = href.indexOf('?') ? href.split('?')[0] : href;
                value = '';
            }
            else {
                href = href.indexOf('&query=') ? href.split('&query=')[0] : href;
                value = '&query='+value;
            }
            window.location.href = href+value;
        },
        
        getSearchValue: function() {
            return this.$search.val();
        },
        
        setSearchButtonStatus: function(isShowSearchButton) {
            if(this.timeoutValue) {
                clearTimeout(this.timeoutValue);
                this.timeoutValue = null;
            }
            var _this = this;
            this.timeoutValue = setTimeout(function() {
                clearTimeout(_this.timeoutValue);
                _this.timeoutValue = null;
                var value = _this.getSearchValue();
                if((value && _this.defaultValue !== value) || isShowSearchButton) {            
                    _this.$searchButton.show();
                }else {
                    _this.$searchButton.hide();
                }
                _this.setSearchButtonStatus();
            }, 200)
            
        },
        
        search: function() {
            var value = this.getSearchValue();
            this.$el.data('searchValue', value);
            this.$el.trigger('search');
            this.setLinkAttr(this.$searchButton, value);
        }
    };
    

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=search)", e.target).each(function() {
            var searchView = new SearchView({
                el: this
            });
        });
	});
})(jQuery);
