ensureNS('W.dialog.app.group');
W.dialog.app.group.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#app-group-viewParticipanceDataDialog-dialog-tmpl'
    },
    getTemplate: function() {
        $('#app-group-viewParticipanceDataDialog-dialog-tmpl').template('app-group-viewMembers-tmpl');
        return "app-group-viewParticipanceDataDialog-dialog-tmpl";
    },

    onInitialize: function(options) {
    	//s.activityId = options.activityId;
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');

    },

    beforeShow: function(options) {
        this.table.reset();

    },

    onShow: function(options) {
    },

    afterShow: function(options) {
        this.table.reload({});

    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        return {};
    }
});