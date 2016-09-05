/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择限定区域对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.EditProductLimitedAreaTemplateDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-edit-product-limited-area-template-tmpl-src').template('mall-edit-product-limited-area-template-tmpl');
        return "mall-edit-product-limited-area-template-tmpl";
    },
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
    },

    beforeShow: function(options) {
    },

    onShow: function(options) {
        
    },

    afterShow: function(options) {
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