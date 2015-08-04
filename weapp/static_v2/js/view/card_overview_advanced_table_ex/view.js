/*
Copyright (c) 2011-2015 Weizoom Inc
*/
/**
 * AdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table
 */
ensureNS('W.view.common');

W.view.common.AdvancedTable_ex = W.view.common.AdvancedTable.extend({

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
            scope: this,
            success: function(data) {
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

                //advanced_tables ex 方法吧 data数据传出去
                if (data.data){
                   render_overview_tables(data.data);
                }


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
                alert('加载分类失败!');
                return false;
            }
        });
    },


});

W.registerUIRole('div[data-ui-role="advanced-table-ex"]', function() {
    xlog("registed advance-table");
    var $div = $(this);
    var app = $div.attr('data-app');
    var api = $div.attr('data-api');
    var resource = $div.attr('data-resource');
    if (resource) {
        api = resource;
    }
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

    var advancedTable_ex = new W.view.common.AdvancedTable_ex({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
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
    advancedTable_ex.render();

    $div.data('view', advancedTable_ex);
});
