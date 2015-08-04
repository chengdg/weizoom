/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * page visit表格
 * @class
 */

W.PageVisitTable = Backbone.View.extend({
	el: '',

	events: {
        'click th.wx-sortableTableHead': 'onClickSortableHead'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);

        this.table = this.$el.find('tbody');
        this.days = 7;
        this.sort = 'pv';
        this.direction = 'desc';

        this.tdTmpl = new W.Template(
            '<tr statistics_id="${id}">' +
                '<td><div class="fl"><a class="tx_displayNameLable" href="${url}" target="_blank" >${display_name_info}</a></div>' +
	            '<div class="fr">' +
	                '<a class="btn btn-mini tx_editDisplayName" href="#" title="编辑" data-display-name="${display_name}" data-id="${id}">' +
	                '<i class="icon-pencil"></i></a></div>' +
	            '</td>' +
                '<td style="width: 150px;">${pv_count}</td>' +
                '<td style="width: 150px;">${uv_count}</td>' +
            '</tr>'
        );
    },

    /**
     * 重新加载
     */
    reload: function(args) {
        W.getLoadingView().show();
        if (args) {
            this.days = args.days;
        }

        W.getApi().call({
            app: 'shop',
            api: 'page_visits/get',
            args: {
                sort: this.sort,
                direction: this.direction,
                days: this.days
            },
            success: function(data) {
                var page_visits = data;
                var $tbody = $('<tbody>');
                var tds = [];
                _.each(page_visits, function(page_visit) {
					console.log('ddddd', page_visit);
	                page_visit.display_name_info = page_visit.display_name;
	                if(page_visit.display_name === ''){
		                page_visit.display_name_info = page_visit.url;
	                }
                    tds.push(this.tdTmpl.render(page_visit));
                }, this);
                W.getLoadingView().hide();
                $('#pageVisitTable tbody').html(tds.join(''));
            },
            error: function(resp) {
                W.getLoadingView().hide();
            },
            scope: this
        })
    },

    /**
     * 点击排序head的响应函数
     */
    onClickSortableHead: function(event) {
        var $th = $(event.currentTarget);

        //在切换th时，将目标th的初始direction设置为desc
        var isSortActive = false;
        $th.find('i').each(function() {
            if ($(this).is(':visible')) {
                isSortActive = true;
            }
        });
        if (!isSortActive) {
            $th.attr('data-sort-next-direction', 'desc');
        }

        var sort = $th.attr('data-sort');
        var nextDirection = $th.attr('data-sort-next-direction');

        //显示相应的图标
        $('i.wx-icon').hide();
        if (nextDirection === 'asc') {
            $th.find('i.icon-arrow-up').css('display', 'inline-block');
            $th.attr('data-sort-next-direction', 'desc');
        } else {
            $th.find('i.icon-arrow-down').css('display', 'inline-block');
            $th.attr('data-sort-next-direction', 'asc');
        }

        //获取数据
        this.sort = sort;
        this.direction = nextDirection;
        this.reload();
    }
});