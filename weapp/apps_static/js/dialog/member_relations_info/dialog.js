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
        'click .show_fans': 'onClickShowFansCheckbox',
        'click .show_friends': 'onClickShowFrinedsCheckbox'
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
        $('.show_friends').attr('value', this.memberId);
    },

    onShow: function(options) {
        console.log('onShow', options.memberId);

        this.memberId = options.memberId;
        //$('.show_fans').attr('checked',false);
        $('.show_fans').attr('value', this.memberId);
        $('.show_friends').attr('value', this.memberId);
        var _this = this;
        if (options.isReload == true) {
            _this.table.curPage = 1;
        }
        $('#member-relations-tmpl-src').html('');
        $('.friend_count').text(options.friendCount);
        $('.fans_count').text(options.fansCount);
        this.$('.show_friends').css('color','#333333');
        this.$('.show_fans').css('color','#fff');
        _this.table.reload({member_id:options.memberId,only_fans:options.onlyFans});

       
    },

    onClickShowFansCheckbox: function(event){
        var $currentTarget = $(event.currentTarget); 
        $currentTarget.css('color','#fff');  
        this.memberId = $currentTarget.val();
        this.onlyFans = true;
        this.$('.show_friends').css('color','#333333');
        this.onFansShow(this);

    },

    onClickShowFrinedsCheckbox: function(event){
        this.$('.show_fans').css('color','#333333');
        var $currentTarget = $(event.currentTarget);   
        this.memberId = $currentTarget.val();
        this.onlyFans = false;
        this.onFansShow(this);
         $currentTarget.css('color','#fff');  

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

