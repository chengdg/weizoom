/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 定制商品规格的对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectProductModelPropertyDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectAllValue': 'onClickSelectAllValueCheckbox',
        'click .xa-selectOneValue': 'onClickSelectOneValueCheckbox',
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
        W.getLoadingView().hint('加载数据...').show();
        var _this = this;
        W.getApi().call({
            app: 'mall2',
            resource: 'model_property_list',
            args: {},
            success: function(data) {
                W.getLoadingView().hide();
                if (data.length === 0) {
                    _this.$dialog.find('.modal-body').html('您还没有定制的规格属性，请关闭或<a href="/mall/editor/mall_settings/">定制规格属性</a>')
                } else {
                    var $node = $.tmpl(_this.propertyTableTemplate, {properties: data, selectedValues: options.selectedValues});
                    _this.$dialog.find('.modal-body').empty().append($node);

                    //判断每一个property是否所有的value都被选中，如果是，check“全选”
                    var selectedValues = options.selectedValues;
                    _.each(data, function(property) {
                        var propertyValueIds = [];
                        _.each(property.values, function(value) {
                            propertyValueIds.push(property.id + ':' + value.id);
                        });

                        var isAllSelected = true;
                        for (var i = 0; i < propertyValueIds.length; ++i) {
                            if (!selectedValues.hasOwnProperty(propertyValueIds[i])) {
                                isAllSelected = false;
                                break;
                            }
                        }

                        if (isAllSelected) {
                            var trSelector = 'tr[data-model-property-id="'+property.id+'"]';
                            var selector = trSelector + ' .xa-selectAllValue';
                            _this.$dialog.find(selector).attr('checked', 'checked');
                        }
                    });
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
        var $tr = $(event.currentTarget).parents('tr');
        var $ul = $tr.find('ul');
        $ul.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            if (isSelect) {
                $checkbox.attr('checked', 'checked');
            } else {
                $checkbox.removeAttr('checked');
            }
        });
    },

    onClickSelectOneValueCheckbox: function(event) {
        var $checkbox = $(event.currentTarget);
        var $td = $checkbox.parents('td');
        var $tr = $checkbox.parents('tr');
        var isAllSelected = true;
        $td.find('input[type="checkbox"]').each(function() {
            if (!isAllSelected) {
                //如果已经判断出没有全选中，则不需要进行判断了，直接返回
                return;
            }

            $checkbox = $(this);
            if (!$checkbox.is(':checked')) {
                isAllSelected = false;
            }
        });

        if (isAllSelected) {
            $tr.find('.xa-selectAllValue').attr('checked', 'checked');
        } else {
            $tr.find('.xa-selectAllValue').removeAttr('checked');
        }
    },

    onGetData: function(options) {
        var data = [];

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            var propertyName = $tr.attr('data-model-property-name');
            var propertyId = $tr.attr('data-model-property-id');
            var values = [];

            $tr.find('ul input[type="checkbox"]').each(function() {
                var $checkbox = $(this);
                if ($checkbox.is(":checked")) {
                    var $li = $checkbox.parents('li');
                    var propertyValueName = $li.attr('data-model-property-value-name');
                    var propertyValueId = $li.attr('data-model-property-value-id');
                    values.push({
                        id: propertyValueId,
                        name: propertyValueName
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
