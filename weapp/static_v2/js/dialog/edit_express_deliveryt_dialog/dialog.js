/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 编辑快递页面
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.ExpressDeliverDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#common-express-deliver-dialog-tmpl-src').template('common-express-deliver-dialog-tmpl');
        return "common-express-deliver-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.dataId = options.dataId;
        this.dataName = options.dataName;
        this.noOption = '<option value="-1" data-name="" data-id="-1">请选择快递公司</option>';
        this.oneOption = '<option value="${value}" data-name="${name}" data-id="${id}">${name}</option>';
    },

    onShow: function(options) {
        this.dataId = options.dataId;
        this.dataName = options.dataName;
        this.dataValue = options.dataValue;
        this.dataRemark = options.dataRemark;

        this.$expressSelectEl = $('select[name="express-value"]');
        this.$remarkEl = $('textarea[name="express-remark"]');      
        this.$remarkEl.val(this.dataRemark);
        this.$expressSelectEl.html('');
        if (this.dataId != -1) {
            this.$('.express-deliver-title').html('修改物流信息');
            var $option = $.tmpl(this.oneOption, {'value': this.dataValue, 'name': this.dataName});
            this.$expressSelectEl.append($option);
            this.$expressSelectEl.val(this.dataName);
        }else{
            this.$('.express-deliver-title').html('添加物流信息');
            this.$expressSelectEl.append(this.noOption);
        }
        this.initExpressDeliverSelect();
    },

    afterShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        xlog('in get data...');
        if (!W.validate($('#commonExpressDeliverDialog'))) {
            return '';
        }

        var remark = $('[name="express-remark"]').val();
        var value = $('[name="express-value"]').val();
        if (value == -1) {
            return '';
        }
        var $expressOptionEl = $('option[value="'+value+'"]');
        console.log('this.dataId', this.dataId)
        if (this.dataId == -1) {
            var args = {
                'name': $expressOptionEl.attr('data-name'),
                'express_number': $expressOptionEl.attr('data-id'),
                'express_value': value,
                'remark': remark
            }
            //var api = 'express_delivery/create';
            var method = 'put'
        }else{
            var args = {
                'id': this.dataId,
                'name': $expressOptionEl.attr('data-name'),
                'express_number': $expressOptionEl.attr('data-id'),
                'express_value': value,
                'remark': remark
            }
            //var api = 'express_delivery/update';
            var method = 'post'
        }
        this.sendExpressDeliverData(args, method);
        // name = request.POST.get('name'),
        // express_number = request.POST.get('express_number'),
        // express_value = request.POST.get('express_value'),
        // remark = response.POST.get('remark'),
        return true;
    },

    initExpressDeliverSelect: function(){        
        var _this = this;
        W.getApi().call({
            app: 'mall2',
            resource: 'express_delivery_company',
            args: {'source': 'init_express_deliverys'},
            success: function(data) {
                for (var i=0; i<data.length; i++ ) {
                    var $option = $.tmpl(_this.oneOption, data[i]);
                    // console.log(data[i], $option)
                    if(data[i]['value'] === _this.express_company_value){
                        $option.attr('selected','selected');
                    }
                    _this.$expressSelectEl.append($option);
                };

            },
            error: function() {
            }
        })
    },

    /*
     * 发送物流信息 'express_delivery/create'
     */
    sendExpressDeliverData:function(args, method){
        W.getApi().call({
            app: 'mall2',
            resource: 'express_delivery',
            args: args,
            method: method,
            success: function(data) {
            },
            error: function() {
            }
        })
    }
});
