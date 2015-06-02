/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 以下为切换当前用户view
 * TOGGLE_EVENT切换用户时触发的事件，参数blogger_id
 */
W.OrderDetailListView = Backbone.View.extend({
	events:  {
        'click .tx_showPassword': 'showPassword',
        'click .tx_sortByStatus': 'sortByStatus',
        'click .tx_sortBySource': 'sortBySource'
	},
    
    getTemplate: function(options) {
        var name = options.template + '-tmpl';
		$(options.template).template(name);
		return name;
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$el.html('<div class="tx_content"></div><div class="tx_page simplePageBox"></div>');
		this.bind('reload', this.reload, this);
        this.template = this.getTemplate(options);
		this.$content = this.$('.tx_content');
		
		var _this = this;
		this.collection = new options.collectionClass(options.collection);
		
		//创建分页部分view
		this.$pagination = this.$('.tx_pageaaaa');
		this.$pagination = this.$('.tx_page');
		this.paginationView = new W.PaginationView({
            el: this.$pagination,
            isHasDetailedPage: true,
        });
		this.paginationView.isDisplayInfo = false;
		this.paginationView.bind('goto', this.gotoPage, this);
		
		this.fetch();
	},
	
	gotoPage: function(page) {
		this.collection.args = this.collection.args || {};
		this.collection.args.page = page;
		this.fetch();
	},
	
	render: function() {
        this.$('.tx_content').html($.tmpl(this.template, {items: this.collection.cacheData}));
        if(this.collection.args.order_id) {
            this.$('tr').css('display','');
            $('.tx_showPassword').html(' - ');
        }
        this.collection.args = this.collection.args || {};
        var status = this.collection.args.status || -1;
        this.$('.tx_sortByStatus[value="'+status+'"]').addClass('active');
        var source = this.collection.args.source || -1;
        this.$('.tx_sortBySource[value="'+source+'"]').addClass('active');
	},
	
    sortByStatus: function(event) {
        var $el = $(event.currentTarget);
        var status = $el.attr('value');
        this.reload({
            status: status
        });
    },
    
    sortBySource: function(event) {
        var $el = $(event.currentTarget);
        var source = $el.attr('value');
        this.reload({
            source: source
        });
    },
	
    setLoading: function() {
        var isHasLoading = this.$('.tx_loading').length;
        if(isHasLoading) {
            this.$('.tx_loading').show();
        }
        else {
            this.$content.append('<div class="chartTableListLoading tx_loading"></div>');
            this.$content.css({
                'position':'relative'
            });
            if(!this.isFirst) {
                this.$content.css({
                    'min-height':this.$('.tx_loading').height()
                });
                this.isFirst = true;
            }
        }
    },
	
	fetch: function() {
		this.setLoading();
		var _this = this;
		this.collection.fetch({
			success: function(model, data) {
				_this.trigger('success', data);
				_this.$('.tx_loading').hide();
				_this.paginationView.pageinfo = data.page_info;
				if(data.data && data.data.page_info) {
					_this.paginationView.pageinfo = data.data.page_info;
				}
				newData = model.toJSON();
				if(!newData || !newData.length) {
					_this.paginationView.hide();
				}
				else {
					_this.paginationView.show();
				}                
				_this.render();
                _this.$content.css({
                    'min-height':'0'
                });
			},
			error: function() {
				_this.$('.tx_loading').hide();
                _this.$content.css({
                    'min-height':'0'
                });
			}
		});
	},
	
	reload: function(args) {
		args.page = 1;
		this.collection.args = _.extend({}, this.collection.args, args);        
		this.fetch();
        this.trigger('reloading', this.collection.args);
	},
    
    showPassword: function(event) {
        var $el = $(event.currentTarget);
        var id = $el.parent('tr').attr('data-id');
        var el_password = id+'_password';
        var $password = $('tr[data-id="'+el_password+'"]');
        if( $password.css('display') === 'none' ){
            $el.html(' - ');
            $password.show();
        }else{
            $el.html(' + ');
            $password.hide();
        }
    }
    
});