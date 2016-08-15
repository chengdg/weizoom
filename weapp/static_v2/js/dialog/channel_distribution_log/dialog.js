ensureNS('W.dialog.mall');

W.dialog.mall.ChannelDistributionLog = W.dialog.Dialog.extend({
    events: _.extend({

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
        $.tmpl(this.getTemplate(), {selectedMemberIds: 1});
        this.searchMemberTepmplate = this.getSearchMemberTepmplate();
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.qrocdeId = options.qrocdeId;
        this.table.reload({
            'qrcode_id': this.qrocdeId
        });
    },

    onShow: function(options) {
        this.enableMultiSelection = false;
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
    },

    afterShow: function(options) {
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