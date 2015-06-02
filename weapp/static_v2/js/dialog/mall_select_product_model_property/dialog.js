/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 定制商品规格的对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectProductModelPropertyDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectPropertyAllValue': 'onClickSelectPropertyAllValueCheckbox',
        'click .xa-selectOneValue': 'onClickSelectOneValueCheckbox',
        'click .xa-selectAllValue': 'onClickSelectAllValueCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-select-product-model-property-dialog-tmpl-src').template('mall-select-product-model-property-dialog-tmpl');
        return "mall-select-product-model-property-dialog-tmpl";
    },

    getPropertyTableTemplate: function() {
        $('#mall-select-product-model-property-dialog-property-table-tmpl-src').template('mall-select-product-model-property-dialog-property-table-tmpl');
        return "mall-select-product-model-property-dialog-property-table-tmpl";
    },

    onInitialize: function(options) {
        this.propertyTableTemplate = this.getPropertyTableTemplate();
    },

    onShow: function(options) {
        var _this = this;
        W.getApi().call({
            app: 'mall',
            api: 'product_model_properties/get',
            args: {},
            success: function(data) {
                if (data.length === 0) {
                    _this.$dialog.find('.modal-body').html('您还没有定制的规格属性，请关闭或<a href="/mall/model_properties/get/">定制规格属性</a>')
                } else {
                    var $node = $.tmpl(_this.propertyTableTemplate, {properties: data, selectedValues: options.selectedValues});
                    _this.$dialog.find('.modal-body').empty().append($node);

                    //判断每一个property是否所有的value都被选中，如果是，check“全选”
                    _this.$dialog.find('tbody tr').each(function() {
                        var $tr = $(this);
                        var $checkboxes = $tr.find('.xa-values input');
                        var isAllSelected = true;
                        for (var i = 0; i < $checkboxes.length; ++i) {
                            var $checkbox = $checkboxes.eq(i);
                            if (!$checkbox.is(":checked")) {
                                isAllSelected = false;
                                break;
                            }
                        }

                        if (isAllSelected) {
                            $tr.find('.xa-selectPropertyAllValue').prop('checked', true);
                        }
                    })
                }
            },
            error: function(resp) {
                W.getLoadingView().hide();
                W.getErrorHintView().show('加载商品规格失败！');
            }
        });
    },

    onClickSelectAllValueCheckbox: function(event) {
        var $checkbox = $(event.currentTarget);
        var isSelect = $checkbox.is(':checked');
        var $table = $checkbox.parents('table');
        $table.find('tbody input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            $checkbox.prop('checked', isSelect);
        })
    },

    onClickSelectPropertyAllValueCheckbox: function(event) {
        var $checkbox = $(event.currentTarget);
        var isSelect = $checkbox.is(':checked');
        var $tr = $(event.currentTarget).parents('tr');
        $tr.find('.xa-values input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            $checkbox.prop('checked', isSelect);
        });
    },

    onClickSelectOneValueCheckbox: function(event) {
        var $checkbox = $(event.currentTarget);
        var $td = $checkbox.parents('td');
        var $tr = $checkbox.parents('tr');
        var isAllSelected = true;
        $td.find('input[type="checkbox"]').each(function() {
            $checkbox = $(this);
            if (!$checkbox.is(':checked')) {
                //有没有选中的value，直接跳出
                isAllSelected = false;
            }
        });

        $tr.find('.xa-selectPropertyAllValue').prop('checked', isAllSelected);
    },

    onGetData: function(options) {
        var data = [];

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            var propertyName = $tr.data('modelPropertyName');
            var propertyId = $tr.data('modelPropertyId');
            var values = [];

            $tr.find('ul input[type="checkbox"]').each(function() {
                var $checkbox = $(this);
                if ($checkbox.is(":checked")) {
                    var $li = $checkbox.parents('li');
                    var propertyValueName = $li.data('modelPropertyValueName');
                    var propertyValueId = $li.data('modelPropertyValueId');
                    var propertyValueFullId = $li.data('modelPropertyValueFullId');
                    values.push({
                        id: propertyValueId,
                        name: propertyValueName,
                        fullId: propertyValueFullId
                    })
                }
            });

            if (values.length !== 0) {
                data.push({
                    propertyId: propertyId,
                    propertyName: propertyName,
                    values: values
                })
            }
        })

        return data;
    }
});