/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 目标页面导航结构的视图
 * @class
 */
W.model.Nav = Backbone.Model.extend({});

W.workbench.PageNavView = Backbone.View.extend({
	el: '',

	events: {
        'click input[type="button"]': 'onClickSubmitButton',
        'click .wx-delete': 'onClickDeleteNavButton'
	},

    getTemplate: function() {
        $('#page-nav-tmpl-src').template('page-nav-tmpl');
        return "page-nav-tmpl";
    },

    getTbodyTemplate: function() {
        $('#page-nav-navs-list-tmpl-src').template('page-nav-navs-list-tmpl');
        return "page-nav-navs-list-tmpl";
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.template = this.getTemplate();
        this.tbodyTemplate = this.getTbodyTemplate();

        this.navs = new Backbone.Collection();
        W.data.NAVS = null;
	},

    render: function() {
        this.$el.append($.tmpl(this.template, {}));
        this.$tbody = this.$('tbody');
    },

    /****************************************************
     * refresh: 刷新nav列表
     ****************************************************/
     refresh: function() {
        this.$tbody.empty().append($.tmpl(this.tbodyTemplate, {
            navs: this.navs.toJSON()
        }));
     },

    /****************************************************
     * onClickSubmitButton: 点击“确定”按钮的响应函数
     ****************************************************/
    onClickSubmitButton: function() {
        var displayName = $.trim(this.$('input[name="displayName"]').val());
        var value = $.trim(this.$('input[name="value"]').val());

        var nav = new W.model.Nav({
            displayName: displayName,
            value: value
        });
        nav.set({id: nav.cid}, {silent: true});
        this.navs.add(nav);

        //清空控件
        this.$('input[name="displayName"]').val('');
        this.$('input[name="value"]').val('');

        //刷新页面
        W.data.NAVS = this.navs.toJSON();
        this.refresh();

        //焦点切换到“显示名”
        this.$('input[name="displayName"]').focus();
    }, 

    /****************************************************
     * onClickDeleteNavButton: 点击一个nav的“删除”按钮的响应函数
     ****************************************************/
    onClickDeleteNavButton: function(event) {
        var $tr = $(event.currentTarget).parents('tr').eq(0);
        var id = $tr.attr('data-id');
        this.navs.remove(this.navs.get(id));

        this.refresh();
    }
});