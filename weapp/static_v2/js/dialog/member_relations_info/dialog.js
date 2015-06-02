/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 好友关系
 *
 * author: bert
 */
ensureNS('W.dialog.member');

W.dialog.member.RelationsDialog = W.dialog.Dialog.extend({
    events: _.extend({
       // 'change select': 'onChangeProjectType',
        'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-relations-tmpl-src').template('member-relations-tmpl');
        return "member-relations-tmpl";
    },

    getMemberLogsTemplate: function() {
        $('#member-relation-tmpl-src').template('member-relation-tmpl-src');
        return "member-relation-tmpl-src";
    },

    onInitialize: function(options) {
        
        this.getTemplate();
        this.memberLogsTemplate = this.getMemberLogsTemplate();
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
        
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
        this.memberId = options.memberId;
        $('.show_fans').attr('value', this.memberId);
    },

    onShow: function(options) {
        console.log('onShow', options.memberId);

        this.memberId = options.memberId;
        $('.show_fans').attr('checked',false);
        $('.show_fans').attr('value', this.memberId);
        var _this = this;
        if (options.isReload == true) {
            _this.table.curPage = 1;
        }
        $('#member-relations-tmpl-src').html('');
        $('.friend_count').text(options.friendCount);
        $('.fans_count').text(options.fansCount);
        _this.table.reload({member_id:options.memberId,only_fans:options.onlyFans})
       
    },

    onClickShowFansCheckbox: function(event){
        var $currentTarget = $(event.currentTarget);   
        var is_checked = $currentTarget.is(':checked');
        this.memberId = $currentTarget.val();
        if (is_checked){
            this.onlyFans = true;
        }else{
            this.onlyFans = false;
        }
        this.onFansShow(this);

    },

    onFansShow: function(event){
        this.table.reload({member_id: this.memberId,only_fans:this.onlyFans})
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
            app: 'member',
            api: 'member_logs/get',
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

