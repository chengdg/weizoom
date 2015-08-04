/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * OrderDeliveryListAdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table,
 * 包含发货功能
 */
ensureNS('W.view.common');
W.view.common.OrderDeliveryListAdvancedTable = Backbone.View.extend({
	events:  {
        'click .tx_searchable': 'onClickSearchableHeader',
        'click .tx_searchable_confirm_btn': 'onClickSearchableConfirmButton',
        'click .tx_sortable': 'onClickSortableHeader',
        'click .tx_filterable': 'onClickFilterableHeader',
        'click .tx_filterable li a': 'onClickFilterableItem',
        'click .tx_selectAll': 'onClickSelectAllItemsCheckbox',
        'click .tx_expandTrigger': 'onClickExpandTrigger',
        'click .xa-inner-sortTrigger': 'onClickSortTrigger',

		'click .tx_showPassword': 'showPassword',
		'click .tx_sendOutBtu': 'onSendOutButton',
		'keyup .tx_waybill': 'isCanSendOutButton',
		'change .tx_express_name': 'isCanSendOutButton',
		// 点击公司选择按钮
		'click .tx_selectGroup': 'selectGroup'
	},

    /**
     * getTemplate: 将options.template指定的模板源码编译为名为${options.template}-tmpl的模板
     */    
    getTemplate: function(options) {
        var name = options.template + '-tmpl';
		$(options.template).template(name);
		return name;
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$el.html('<div class="tx_content"></div><div class="tx_advancedTable_paginator"></div>');
		this.template = this.getTemplate(options);
		this.$content = this.$('.tx_content');

        /*
        if (options.hasOwnProperty('sorted_attr')) {
            this.sortAttr = options.sorted_attr;
        }
        */
        this.searchQuery = null;

        this.filterAttr = null;
        this.filterValue = null;

        this.sortAttr = options.initSort || null;

        this.paginationView = null;
        this.itemCountPerPage = parseInt(options.itemCountPerPage) || 15;
        this.curPage = 1;
        if (options.enablePaginator) {
            this.createPaginationView();
        }

        this.enableSort = options.enableSort;

		//创建分页部分view
        /*
		this.$pagination = this.$('.tx_page');
		this.paginationView = new W.PaginationView({
            el: this.$pagination,
            isHasDetailedPage: true,
        });
		this.paginationView.isDisplayInfo = false;
		this.paginationView.bind('goto', this.gotoPage, this);
		
		this.fetch();
        */
	},

    /*在拖动时，拖动行的cell（单元格）宽度会发生改变。在这里做了处理就没问题了*/
        /*
    storHelper: function(e, ui) {
        ui.children().each(function() {
            $(this).width($(this).width());
        });
        return ui;
    },

    submitForSort: function() {
        var sortedItemIds = [];
        this.$("tbody tr").each(function() {
            var id = $(this).attr("data-id");
            sortedItemIds.push(id);
        });

        W.getApi().call({
            app: this.options.app,
            api: this.options.sortApi,
            args: {
                ids: sortedItemIds.join(','),
                cur_page: this.curPage,
                count_per_page: this.itemCountPerPage
            },
            success: function(data) {
                W.getSuccessHintView().show('调整顺序成功');
            },
            error: function(resp) {
                W.getErrorHintView().show('调整顺序失败，请稍后重试！');
            },
            scope: this
        });
    },
    */
	
	render: function() {
        this.load(true);
	},

    reload: function() {
        this.searchQuery = null;
        this.filterAttr = null;
        this.filterValue = null;
        this.sortAttr = this.options.initSort || null;
        this.load(true);
    },

    load: function(from_goto) {
        //构造传递给后台api的参数
        var args = {};
        if (this.options.args) {
            args = $.parseJSON(this.options.args);
        }
        if (this.sortAttr) {
            args['sort_attr'] = this.sortAttr;
        }
        if (this.searchQuery) {
            args['query'] = this.searchQuery;
        }
        if (this.filterAttr) {
            args['filter_attr'] = this.filterAttr;
            args['filter_value'] = this.filterValue;
        }

        if (this.itemCountPerPage) {
            args['count_per_page'] = this.itemCountPerPage;
            args['page'] = this.curPage;
        }

        if (this.enableSort) {
            if (from_goto) {
                //来自翻页的load，保持排序行为
            } else {
                this.enableSort = false;
            }
        }

        W.getLoadingView().show();
        W.getApi().call({
            app: this.options.app,
            api: this.options.api,
            args: args,
            scope: this,
            success: function(data) {
                W.getLoadingView().hide();
                var $node = $.tmpl(this.template, {items: data.items, data: data, categories: data.categories});

                //table不存在
                this.$content.html($node);

                //初始化searchable header
                this.$content.find('.tx_searchable').css('cursor', 'pointer').append(' <i class="icon-search"></i>').popover({
                    placement: 'bottom',
                    title: '输入搜索文本',
                    html: true,
                    trigger: 'manual',
                    content: '<input type="text" class="input-medium inline" />&nbsp;<button class="btn btn-success tx_searchable_confirm_btn">确定</button>'
                });

                //初始化sortable header
                this.$content.find('.tx_sortable').css('cursor', 'pointer').append(' <i class="hide icon-arrow-up"></i>');
                //显示当前已排序column的排序指示图标
                var sortedDirection = 'up';
                var sortedAttr = data.sortAttr;
                if (sortedAttr[0] === '-') {
                    sortedDirection = 'down';
                    sortedAttr = sortedAttr.substring(1);
                }

                //初始化filterable header
                var $filterables = this.$content.find('.tx_filterable');
                $filterables.css('cursor', 'pointer').find('.dropdown-toggle').append(' <i class="icon-chevron-down"></i>');
                $filterables.find('.dropdown-menu').css('margin-top', '8px');
                $filterables.find('.dropdown-toggle').dropdown();

                var selector = '[data-sort-attr="' + sortedAttr + '"]';
                var $th = this.$content.find(selector);
                $th.attr('data-sort-direction', sortedDirection);
                var newIconClass = 'icon-arrow-' + sortedDirection;
                $th.find('i').removeClass('icon-arrow-up').addClass(newIconClass).removeClass('hide');

                //处理翻页
                if (this.paginationView) {
                    this.paginationView.setPageInfo(data.pageinfo);
                    this.paginationView.show();
                }

                //处理拖动排序
                if (this.enableSort) {
                    this.$el.find('thead tr').append('<th width="100">调整顺序</th>');
                    this.$el.find('tbody tr').append('<td>'
                        + '<a class="btn btn-mini xa-inner-sortTrigger" data-direction="up" href="javascript:void(0);" data-toggle="tooltip" title="向上" data-placement="bottom"><i class="icon-arrow-up"></i></a>'
                        + '<a class="btn btn-mini xa-inner-sortTrigger ml5" data-direction="down" href="javascript:void(0);" data-toggle="tooltip" title="向下" data-placement="bottom"><i class="icon-arrow-down"></i></a>'
                        + '<a class="btn btn-mini xa-inner-sortTrigger ml5" data-direction="top" href="javascript:void(0);" data-toggle="tooltip" title="置顶" data-placement="bottom"><i class="icon-hand-up"></i></a>'
                    );
                    /*
                    $tbody = this.$el.find('tbody');
                    $sortHandler = $tbody.find('td.wui-advanced-table-sort-handler');
                    $sortHandler.wrapInner('<div class="fl"></div>');
                    $sortHandler.prepend('<div class="fl wui-inner-real-sort-handler" style="cursor: move;"><i class=" icon-resize-vertical"></i></div>');
                    $tbody.sortable({
                        axis: 'y',
                        helper: this.storHelper,
                        placeholder: "ui-state-highlight",
                        cursor: 'move',
                        handle: '.wui-inner-real-sort-handler',
                        stop: _.bind(function(options) {
                            this.submitForSort();
                        }, this)
                    });
                    */
                }
            },
            error: function(resp) {
                W.getLoadingView().show();
                // alert('加载分类失败!');
            }
        });
    },

    /**
     * gotoPage: 翻页
     */
    gotoPage: function(page) {
        this.curPage = page;
        this.load(true);
    },

    /**
     * createPaginationView: 创建翻页view
     */
    createPaginationView: function() {
        this.paginationView = new W.view.common.PaginationView({
            el: this.$('.tx_advancedTable_paginator'),
            isHasDetailedPage: true,
            isHasJumpPage: true
        });
        this.paginationView.bind('goto', this.gotoPage, this);
    },

    /**
     * onClickSearchableHeader: 点击searchable header时的响应函数
     */
    onClickSearchableHeader: function(event) {
        $(event.currentTarget).popover('toggle');
    },

    /**
     * onClickSearchableConfirmButton: 点击searchable编辑区中“确定”按钮时的响应函数
     */
    onClickSearchableConfirmButton: function(event) {
        var $button = $(event.currentTarget);
        var $input = $(event.currentTarget).parent().find('input[type="text"]');
        $button.parents('th').find('.tx_searchable').popover('toggle');

        var query = $.trim($input.val());
        if (query) {
            this.searchQuery = query;
        } else {
            this.searchQuery = null;
        }
        this.load();
    },

    /**
     * onClickSortableHeader: 点击sortable header时的响应函数
     */
    onClickSortableHeader: function(event) {
        var $th = $(event.currentTarget);
        var sortAttr = $th.attr('data-sort-attr');

        //确定排序方向
        var sortDirection = $th.attr('data-sort-direction');
        if (!sortDirection) {
            sortDirection = 'up';
        } else if ('up' === sortDirection) {
            sortDirection = 'down';
        } else if ('down' === sortDirection) {
            sortDirection = 'up';
        }

        this.sortAttr = (sortDirection === 'up' ? '' : '-') + sortAttr;
        this.load(); 
    },

    /**
     * onClickFilterableHeader: 点击filterable header时的响应函数
     */
    onClickFilterableHeader: function(event) {
        var $th = $(event.currentTarget);
        $th.find('.dropdown-toggle').dropdown('toggle');
    },

    /**
     * onClickFilterableItem: 点击filterable item时的响应函数
     */
    onClickFilterableItem: function(event) {
        var $item = $(event.currentTarget);
        this.filterAttr = $item.attr('data-attr');
        this.filterValue = $item.attr('data-value');
        this.load();
    },

    /**
     * onClickSelectAllItemsCheckbox: 点击.tx_selectAll复选框时的响应函数
     */
    onClickSelectAllItemsCheckbox: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');

        var $allCheckboxes = $checkbox.parents('table').find('tbody input[type="checkbox"]')
        if (isChecked) {
            $allCheckboxes.attr('checked', 'checked');
        } else {
            $allCheckboxes.removeAttr('checked');
        }
    },

    /**
     * onClickExpandTrigger: 点击.tx_expandTrigger时的响应函数
     */
    onClickExpandTrigger: function(event) {
        var $el = $(event.currentTarget);
        var source = $el.attr('data-expand-source');

        var $targetEl = $('[data-expand-target="'+source+'"]');
        if ($targetEl.is(':visible')) {
            $targetEl.hide();
            $el.text('+');
        } else {
            $targetEl.show();
            $el.text('-');
        }
    },

    /**
     * onClickSortTrigger: 点击.xa-inner-sortTrigger时的响应函数
     */
    onClickSortTrigger: function(event) {
        var $el = $(event.currentTarget);
        var direction = $el.attr('data-direction');

        var $srcTr = $el.parents('tr').eq(0);
        var $dstTr = null;
        var srcId = $srcTr.attr('data-id');
        var dstId = 0;
        if (direction === 'up') {
            $dstTr = $srcTr.prev();
            if ($dstTr.length === 0) {
                return;
            }
            dstId = $dstTr.attr('data-id');
        } else if (direction === 'down') {
            $dstTr = $srcTr.next();
            if ($dstTr.length === 0) {
                return;
            }
            dstId = $dstTr.attr('data-id');
        } else if (direction === 'top') {
            dstId = 0;
        }

        W.getApi().call({
            app: this.options.app,
            api: this.options.sortApi,
            args: {
                src_id: srcId,
                dst_id: dstId
            },
            success: function(data) {
                //W.getSuccessHintView().show('调整顺序成功');
                if (direction === 'up') {
                    $srcTr.detach().insertBefore($dstTr);
                } else if (direction === 'down') {
                    $srcTr.detach().insertAfter($dstTr);
                } else {
                    this.reload();
                }
            },
            error: function(resp) {
                W.getErrorHintView().show('调整顺序失败，请稍后重试！');
            },
            scope: this
        });
    },

	/***
	 *  新加入
	 * @param event
	 */
	showPassword: function(event) {
		var $el = $(event.currentTarget);
		var id = $el.parents('tr').attr('data-id');
		var el_password = id+'_password';
		var $password = $('tr[data-id="'+el_password+'"]');
		if( $password.css('display') === 'none' ){
			$('tr.hide-tr').hide();
			$password.show();
		}else{
			$password.hide();
		}
	},

	onSendOutButton: function(event){
		console.log('sendOutButton');
		var $el = $(event.currentTarget);
		var $password = this.getSupernatantDivEl($el);
		if($el.hasClass('btn-success')){
			var order_id = $password.find('.tx_orderId').val();
			var tx_waybill = $password.find('.tx_waybill').val().trim();
			var tx_express_name = $password.find('.tx_selectGroup').attr('data-name');
            var tx_leader_name = $password.find('.tx_leader_name').val().trim();
			console.log(tx_leader_name)
            this.callApi(order_id, tx_waybill, tx_express_name, tx_leader_name);
		}


	},
	// 发货按钮是否可用
	isCanSendOutButton: function(event){
		var $el = $(event.currentTarget);
		var $password = this.getSupernatantDivEl($el);

		var tx_waybill = $password.find('.tx_waybill').val().trim();
		var tx_express_name = $password.find('.tx_selectGroup').attr('data-name');

		if(tx_express_name!='0' && tx_waybill.length > 1){
			$password.find('.tx_sendOutBtu').addClass('btn-success');
		}else{
			$password.find('.tx_sendOutBtu').removeClass('btn-success');
		}
	},

	getSupernatantDivEl: function($el){
		var id = $el.attr('data-id');
		var el_password = id+'_password';
		var $password = $('tr[data-id="'+el_password+'"]');
		return $password;
	},

	callApi: function(order_id, waybill, express_name, leader_name){
		W.getLoadingView().show();
		W.getApi().call({
			app: 'ft/waybill',
			api: 'waybill/add',
			method: 'post',
			args: {
				order_id: order_id,
				waybill:waybill,
				express_name:express_name,
                leader_name:leader_name
			},
			success: function(data) {
				W.getLoadingView().hide();
				W.getErrorHintView().show('确发货成功！');
				this.load();
			},
			error: function(resp) {
				W.getLoadingView().hide();
				W.getErrorHintView().show('发货失败，请稍后重试！');
			},
			scope: this
		});
	},

	selectGroup: function(event) {
		xlog('selectGroup');
		var $el = $(event.currentTarget);
		var $password = this.getSupernatantDivEl($el);
		W.ISELECTED_GROUPS_LOADING = false;
		var moveDropBox = W.getMoveTimeLineDropBox();
		moveDropBox.show({
			locationElement:$(event.currentTarget),
			isShowAddGroupButton : true
		});

		moveDropBox.bind(moveDropBox.CLICK_ACTIONS_EVENT, function(resp) {
			$password.find('.tx_selectGroup').html(resp.name+'&nbsp;<span class="caret mt0"></span>');
			$password.find('.tx_selectGroup').attr("data-name", resp.name);
			this.isCanSendOutButton(event);
		}, this);

	}
});

W.registerUIRole('div[data-ui-role="order-delivery-advanced-table"]', function() {
    var $div = $(this);
    var app = $div.attr('data-app');
    var api = $div.attr('data-api');
    var args = $div.attr('data-args');
    var template = $div.attr('data-template-id');
    var initSort = $div.attr('data-init-sort');
    var enablePaginator = !!($div.attr('data-enable-paginator') === 'true');
    var enableSort = !!($div.attr('data-enable-sort') === 'true');
    var sortApi = $div.attr('data-sort-api');
    var itemCountPerPage = $div.attr('data-item-count-per-page');
    if (itemCountPerPage) {
        itemCountPerPage = parseInt(itemCountPerPage);
    } else {
        itemCountPerPage = 15;
    }

    var orderAdvancedTable = new W.view.common.OrderDeliveryListAdvancedTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
        initSort: initSort,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        sortApi: sortApi
    });
	orderAdvancedTable.render();

    $div.data('view', orderAdvancedTable);
});