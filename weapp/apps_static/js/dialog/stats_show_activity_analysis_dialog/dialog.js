/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 营销传播分析中"结果分析"对话框
 *
 * 举例：http://dev.weapp.com/stats/activity_analysis/
 */
ensureNS('W.weapp.dialog');
W.weapp.dialog.ShowActivityAnalysisDialog = W.dialog.Dialog.extend({

    events: _.extend({
        'change select': 'onChangeProjectType',
        //'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#show-activity-analysis-dialog-tmpl-src').template('show-activity-analysis-dialog-tmpl');
        return "show-activity-analysis-dialog-tmpl";
    },

    getTableTemplate: function() {
        $('#activity-analysis-table-tmpl-src').template('activity-analysis-table-tmpl');
        return "activity-analysis-table-tmpl";
    },

    onInitialize: function(options) {
        //this.$el.html("<b>Hello, World!</b>");
        this.tableTemplate = this.getTableTemplate();
    },

    onShow: function(options) {
        var activityId = options.activityId;
        var activityType = options.activityType;

        //alert(activityId+", "+ activityType);

        var _this = this;
        W.getApi().call({
            app: 'stats',
            resource: 'activity_stats',
            args: {
                "id": activityId,
                "type": activityType,
            },
            success: function(data) {
                xlog(data);

                var $table = _this.$dialog.find('#activity-analysis-table');
                var $node = $.tmpl(_this.tableTemplate, {
                    stats: data.stats,
                    type: activityType,
                    data: data,
                });
                //xlog($node);
                $table.empty().append($node);
            }
        });
    },

});
