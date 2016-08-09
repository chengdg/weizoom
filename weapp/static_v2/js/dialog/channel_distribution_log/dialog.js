ensureNS('W.dialog.mall');

W.dialog.mall.ChannelDistributionLog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectMember': 'onSelectMember',
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
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
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.table.reset();
    },

    onShow: function(options) {
        this.renderMemberFilter();
        this.enableMultiSelection = false;
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
    },

    afterShow: function(options) {
        var currentMemberId = $('.xa-selectMemberName').attr('data-id') | 0;
        this.table.reload({
            'currentMemberId': currentMemberId
        });
    },

    renderMemberFilter: function() {
        var _this = this;
        var args = {
            webapp_id: this.webapp_id,
            filter_type: 'member'
        };
        W.getApi().call({
            app: 'mall2',
            resource: 'issuing_coupons_filter',
            args: args,
            success: function(data){
                var $node = $.tmpl(
                    _this.searchMemberTepmplate,
                    {grades: $.parseJSON(data.member_grade),
                     tags: $.parseJSON(data.member_tags)}
                );
                this.$('.xa-searchMember').empty().append($node);
            }
        });
    },

    onSelectMember: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

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

    onClickResetButton: function(event) {
        $('#member_name').val('');
        $('#member_group').val(-1);
        $('#member_grade').val(-1);
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