ensureNS('W.dialog.app.group');
W.dialog.app.group.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#app-group-viewParticipanceDataDialog-dialog-tmpl',
        resultTmpl: 'app-group-viewMembers-tmpl'
    },
    onInitialize: function(options) {
    	//s.activityId = options.activityId;
        // this.table = this.$('[date-ui-role="advanced-table"]').data('view');

    },

    beforeShow: function(options) {
    	// console.log('fronted-->Dialog +66666666666666666666666');
    	// console.log(this.activityId);
        // console.log(this.table);
        // this.table.reset();
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
        this.activityId = options.activityId;
    },

    afterShow: function(options) {
        var that = this;
        if(this.activityId){
            W.getApi().call({
                app:'apps/group',
                resource: 'group_participance',
                scope: this,
                args: {
                    id: this.activityId
                },
                success: function(data) {
                    console.log('GGGGGGGGGGGGGGGGGGSSSSSSSSSSSSSS');
                    console.log(data);//数据是对的
                    this.$dialog.find('.modal-body').text(data);
                    var template = Handlebars.compile($(that.templates['resultTmpl']).html());
                    $('.xui-app_group-Dialog .modal-body').html(template(data));
                    // $('table img[data-toggle="tooltip"]').tooltip();
                },
                error: function(resp) {
                }
            })
        }
        // this.table.reload({});
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