/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 发货的对话框
 * 
 * author: liupeiyu
 */
ensureNS('W.view.mall');
W.view.mall.Weixin2FansRemarkView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#fans_remark_info_view').template('remark-info-view-dialog-tmpl');
        return "remark-info-view-dialog-tmpl";
    },

    getOneTemplate: function() {
        $('#single-logistics-info-view').template('single-logistics-info-view-dialog-tmpl');
        return "single-logistics-info-view-dialog-tmpl";
    },

    events: {
        'click .xa-submit': 'submit',
    },

    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    },

    submit: function(event) {
        var $el = $(event.currentTarget);
        //xlog("currentTarget:");
        //xlog(event.currentTarget);
        var newRemark = ($('input[name="fans_remark"]').val()).replace(/\s/gi,'');
        if (newRemark.length > 20) {
            W.showHint('error', '备注姓名不能超过20个字');
            return;
        }

        // 修改粉丝备注名称
        var _this = this;
        W.getApi().call({
            method: 'post',
            app: 'new_weixin',
            api: 'fans_memo',
            args: {
                'member_id': this.member_id,
                'member_remarks': newRemark,
            },
            success: function(data) {
                W.getSuccessHintView().show("修改成功");
                // 更新备注名称
                var displayRemark;
                if(newRemark) {
                    displayRemark = newRemark + "(" + _this.nickname + ")";
                    _this.$action.attr('data-remark', newRemark);
                } else {
                    displayRemark = _this.nickname;
                    _this.$action.attr('data-remark', '');
                }
                _this.$display.html(displayRemark);
                // TODO: 应该有漂亮的解决方案
                $('.' + _this.privateContainerClass).hide(); // 对话框关闭
            },
            error: function(data) {
                var msg = data.errMsg || '修改备注失败';
                W.getErrorHintView().show(msg);
                // TODO: 应该有漂亮的解决方案
                $('.' + _this.privateContainerClass).hide(); // 对话框关闭                    
            }
        });
    },

    validate: function() {

    },

    render: function() {
        this.$content.html($.tmpl(this.getTemplate()));
    },

    onShow: function(options) {
        this.$content.html($.tmpl(this.getTemplate()));
        this.position = options.position;

        $('.modal-backdrop').css({
            'background-color': '#fff',
            'opacity': '0'
        })
    },

    showPrivate: function(options) {
        this.$display = options.$display;
        this.member_id = options.member_id; // fanId
        this.member_remarks = options.member_remarks; // 备注名
        this.nickname = options.nickname; // 用户昵称
        this.$content.html($.tmpl(this.getTemplate(), {
            'member_remarks': this.member_remarks
        }));
    },

    clickIsNeedLogistics: function(event) {
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
        if (isNeedLogistics === '1') {
            $('.xa-ship-detail-from').show();
        } else {
            $('.xa-ship-detail-from').hide();
        }
    }

});


W.getWeixin2FansRemarkView = function(options) {
    var dialog = W.registry['W.view.mall.Weixin2FansRemarkView'];
    if (!dialog) {
        //创建dialog
        xlog('create W.view.mall.Weixin2FansRemarkView');
        dialog = new W.view.mall.Weixin2FansRemarkView(options);
        W.registry['W.view.mall.Weixin2FansRemarkView'] = dialog;
    }
    return dialog;
};
