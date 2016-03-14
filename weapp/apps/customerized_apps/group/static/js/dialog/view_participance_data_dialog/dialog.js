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
        this.table = this.$('[date-ui-role="advanced-table"]').data('view');

    },

    beforeShow: function(options) {
    	console.log('fronted-->Dialog +66666666666666666666666');
    	console.log(this.activityId);
        console.log(this.table);
        this.table.reset();
        // if (this.activityId) {
        //     W.getApi().call({
        //         app: 'apps/group',
        //         resource: 'group_participance',
        //         scope: this,
        //         args: {
        //             id: this.activityId
        //         },
        //         success: function(data) {
        //             this.$dialog.find('.modal-body').text(this.table);
        //         },
        //         error: function(resp) {
        //         }
        //     })
        // }
    },

    onShow: function(options) {
        // this.activityId = options.activityId;
    },

    afterShow: function(options) {
        this.table.reload({});
        // if (this.activityId) {
        //     W.getApi().call({
        //         app: 'apps/group',
        //         resource: 'group_participance',
        //         scope: this,
        //         args: {
        //             id: this.activityId
        //         },
        //         success: function(data) {
        //             this.$dialog.find('.modal-body').text(data);
        //         },
        //         error: function(resp) {
        //         }
        //     })
        // }
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        return {};
    }
});