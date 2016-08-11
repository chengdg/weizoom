ensureNS('W.dialog.mall');

W.dialog.mall.ChannelDistributionDetail = W.dialog.Dialog.extend({
    events: _.extend({
        'change .xa-change': 'onChangeSelect'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#channel-distribution-detail-dialog-tmpl-src').template('channel-distribution-detail-dialog-tmpl-src-dialog-tmpl');
        return "channel-distribution-detail-dialog-tmpl-src-dialog-tmpl";
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

    onChangeSelect: function(event){
        var logSelect = $.trim($('#log_select').val());
        this.table.reload({
            'log_select': 1,
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