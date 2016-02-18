/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择红包会员对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectPromotionRedEnevlopDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectAll': 'onSelectALL',
        'click .xa-allin': 'onAllin',
        'click .xa-selectUser': 'onSelectUser',
    }, W.dialog.Dialog.prototype.events),


    getTemplate: function() {
        $('#mall-select-promotion-red-enevlop-dialog-tmpl-src').template('mall-select-promotion-product-dialog-tmpl');
        return "mall-select-promotion-product-dialog-tmpl";
    },

    onSelectUser: function(e){
        var isSelectUserCB = $(e.target).is(':checked');
        if(isSelectUserCB){
            if(this.$el.find('.xa-selectUser').length == this.$el.find('.xa-selectUser:checked').length){
                this.$el.find('.xa-selectAll').prop('checked', true);
            }
        }else{
            this.$el.find('.xa-selectAll').prop('checked', false);
        }
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="red-advanced-table"]').data('view');
        this.allin_input = false;
    },

    _initFooterCheckbox: function(){
        this.allin_input = false;
        this.$el.find('.xa-allin').prop('checked', false);
        this.$el.find('.xa-selectAll').attr('disabled', false);
        this.$el.find('.xa-selectAll').prop('checked', false);

        this.$el.find('.xa-selectUser').each(function(){
            $(this).prop('checked', false);
            $(this).attr('disabled', false);
        });

    },

    onAllin: function(event){
        var $modal_content = $(event.target).parents('.modal-content');
        if($(event.target).is(':checked')){
            this.allin_input = $(event.target).is(':checked');
            $modal_content.find('.xa-selectAll').attr('disabled', true);
            $modal_content.find('.xa-selectAll').prop('checked', true);
            $modal_content.find('.xa-selectUser').each(function(){
                $(this).prop('checked', true);
                $(this).attr('disabled', true);
            });
        }else{
            this.allin_input = $(event.target).is(':checked');
            $modal_content.find('.xa-selectAll').attr('disabled', false);
            $modal_content.find('.xa-selectAll').prop('checked', false);

            $modal_content.find('.xa-selectUser').each(function(){
                $(this).prop('checked', false);
                $(this).attr('disabled', false);
            });
        }

    },


    beforeShow: function(options) {
        this._initFooterCheckbox();
        this.allin_input = false;
        this.vip_options = options;

        var dataValue = [];
        if(options.name.value.length > 0){
            dataValue.push('name:' + options.name.value);

        }
        // 构造会员查询api
        if(options.grade_id.value != '-1'){
            dataValue.push('grade_id:' + options.grade_id.value);
        }
        if(options.member_tag.value != '-1'){
            dataValue.push('tag_id:' + options.member_tag.value);
        }
        if(options.member_source.value != '-1'){
            dataValue.push('source:' + options.member_source.value);
        }
        if(options.member_status.value != '-1'){
            dataValue.push('status:' + options.member_status.value);
        }
        if(options.integral.value != ''){
            dataValue.push('integral:' + options.integral.value);
        }
        var filter_value = dataValue.join('|');
        this.table.reload({
            'filter_value': filter_value,
            'allin': $('.xa-allin:checked').length
        })
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
    },

    onSelectALL: function(event){
        var $check_box = $(event.target);
        var $tbody = $(event.target).parents('table').children('tbody');
        if($check_box.is(":checked")){
            $tbody.find('.xa-selectUser').each(function(i){
                $(this).prop('checked',true);

            });
        }else{
            $tbody.find('.xa-selectUser').each(function(i){
                $(this).prop('checked',false);

            });

        }

    },

    onGetData: function(options) {
        // 初始化返回数据结构
        var data = {};
        data.is_group = false;
        data.items_ids = [];
        var _this = this;
        // 如果是全部全选
        if(this.allin_input){
            data.display_items = [];  // 显示红包查询信息

            // 构造会员查询信息
            if(this.vip_options.name.value != ""){  // 会员名称
                data.display_items.push(this.vip_options.name);
            }
            data.display_items.push(this.vip_options.grade_id);  // 会员等级
            data.display_items.push(this.vip_options.member_tag);  // 会员分组
            data.display_items.push(this.vip_options.member_source);  // 会员来源

            var vip_status = this.vip_options.member_status;  // 会员状态
            //vip_status.value = '1';
            vip_status.text = '关注';
            data.display_items.push(vip_status);

            // 积分范围
            if(this.vip_options.integral.value != ''){
                data.display_items.push(this.vip_options.integral);
            }

            //  构造会员查询api
            var filter_value = 'name:' + this.vip_options.name.value;
            if(this.vip_options.grade_id.value != '-1'){
                filter_value += '|' + 'grade_id:' + this.vip_options.grade_id.value;
            }
            if(this.vip_options.member_tag.value != '-1'){
                filter_value += '|' + 'tag_id:' + this.vip_options.member_tag.value;
            }
            if(this.vip_options.member_source.value != '-1'){
                filter_value += '|' + 'source:' + this.vip_options.member_source.value;
            }
            if(this.vip_options.integral.value != ''){
                filter_value += '|' + 'integral:' + this.vip_options.integral.value;
            }
            if(this.vip_options.member_status.value != '-1') {
                filter_value += '|' + 'status:' + this.vip_options.member_status.value;
            }
            var args = {
                'filter_value': filter_value,
                'count_per_page':999999999
            };
            W.getApi().call({
                app: 'member' ,
                api: 'member_list',
                method: 'get',
                args: args,
                success: function(vipdata){
                    data.is_group = true;
                    for(var i=0; i<vipdata.items.length; ++i){
                        data.items_ids.push(vipdata.items[i])
                    }
                    W.view.mall.PromotionRedProductView.prototype.addVipInfo(data);

                },
            });
        }else{ // 部分选择
            data.is_group = false;
            this.$('tbody tr').each(function() {
                var $tr = $(this);
                if ($tr.find('.xa-selectUser').is(':checked')) {
                    var productId = $tr.data('id');
                    data.items_ids.push(_this.table.getDataItem(productId).toJSON());
                }
                W.view.mall.PromotionRedProductView.prototype.addVipInfo(data);
            })
        }
        return data;
    }
});
