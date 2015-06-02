/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * 
 * 
 * author: tianyanrong
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.fetch", $.mobile.widget, {
		options : {
            api: '',
            app: '',
            args: {
                count: 10
            }
		},
		
		settings : {
			
		},
        
        _setCount: function() {
            var itemHeight = this.$el.attr('item-height');
            if(!itemHeight) {
                return;
            }
            if(this.count) {
                return this.count;
            }
            var offset = this.$el.offset();
            var windowHeight = $(window).height();
            var count = (windowHeight - offset.top)/itemHeight;
            this.count = parseInt(count, 10);
            return this.count;
        },
				
		_create: function() {
            this._bind();
			this.$el = this.element;
            this.options.api = this.$el.attr('fetch-api');
            this.options.app = this.$el.attr('fetch-app');
            var _this = this;
            this.cacheData = {};
            this.pageInfo = {};
            this.currentPage = 1;
            
            //绑定change事件
            var _this = this;
            this.$el.bind('event-fetch', function() {
                _this._triggerFetch();
            });
            
            setTimeout(function() {
                _this.options.args.count = _this._setCount();
                _this._fetch();
            },20)
		},
        
        _triggerFetch: function(event) {
            var type = this.$el.attr('type');
            var isCanFetch = false;
            switch(type) {
            case 'prev':
                this.options.args.direction = 1;
                this.options.args.index_id = this.pageInfo.first_id;
                isCanFetch = this.pageInfo && this.pageInfo.is_first_page ? false : true;
                this.currentPage = isCanFetch ? this.currentPage-1 : this.currentPage;
                break;
            case 'next':
                this.options.args.direction = 2;
                this.options.args.index_id = this.pageInfo.end_id;
                isCanFetch = this.pageInfo && this.pageInfo.is_end_page ? false : true;
                this.currentPage = isCanFetch ? this.currentPage+1 : this.currentPage;
                break;
            }
            if(isCanFetch) {
                this._fetch();
            }
        },
        
        _success: function(data) {
            this.$el.data('success-data', data);
            this.$el.trigger('event-success');
        },
        
        _fetch: function() {
            var _this = this;
            this.$el.data('fetch-args', this.options.args);
            this.$el.trigger('event-loading');
            if(this.cacheData[this.currentPage]) {
                this.pageInfo = this.cacheData[this.currentPage].page_info
                this._success(this.cacheData[this.currentPage]); 
                return;
            }
            W.getApi().call({
                api: this.options.api,
                app: this.options.app,
                args: this.options.args,
                success: function(data) {
                    _this.pageInfo = data.page_info
                    _this.cacheData[_this.currentPage] = data;
                    _this._success(data);                    
                },
                error: function(resp) {
                    
                }
            });
        },

		_bind : function() {
		},
		
		_unbind : function() {
		},
		
		destroy : function() {
			// Unbind any events that were bound at _create
			this._unbind();

			this.options = null;
		}
	});

	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=fetch)", e.target).fetch();
	});
})(jQuery);
