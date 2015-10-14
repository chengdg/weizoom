ensureNS('W.dialog.mall');

W.dialog.mall.RedEnvelopeDetailDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectCoupon': 'onSelectCoupon',
        'click .xa-up': 'upCounter',
        'click .xa-down': 'downCounter',
        'click .xa-selectAll': 'onClickSelectAll'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#red-envelope-detail-dialog-tmpl-src').template('red-envelope-detail-dialog-tmpl');
        return "red-envelope-detail-dialog-tmpl";
    },
    /**
     * onClickSelectAll: 点击“全选”复选框的响应函数
     */
    onClickSelectAll: function(event) {
        var $checkbox = $(event.target);
        var isChecked = $checkbox.is(':checked');
        console.log(isChecked);
        $('.red-envelope-dialog .xa-select').prop('checked', isChecked);
        $('.red-envelope-dialog .xa-selectAll').prop('checked', isChecked);
    }
});
/**
 * RedShowDialog: ��ʾdialogNameָ����dialog
 */
W.dialog.RedShowDialog = function(dialogName, options) {
    var dialog = W.dialog.NAME2DIALOG[dialogName];
    if (dialog) {
        dialog.show(options);
        return;
    }

    //û��dialog������֮
    xlog('create new dialog: ' + dialogName);
    var obj = window;
    var items = dialogName.split('.');
    var itemCount = items.length-1;
    // ��λ����?
    for (var i = 0; i < itemCount; ++i) {
        var item = items[i];
        if (obj.hasOwnProperty(item)) {
            obj = obj[item];
        } else {
            obj = [];
            break;
        }
    }

    if (obj !== null) {
        //xlog(options);
        xlog("obj=");
        xlog(obj);
        var dialog = new obj(options);
        W.dialog.NAME2DIALOG[dialogName] = dialog;
        dialog.show(options);
    }
};