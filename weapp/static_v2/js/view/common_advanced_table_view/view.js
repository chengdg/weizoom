/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * AdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table
 */
ensureNS('W.view.common');

W.view.common.AdvancedTable = Backbone.View.extend({
    events: {
        'click .tx_searchable': 'onClickSearchableHeader',
        'click .tx_searchable_confirm_btn': 'onClickSearchableConfirmButton',
        'click .tx_sortable': 'onClickSortableHeader',
        'click .tx_filterable': 'onClickFilterableHeader',
        'click .tx_filterable li a': 'onClickFilterableItem',
        'click .tx_expandTrigger': 'onClickExpandTrigger',
        'click .xa-inner-sortTrigger': 'onClickSortTrigger',
        'keyup .popover input[type="text"]': 'onPressKeyInPopoverTextInput',
        'click .xa-selectAll': 'onClickSelectAll',
        'click .xa-select': 'onClickSelect'
    },

    /**
     * getTemplate: 将options.template指定的模板源码编译为名为${options.template}-tmpl的模板
     */
    getTemplate: function(options) {
        var name = options.template + '-tmpl';
        xlog("getTemplate() name: " + name);
        $(options.template).template(name);
        return name;
    },

    initialize: function(options) {
        this.$el = $(this.el); // div object of advance table
        this.$el.html('<div class="xa-content xui-advancedTableContent"></div><div class="xa-advancedTablePaginator xui-advancedTablePaginator clearfix"></div>');
        this.template = this.getTemplate(options);
        this.$content = this.$('.xa-content');
        /*
        if (options.hasOwnProperty('sorted_attr')) {
            this.sortAttr = options.sorted_attr;
        }
        */
        this.options = options;
        this.searchQuery = null;
        this.searchAttr = null;

        this.filterAttr = null;
        this.filterValue = null;

        this.initSort = options.initSort;
        this.sortAttr = options.initSort || null;

        this.paginationView = null;
        this.itemCountPerPage = parseInt(options.itemCountPerPage) || 15;
        this.curPage = 1;
        this.userWebappId = options.userWebappId;
        if (options.enablePaginator) {
            this.createPaginationView();
        }

        this.enableSort = options.enableSort;
        this.args = {};
        if (options.args) {
            this.args = $.parseJSON(this.options.args);
        }
        if (this.args['page']) {
            this.curPage = this.args['page'] || 1;
        }
        this.enableSelect = options.enableSelect || false;
        this.disableHeaderSelect = options.disableHeaderSelect || false;
        //this.onlyShowFrontSelect = options.onlyShowFrontSelect || false;
        this.selectableTrSelector = options.selectableTrSelector;
        this.autoLoad = options.autoLoad;

        this.items = null;
        this.frozenArgs = {};
        this.outerSelecter = options.outerSelecter || null;


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
        if (this.autoLoad) {
            this.load(true);
        }
    },

    addFrozenArgs: function(args) {
        _.extend(this.frozenArgs, args);
    },

    setPage: function(page) {
        this.curPage = page;
    },

    reload: function(args, options) {
        this.searchAttr = null;
        this.searchQuery = null;
        this.filterAttr = null;
        this.filterValue = null;
        this.sortAttr = this.options.initSort || null;
        if(args){
            this.extraArgs = args;
        }
        this.load(true, options);
    },

    load: function(from_goto, options) {
        //构造传递给后台api的参数
        var args = {};

        // 解决BUG 002900: 微站-订单管理-创建筛选标签可以创建但是创建好的点击没有效果
        // 去掉注释部分
        _.extend(args, this.args, args);
        if (this.options.args) {
            _.extend(args, $.parseJSON(this.options.args));
        }
        if (this.frozenArgs) {
            _.extend(args, this.frozenArgs);
        }
        if (this.extraArgs) {
            _.extend(args, this.extraArgs);
        }

        if (this.sortAttr) {
            args['sort_attr'] = this.sortAttr;
        }
        if (this.searchQuery) {
            args['query_attr'] = this.searchAttr;
            args['query'] = this.searchQuery;
        }
        if (this.filterAttr) {
            args['filter_attr'] = this.filterAttr;
            args['filter_value'] = this.filterValue;
        }

        if (this.itemCountPerPage) {
            args['count_per_page'] = this.itemCountPerPage;
            args['page'] = this.curPage;
            args['enable_paginate'] = 1
        }

        if (this.enableSort) {
            if (from_goto) {
                //来自翻页的load，保持排序行为
            } else {
                this.enableSort = false;
            }
        }
        var _this = this;
        console.log("options.app", this.options.app);
        console.log("options.api", this.options.api);
        //W.getLoadingView().show();
        W.getApi().call({
            app: this.options.app,
            api: this.options.api,
            args: args,
            method: this.options.apiMethod,
            scope: this,
            success: function(data) {
                _this.rawData = data;
                if (data.items.length == 0) {
                    if (options && options.emptyDataHint) {
                        W.showHint('error', options.emptyDataHint);
                    }
                }
                _this.items = new Backbone.Collection(data.items);
                var $node = $.tmpl(this.template, {
                    items: data.items,
                    data: data,
                    categories: data.categories,
                    'userWebappId': _this.userWebappId
                });
                xwarn('====== advance table =====');
                xwarn($node.html());
                if (this.enableSelect) {
                    if (this.disableHeaderSelect) {
                        $node.find('thead tr').prepend('<th width="30"></th>');
                    } else {
                        $node.find('thead tr').prepend('<th width="30"><input type="checkbox" class="xa-selectAll" /></th>');
                    }
                    if (this.selectableTrSelector) {
                        $node.find('tbody tr').each(function() {
                            var $tr = $(this);
                            
                            if ($tr.hasClass(_this.selectableTrSelector)) {
                                $tr.prepend('<td width="30"><input type="checkbox" class="xa-select" /></td>');
                            } else {
                                $tr.prepend('<td width="30"></td>');
                            }
                        });
                    } else {
                        $node.find('tbody tr').each(function() {
                            var $tr = $(this);
                            $tr.prepend('<td><input type="checkbox" class="xa-select" /></td>');
                        });
                    }
                }

                //table不存在
                xwarn(this.$content);
                this.$content.html($node);
				
                var multilineClass = this.$content.find('#multiline').attr('name');
                if (multilineClass) {
                	this.$content.find(multilineClass).dotdotdot();
                }

                //初始化searchable header
                this.$content.find('.tx_searchable').css('cursor', 'pointer').append(' <i class="icon-search"></i>').popover({
                    placement: 'bottom',
                    title: '输入搜索文本',
                    html: true,
                    trigger: 'manual',
                    content: '<input type="text" class="input-medium inline" />&nbsp;<button class="btn btn-success tx_searchable_confirm_btn mb10">确定</button>'
                });

                //初始化sortable header
                this.$content.find('.tx_sortable').css('cursor', 'pointer').append(' <i class="hide icon-arrow-up"></i>');
                //显示当前已排序column的排序指示图标
                var sortedDirection = 'up';
                var sortedAttr = data.sortAttr;
                if (sortedAttr && sortedAttr[0] === '-') {
                    sortedDirection = 'down';
                    sortedAttr = sortedAttr.substring(1);
                }

                var selector = '[data-sort-attr="' + sortedAttr + '"]';
                var $th = this.$content.find(selector);
                if ($th.length > 0) {
                    $th.attr('data-sort-direction', sortedDirection);
                    var newIconClass = 'icon-arrow-' + sortedDirection;
                    $th.find('i').removeClass('icon-arrow-up').addClass(newIconClass).removeClass('hide');
                }

                //初始化filterable header
                var $filterables = this.$content.find('.tx_filterable');
                $filterables.css('cursor', 'pointer').find('.dropdown-toggle').append(' <i class="icon-chevron-down"></i>');
                //添加搜索框
                var onInputKeyUpHandler = function(event) {
                    var $input = $(event.target);
                    var $li = $(event.currentTarget)
                    var text = $.trim($input.val());
                    if (text === "") {
                        $li.nextAll('li').show();
                    } else {
                        $li.next('li').nextAll('li').hide().each(function() {
                            var $el = $(this);
                            var linkText = $el.text();
                            if (linkText.indexOf(text) !== -1) {
                                //如果链接文本中存在待搜索的字符串，显示该li
                                $el.show();

                            }
                        });
                    }
                }
                $filterables.each(function() {
                    var $filterable = $(this);
                    var $li = $('<li><input /><i class="icon-search"></i></li>');
                    $li.on('click.dropdown.data-api', function(event) {
                        return false;
                    });
                    var $input = $li.find('input');
                    $li.keyup(onInputKeyUpHandler);
                    $filterable.find('.dropdown-menu').css('margin-top', '8px').find('li:first').before($li);
                });

                $filterables.find('.dropdown-toggle').dropdown();

                //处理排序
                //处理翻页
                if (this.paginationView) {
                    this.paginationView.setPageInfo(data.pageinfo);
                    if (this.paginationView && data.pageinfo.object_count != 0) {
                        this.paginationView.show();
                    } else {
                        this.paginationView.hide();
                    }
                }

                //处理拖动排序
                if (this.enableSort) {
                    this.$el.find('thead tr').append('<th width="100">排序</th>');
                    this.$el.find('tbody tr').append('<td>' + '<a class="xa-inner-sortTrigger" data-direction="up" href="javascript:void(0);" data-toggle="tooltip" title="向上" data-placement="bottom" style="color:#0C9D08;"><i class="icon-arrow-up glyphicon glyphicon-arrow-up"></i></a>' + '<a class="ml20 xa-inner-sortTrigger" data-direction="down" href="javascript:void(0);" data-toggle="tooltip" title="向下" data-placement="bottom"><i class="icon-arrow-down glyphicon glyphicon-arrow-down"></i></a>' + '<a class="" data-direction="top" href="javascript:void(0);" data-toggle="tooltip" title="置顶" data-placement="bottom"><i class=""></i></a>');
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
                // 扩展advanced_table.load方法
                this.afterload();
            },
            error: function(resp) {
                // W.getLoadingView().show();
                // alert('加载分类失败!');
                return false;
            }
        });
    },
    /**
    * afterload:扩展advanced_table.load方法
    *
    */
    afterload:function(){},

    /**
     * gotoPage: 翻页
     */
    gotoPage: function(page) {
        this.curPage = page;
        this.load(true);
    },

    getRawData: function() {
        return this.rawData;
    },

    /**
     * getDateItem: 根据数据id获取数据
     */
    getDataItem: function(id) {
        var data = this.items.get(id);
        if (!data) {
            id = parseInt(id);
            data = this.items.get(id);
        }
        return data;
    },

    /**
     * createPaginationView: 创建翻页view
     */
    createPaginationView: function() {
        this.paginationView = new W.view.common.PaginationView({
            el: this.$('.xa-advancedTablePaginator'),
            isHasDetailedPage: true,
            isHasJumpPage: true
        });
        this.paginationView.bind('goto', this.gotoPage, this);
    },

    getAllSelectedDataIds: function() {
        var ids = [];
        this.$('tbody .xa-select').each(function() {
            var $checkbox = $(this);
            if ($checkbox.is(":checked")) {
                var $tr = $checkbox.parents('tr');
                ids.push($tr.data('id'));
            }
        });

        return ids;
    },

    selectAll: function(isSelect) {
        this.$('.xa-select').each(function() {
            var $checkbox = $(this);
            $checkbox.prop('checked', isSelect);
        })
    },

    /**
     * onClickSearchableHeader: 点击searchable header时的响应函数
     */
    onClickSearchableHeader: function(event) {
        var $searchable = $(event.currentTarget);
        $searchable.popover('toggle');
        $searchable.parents('th').eq(0).find('.popover input').attr('name', $searchable.attr('name')).focus();
    },

    /**
     * onClickSearchableConfirmButton: 点击searchable编辑区中“确定”按钮时的响应函数
     */
    onClickSearchableConfirmButton: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var $button = $(event.currentTarget);
        var $input = $(event.currentTarget).parent().find('input[type="text"]');
        var $th = $button.parents('th');
        var $searchable = $th.find('.tx_searchable');
        $searchable.popover('toggle');
        this.searchAttr = $searchable.attr('data-attr');
        if (!this.searchAttr) {
            this.searchAttr = '';
        }

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
     * onClickExpandTrigger: 点击.tx_expandTrigger时的响应函数
     */
    onClickExpandTrigger: function(event) {
        var $el = $(event.currentTarget);
        var source = $el.attr('data-expand-source');

        var $targetEl = $('[data-expand-target="' + source + '"]');
        if ($targetEl.is(':visible')) {
            $targetEl.hide();
            $el.text('+');
            this.trigger('table-row-collapsed', source, $targetEl);
        } else {
            $targetEl.show();
            $el.text('-');
            this.trigger('table-row-expanded', source, $targetEl);
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
            method: 'post',
            args: _.extend({
                src_id: srcId,
                dst_id: dstId,
                sort_attr: this.initSort
            }, this.args),
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

    /**
     * onPressKeyInPopoverTextInput: 在popover text input敲回车的响应函数
     */
    onPressKeyInPopoverTextInput: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            var buttonEl = $(event.currentTarget).parent().find('.tx_searchable_confirm_btn').get(0);
            var submitEvent = {
                'currentTarget': buttonEl
            };
            this.onClickSearchableConfirmButton(submitEvent);
        }
    },

    /**
     * onClickSelectAll: 点击全选选择框时的响应函数
     */
    onClickSelectAll: function(event) {
        //xlog("in onClickSelectAll()");
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        this.$('tbody .xa-select').prop('checked', isChecked);
    },

    /**
    * onClickSelect: 点击单个选择框的响应函数
    */
    onClickSelect: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        //xlog("isChecked: " + isChecked);
        var isAllChecked = true;
        var unCheckedCount = 0;
        var isAnyUnChecked = false;
        this.$('tbody .xa-select').each(function() {
            var $select = $(this);
            //xlog($select.parents('tr').attr("data-id"));
            if (!$select.is(':checked')) {
                isAllChecked = false;
                unCheckedCount += 1;
            }
        });

        //xlog("isAllChecked: " + isAllChecked+", unCheckedCount:"+unCheckedCount);
        if (isAllChecked) {
            this.trigger('enter-select-all');
            if (this.outerSelecter) {
                var $outerSelecter = $(this.outerSelecter);
                var tagName = $outerSelecter.get(0).tagName.toLowerCase();
                if (tagName === 'input') {
                    $outerSelecter.prop('checked', true);
                }
            }
        }

        if (!isChecked && unCheckedCount === 1) {
            this.trigger('leave-select-all');
            if (this.outerSelecter) {
                var $outerSelecter = $(this.outerSelecter);
                var tagName = $outerSelecter.get(0).tagName.toLowerCase();
                if (tagName === 'input') {
                    $outerSelecter.prop('checked', false);
                }
            }
        }
    },

    reset: function() {
        //this.$('table').empty();
        this.$content.empty();
        this.frozenArgs = {};
    }

});

W.registerUIRole('div[data-ui-role="advanced-table"]', function() {
    xlog("registed advance-table");
    var $div = $(this);
    var app = $div.attr('data-app');
    var api = $div.attr('data-api');
    var resource = $div.attr('data-resource');    
    if (resource) {
        api = resource;
    }

    var apiMethod = $div.attr('data-method') || 'get';
    var args = $div.attr('data-args');
    var template = $div.attr('data-template-id');
    var initSort = $div.attr('data-init-sort');
    var enablePaginator = $div.data('enablePaginator');
    var enableSort = !!($div.attr('data-enable-sort') === 'true');
    var enableSelect = !!($div.attr('data-selectable') === 'true');
    var disableHeaderSelect = !!($div.attr('data-disable-header-select') === 'true');
    var selectableTrSelector = $div.data('selecttableTr');
    //var onlyShowFrontSelect = !!($div.attr('data-only-show-front-select') === 'true');
    var sortApi = $div.attr('data-sort-api');
    var itemCountPerPage = $div.attr('data-item-count-per-page');
    var userWebappId = $div.attr('data-user-webapp-id');
    var outerSelecter = $div.attr('data-outer-selecter');

    var autoLoad = $div.data('autoLoad');
    if (autoLoad !== false) {
        autoLoad = true;
    }

    if (itemCountPerPage) {
        itemCountPerPage = parseInt(itemCountPerPage);
    } else {
        itemCountPerPage = 15;
    }

    var advancedTable = new W.view.common.AdvancedTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
        apiMethod: apiMethod,
        initSort: initSort,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        enableSelect: enableSelect,
        disableHeaderSelect: disableHeaderSelect,
        //onlyShowFrontSelect: onlyShowFrontSelect,
        selectableTrSelector: selectableTrSelector,
        sortApi: sortApi,
        userWebappId: userWebappId,
        autoLoad: autoLoad,
        outerSelecter: outerSelecter
    });
    advancedTable.render();

    $div.data('view', advancedTable);
});
