/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单支付弹出框
 *
 * author: robert
 */
ensureNS('W.dialog.member');

W.dialog.member.MemberIntegralDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#member-ingegral-logs-tmpl-src').template('member-ingegral-logs-tmpl');
        return "member-ingegral-logs-tmpl";
    },

    getMemberLogsTemplate: function() {
        $('#member-ingegral-log-tmpl-src').template('member-ingegral-log-tmpl-src');
        return "member-ingegral-log-tmpl-src";
    },

    onInitialize: function(options) {
        this.memberLogsTemplate = this.getMemberLogsTemplate();
         this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
          this.memberId = options.memberId;
    },

    onShow: function(options) {
        console.log('onShow', options.memberId);
        this.table.reload({member_id:this.memberId})
        //this.reloadLogs(options.memberId);
       
    },


    createCollection: function(datas, extra) {
        if (extra) {
            _.each(datas, function(data) {
                _.extend(data, extra);
            });
        }

        return new Backbone.Collection(datas);
    },


    reloadLogs: function(memberId){
        W.getApi().call({
            method: 'get',
            app: 'member',
            resource: 'integral_logs',
            args: {
                member_id: memberId
            },
            scope: this,
            success: function(data) {
                console.log(data)
                var log_count = data['member_logs'].length;
                var $logs = $.tmpl(this.memberLogsTemplate, {
                    'logs': data,
                    'log_count': log_count,
                });
                this.$('.xa-logTable').empty().append($logs);
            },
            error: function(resp) {

            }
        });
    }
});

