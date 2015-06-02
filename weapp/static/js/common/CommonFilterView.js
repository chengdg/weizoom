/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 以下为切换当前用户view
 * TOGGLE_EVENT切换用户时触发的事件，参数blogger_id
 */
W.CommonFilterListView = Backbone.View.extend({
	events:  {
        'click .tx_showPassword': 'showPassword',
        'click .tx_sortByStatus': 'sortByStatus',
        'click .tx_sortBySource': 'sortBySource',
        'click .tx_sortByCreatedTime':'sortByCreatedTime',
        'click .tx_inputFilterShow': 'inputFilterShow',
        'click .tx_inputFilterButton': 'inputFilterButton',
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
		this.created_click = 0;
        xlog('-=-=-=-=-=-=-=----------------------------------')
        xlog(options.filter_relation)
        if (options.filter_relation) {
            this.filter_relation = options.filter_relation;
        } else {
            this.filter_relation = 'false';
        }
		var _this = this;
		//this.collection = new options.collectionClass(options);
		this.collection = new W.CommonFilterCollection(options);
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
        this.$('.tx_content').html($.tmpl(this.template, {items: this.collection.cacheData, categories: this.collection.cacheCategories}));
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

	inputFilterShow: function(event){
        var is_input_hide= $(".tx_input_div").is(":hidden");
        if (is_input_hide) {
            $('.tx_input_div').show();
        } else{
            $('.tx_input_div').hide();
        }
    },
    inputFilterButton: function(event){
        var $el = $(event.currentTarget);
        var data_value = $('.tx_inputFilterValue').attr('value');
        var data_attr = $el.attr('data-attr');
        var args = {};
        args[data_attr] = data_value;
        this.reload(args);
    },

    sortByStatus: function(event) {
        var $el = $(event.currentTarget);
        var data_value = $el.attr('value');
        var data_attr = $el.attr('data-attr');
        var args = {};
        args[data_attr] = data_value;
        this.reload(args);
    },
    
    sortBySource: function(event) {
        var $el = $(event.currentTarget);
        var source = $el.attr('value');
        this.reload({
            source: source
        });
    },

	sortByCreatedTime: function(event){
        var $el = $(event.currentTarget);
        var data_value = $el.attr('value');
        var data_attr = $el.attr('data-attr');
        if (this.created_click === 0) {
            data_value = '-'+data_attr;
            this.created_click = 1;
        } else{
            data_value = data_attr;
            this.created_click = 0
        }
        var args = {};
        args[data_attr] = data_value;
        this.reload(args);
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
        if (this.filter_relation == 'true') {
            this.collection.args = _.extend({}, this.collection.args, args);
        }else {
           // if (!args.hasOwnProperty('created_at') && this.collection.args.hasOwnProperty('created_at')){
    		 //   args['created_at'] = this.collection.args['created_at'];
            //} 
            this.collection.args = args;
        }
           
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