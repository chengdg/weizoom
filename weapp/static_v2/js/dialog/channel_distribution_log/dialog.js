ensureNS('W.dialog.mall');

W.dialog.mall.ChannelDistributionLog = W.dialog.Dialog.extend({
    events: _.extend({
        'change .xa-change': 'onChangeSelect'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#channel-distribution-log-dialog-tmpl-src').template('channel-distribution-log-dialog-tmpl-src-dialog-tmpl');
        return "channel-distribution-log-dialog-tmpl-src-dialog-tmpl";
    },

    getSearchMemberTepmplate: function() {
        $('#search-member-tmpl-src').template('search-member-tmpl');
        return "search-member-tmpl";
    },

    onInitialize: function(options) {
        this.qrocdeId = options.qrocdeId;
        $.tmpl(this.getTemplate(), {selectedMemberIds: 1});
        this.searchMemberTepmplate = this.getSearchMemberTepmplate();
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.table.reset();
    },

    onShow: function(options) {
        this.enableMultiSelection = false;
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
    },

    afterShow: function(options) {
        this.table.reload({
            'qrcode_id': this.qrocdeId
        });
    },

    // renderMemberFilter: function() {
    //     var _this = this;
    //     var args = {
    //         webapp_id: this.webapp_id,
    //     };
    //     W.getApi().call({
    //         app: 'mall2',
    //         resource: 'issuing_coupons_filter',
    //         args: args,
    //         success: function(data){
    //             var $node = $.tmpl(
    //                 _this.searchMemberTepmplate,
    //                 {grades: $.parseJSON(data.member_grade),
    //                  tags: $.parseJSON(data.member_tags)}
    //             );
    //             this.$('.xa-searchMember').empty().append($node);
    //         }
    //     });
    // },

    onClickSearchButton: function(event) {
        var filter_value = '';
        var name = $.trim($('#member_name').val());
        var group = $.trim($('#member_group').val());
        var grade = $.trim($('#member_grade').val());


        filter_value = 'name:' + name;
        if(grade != '-1') {
            filter_value += '|' + 'grade_id:' + grade;
        }
        if(group != '-1') {
            filter_value += '|' + 'tag_id:' + group;
        }

        filter_value += '|' + 'status:1';

        this.table.reload({
            'filter_value': filter_value
        })
    },

    // onClickResetButton: function(event) {
    //     $('#member_name').val('');
    //     $('#member_group').val(-1);
    //     $('#member_grade').val(-1);
    // },
    onChangeSelect: function(event){
        var logSelect = $.trim($('#log_select').val());
        this.table.reload({
            'log_select': logSelect,
            'qrocde_id': this.qrocdeId
        })
    },

    onGetData: function(options) {
        var data = [];
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectMember').is(':checked')) {
                var memberId = $tr.data('id');
                data.push(_this.table.getDataItem(memberId).toJSON());
            }
        })
        return data;
    }
})