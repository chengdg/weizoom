/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择链接dialog
 */
ensureNS('W.dialog.termite');
W.dialog.termite.CreateProjectDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-template': 'onSelectTemplate',
        'click .xa-nav': 'onClickNav'
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#termite-create-project-dialog-tmpl-src'
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    reset: function() {
        var $currentSelected = this.$dialog.find('.xui-i-selectedTemplate');
        $currentSelected.removeClass('xui-i-selectedTemplate');
        $currentSelected.find('.xui-i-selectedIndicator').hide();
    },

    resetNav: function() {
        this.$dialog.find('.xui-i-activeNav').removeClass('xui-i-activeNav');
        var $link = this.$dialog.find('.xa-nav').eq(0);
        $link.addClass('xui-i-activeNav');
    },

    beforeShow: function() {
        this.table.reset();
        this.resetNav();
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
        this.fetchProjectTemplates();
    },

    fetchProjectTemplates: function() {
        var type = this.$dialog.find('.xui-i-activeNav').data('type');
        var param = {type: type};
        this.table.reload(param)
    },

    onSelectTemplate: function(event) {
        this.reset();

        var $li = $(event.currentTarget);
        $li.addClass('xui-i-selectedTemplate');
        $li.find('.xui-i-selectedIndicator').show();
    },

    onClickNav: function(event) {
        this.$dialog.find('.xui-i-activeNav').removeClass('xui-i-activeNav');
        var $link = $(event.currentTarget);
        $link.addClass('xui-i-activeNav');

        this.fetchProjectTemplates();
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var $activeTemplate = this.$dialog.find('.xui-i-selectedTemplate');
        var id = $activeTemplate.data('id');
        return {id:id}
    }
});