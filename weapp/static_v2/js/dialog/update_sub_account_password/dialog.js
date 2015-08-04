ensureNS('W.dialog.newmall');
W.dialog.newmall.UpdateSubAccountPassword = W.dialog.Dialog.extend({
    templates: {
        dialogTmpl: '#newmall-update-sub-account-password-dialog-tmpl-src'
    },

    onInitialize: function(options) {
    },

    beforeShow: function() {
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
    },

    onGetData: function(event) {
        xlog('in get data...');
        if (!W.validate($('#updateSubAccountPasswordDialog'))) {
            return false;
        }
        return $("#password").val();
    }
});