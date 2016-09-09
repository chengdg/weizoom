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
        this.selectedIds = options.selectedIds;
    },

    beforeShow: function(options) {
        this.selectedIds = options.selectedIds;
        $('.xa-city-panel').hide();
        this.table.reload();
    },

    onShow: function(options) {
        
    },

    afterShow: function(options) {
        this.selectedIds.map(function(uid){
            $('input[data-uid='+ uid+']'[0]).siblings('i.xui-checkbox').trigger('click');
        })
    },
    onClickOpenCityPanel:function(event){
        var $panel = $(event.target).siblings('.xa-city-panel');
        var siblingsTrPanel = $(event.target).parents('tr').siblings('tr').find('.xa-city-panel');
        var siblingsLiPanel = $(event.target).parent('li').siblings('li').find('.xa-city-panel');
        $panel.show();
        $(siblingsTrPanel).hide();
        $(siblingsLiPanel).hide();
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
            $target.parents('.xa-city-panel').siblings('.xa-open-cityPanel').removeClass('xui-checked')
        }else{
            $input.prop('checked',true);
            $target.parents('.xa-city-panel').siblings('.xa-open-cityPanel').addClass('xui-checked')
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
        var isAllNotChecked = true;
        for (var i = 0; i < cityCount; ++i) {
            var $input = $li.eq(i).find('input');
                if ($input.is(':checked')) {
                    isAllNotChecked = false;
                    break;
                }
        }
        var $plus = $target.parents('.xa-city-panel').siblings('.xa-open-cityPanel');
        if(!isAllNotChecked){
            $plus.addClass('xui-checked');
        }else{
            $plus.removeClass('xui-checked');

        }
        $target.parents('.xa-city-panel').find('.xa-selectAllCity').siblings('input[type="checkbox"]').prop('checked', isAllChecked);

    },

    onGetData: function(event) {
        var provinces = {};
        this.$('input[type="checkbox"]:checked').each(function() {
            var $checkbox = $(this);
            var provinceId = $checkbox.attr('data-provinceId');

            if($checkbox.data('type') == 1){
                provinces[provinceId] =
                    {
                        provinceId:provinceId,
                        provinceName:$checkbox.attr('name'),
                        zoneName:$checkbox.attr('data-zoneName'),
                        cities:[]
                    };
            }else if($checkbox.data('type') == 2){
                if(!$checkbox.parents('.xa-city-panel').find('.xa-selectAll').is(':checked')){
                    if(!provinces[provinceId]){
                        provinces[provinceId] =
                            {
                                provinceId:provinceId,
                                provinceName:$checkbox.attr('data-provinceName'),
                                zoneName:$checkbox.attr('data-zoneName'),
                                cities:[{
                                    cityId:$checkbox.attr('data-cityId'),
                                    cityName:$checkbox.attr('name')
                                }]
                            }
                    }else{
                        provinces[provinceId].cities.push({cityId:$checkbox.attr('data-cityId'),cityName:$checkbox.attr('name')});
                    }
                }
            }
        });
        
        var provincesArray =[];
        var provinceObj = _.map(provinces,function(province,i){
            provincesArray.push(province);
        });
        return {
            provinces: provincesArray,
        };
    }
});