/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择限定区域对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.SelectLimitedAreaDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-select-limited-area-dialog-tmpl-src').template('mall-select-limited-area-dialog-tmpl');
        return "mall-select-limited-area-dialog-tmpl";
    },
    events: _.extend({
        'click .xa-selectAllProvince': 'onClickSelectAllProvince',
        'click .xa-checkbox': 'onClickSelectCity',
        'click .xa-selectAllCity': 'onClickSelectAllCity',
        'click .xa-open-cityPanel': 'onClickOpenCityPanel',
        'click .xa-close-city-panel': 'onClickCloseCityPanel'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        console.log('---------------------------',this.table)

    },

    beforeShow: function() {
        // this.$('input[type="checkbox"]').prop('checked', false).prop('disabled', false);
        
    },

    onShow: function(options) {
        // this.checkedProvinces = options.provinces || [];
        // this.disabledProvinceSet = options.disabledProvinceSet || {};
    },

    afterShow: function(options) {
    },
    onClickOpenCityPanel:function(event){
        var $panel = $(event.target).siblings('.xa-city-panel');
        $panel.show();
    },
    onClickCloseCityPanel:function(event){
        var $panel = $(event.target).parents('.xa-city-panel');
        $panel.hide();
    },
    onClickSelectAllCity: function(event) {
        var $target = $(event.target);
        var $input = $target.siblings('input');
        var isChecked = $input.is(":checked");
        if(isChecked){
            $input.prop('checked',false);
        }else{
            $input.prop('checked',true);
            // $target.parents('.xa-open-cityPanel').addClass('xui-checked')
        }
        isChecked = $input.is(":checked");
        var $li = $target.parents('.xa-city-panel').find('ul li').children('input').prop('checked', isChecked);
    },

    onClickSelectCity: function(event) {
        var $target = $(event.target);
        var $inputCurrent = $target.siblings('input[type="checkbox"]');
        if($inputCurrent.is(':checked')){
            $inputCurrent.prop('checked',false);
        }else{
            $inputCurrent.prop('checked',true);
            // $target.parents('.xa-open-cityPanel').addClass('xui-checked')
        }
        if($target.hasClass('xa-unique')){
            return;
        }
        var $li = $target.parent().parent('ul').children();
        var isAllChecked = true;
        var cityCount = $li.length;
        for (var i = 0; i < cityCount; ++i) {
            var $input = $li.eq(i).find('input');
                if (!$input.is(':checked')) {
                    isAllChecked = false;
                    break;
                }
        }
       $target.parents('.xa-city-panel').find('.xa-selectAllCity').siblings('input[type="checkbox"]').prop('checked', isAllChecked);
    },

    onGetData: function(event) {
        var provinces = [];
        this.$('input[type="checkbox"]:checked').each(function() {
            var $checkbox = $(this);
            if (!$checkbox.hasClass('xa-selectAllProvince')) {
                provinces.push({
                    id: $checkbox.val(),
                    name: $checkbox.parent().text()
                });
            }
        });

        provinces = _.sortBy(provinces, function(province) { return province.id; });
        var province_ids = [];
        var province_names = [];
        _.each(provinces, function(province) {
            province_ids.push(province.id);
            province_names.push(province.name);
        })
        return {
            ids: province_ids,
            names: province_names
        };
    }
});