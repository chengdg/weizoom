/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');

W.view.common.PostageConfigEditorSpecialConfigTable = Backbone.View.extend({
	events:  {
	},

    /**
     * getTemplate: 将options.template指定的模板源码编译为名为${options.template}-tmpl的模板
     */    
    getTemplate: function(options) {
	},

	getTdTemplate: function() {
		$('#mall-product-postage-config-editor-special-config-td-tmpl-src').template('mall-product-postage-config-editor-special-config-td-tmpl');
		return 'mall-product-postage-config-editor-special-config-td-tmpl';
	},
	
	initialize: function(options) {
		xlog('in editable table');
        //搜集field
        this.fields = [];
        var _this = this;
        this.$('th').each(function() {
            var $th = $(this);
            var field = $th.data('field');
            var isModelField = !!$th.data('modelField');
            var isEditable = !!$th.data('editable');
            var isUseDataValue = !!$th.data('useDataValue');
            _this.fields.push({
                name: field,
                isModelField: isModelField,
                isEditable: isEditable,
                isUseDataValue: isUseDataValue
            });
        });

        //td模板
        this.tdTemplate1 = _.template('<td <% if (field.isEditable) { %> contenteditable="true" class="xui-contenteditable xa-contenteditable" data-old-value="<%=value%>" <% } %> <% if (field.isUseDataValue) { %> data-use-data-value="true" <% } %> data-field="<%=field.name%>" data-model-field="<%=field.isModelField%>"><%=value%></td>')
        //this.tdTemplate = _.template('<td <% if (field.isUseDataValue) { %> data-use-data-value="true" <% } %> data-field="<%=field.name%>" data-model-field="<%=field.isModelField%>"><input type="text" value="<%=value%>" /></td>')
        this.tdTemplate = this.getTdTemplate();
	},

    /**
     * addRow: 向table中添加一行
     */
    addRow: function(data) {
        if (data.hasOwnProperty('id')) {
            var trId = data.id;
        } else {
            var trId = 0-this.$('tr').length;
        }
        
        var buf = ['<tr data-id="'+trId+'">'];
        var $tr = $('<tr data-id="'+trId+'">');
        _.each(this.fields, function(field) {
            var value = data[field.name];
            if (field.isEditable && !value) {
                value = '';
            }
            xlog($.tmpl(this.tdTemplate, {field:field, value:value}));
            $tr.append($.tmpl(this.tdTemplate, {field:field, value:value}));
            //var tdStr = this.tdTemplate({field:field, value:value})

            //buf.push(tdStr);
            //errorHintBuf.push('<td>请输入数字</td>');
        }, this);
        //buf.push('</tr>');
        //errorHintBuf.push('</tr>');
        //buf.push(errorHintBuf.join(''));

        //var $tr = $(buf.join(''));
        this.$('tbody').append($tr);
        var spe_btn_count = $('.xa-deleteSpecialPostageConfig').length;
        if(spe_btn_count === 1){
            $('.xa-deleteSpecialPostageConfig').hide();
        }else{
            $('.xa-deleteSpecialPostageConfig').show();
        }
        return $tr;
    },

    deleteRowById: function(targetId) {
        _.each(this.$('tr'), function($tr) {
            var id = $tr.data('id');
            if (id && id === targetId) {
                $tr.remove();
            }
        });
    },

    deleteRow: function($row) {
        $row.remove();
        var spe_btn_count = $('.xa-deleteSpecialPostageConfig').length;
        if(spe_btn_count === 1){
            $('.xa-deleteSpecialPostageConfig').hide();
        }else{
            $('.xa-deleteSpecialPostageConfig').show();
        }

    },

    getRowCount: function() {
        return this.$('tbody tr').length;
    },

    getData: function() {
        var _this = this;
        var datas = [];
        this.$('tbody tr').each(function() {
            var $tr = $(this);
            var data = {};
            data.id = parseInt($tr.data('id'));
            //抽取$tr中的model数据
            $tr.find('td').each(function() {
                var $td = $(this);
                var isModelField = !!$td.data('modelField');
                if (!isModelField) {
                    return;
                }

                var value = null;
                var isUseDataValue = !!$td.data('useDataValue');
                if (isUseDataValue) {
                    value = $td.data('value');
                } else {
                    value = $.trim($td.find('input[type="text"]').val());
                }
                
                var fieldName = $td.data('field');
                data[fieldName] = value;
            });
            datas.push(data);
        });

        return datas;
    }
});

W.view.mall.ProductPostageConfigEditor = Backbone.View.extend({
	getFreeConfigRowTemplate: function() {
		$('#mall-product-postage-config-editor-free-config-row-tmpl-src').template('mall-product-postage-config-editor-free-config-row-tmpl');
		return 'mall-product-postage-config-editor-free-config-row-tmpl';
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.freeConfigRowTemplate = this.getFreeConfigRowTemplate();

		this.specialConfigTable = new W.view.common.PostageConfigEditorSpecialConfigTable({
			el: '.xa-specialConfigTable'
		});
		this.specialConfigTable.render();

		this.specialConfigs = options.specialConfigs || [];
		//this.freeConfigs = options.freeConfigs || [];
	},
	
	events: {
		'click .xa-addSpecialConfig': 'onClickAddSpecialConfigButton',
		'click .xa-deleteSpecialPostageConfig': 'onClickDeleteSpecialConfigButton',
		'click .xa-addFreeConfig': 'onClickAddFreeConfigButton',
		'click .xa-deleteFreePostageConfig': 'onClickDeleteFreeConfigButton',
		'change .xa-freeConfigConditionType': 'onChangeFreeConfigConditionType',
		'click .xa-editProvince': 'onClickSelectProvince',
		'click .xa-enableFreeConfig': 'onClickEnableFreeConfig',
		'click .xa-enableSpecialConfig': 'onClickEnableSpecialConfig'
	},

	render: function() {
		//将free table的地址td上的data-value从字符串转为array
		this.$('.xa-freeConfigTable .xa-destination').each(function() {
			var $td = $(this);
			var oldValue = $td.data('value');
			if (typeof oldValue === 'string') {
				var newValue = oldValue.split(',');
				$td.data('value', newValue);	
			} else {
				$td.data('value', [oldValue+'']);
			}			
		});

		//填充special config
		_.each(this.specialConfigs, function(specialConfig) {
			var destinationDataValue = specialConfig['destination'];
			if (destinationDataValue.indexOf(',') > 0) {
				destinationDataValue = destinationDataValue.split(',');
			} else {
				destinationDataValue = [destinationDataValue];
			}
			var $tr = this.specialConfigTable.addRow({
				id: specialConfig['id'],
				destination: '<div\
								data-validate="require-custom-function"\
	    	                    data-validate-function="checkDestination">\
	    	                    <span class="xa-destinationText">'+specialConfig['destination_str']+'</span>\
	    	                    <a href="javascript:void(0);" class="ml10 xa-editProvince xui-block">编辑</a>\
	    	                 </div>\
	    	                 <div class="errorHint"></div>',
				firstWeight: parseFloat(specialConfig['first_weight']).toFixed(1),
				firstWeightPrice: parseFloat(specialConfig['first_weight_price']).toFixed(2),
				addedWeight: parseFloat(specialConfig['added_weight']).toFixed(1),
				addedWeightPrice: parseFloat(specialConfig['added_weight_price']).toFixed(2),
				actions: '<a href="javascript:void(0);" class="btn btn-xs xa-deleteSpecialPostageConfig">删除</a>'
			});
			$tr.find('[data-field="destination"]').data('value', destinationDataValue);
		}, this);

		this.$('input[name="name"]').focus();
	},

	getFreeConfigData: function() {
		var $freeConfigTable = this.$('.xa-freeConfigTable').eq(0);

		var datas = [];
		$freeConfigTable.find('tbody tr').each(function() {
			var $tr = $(this);
			var id = $tr.data('id');
			var destination = $tr.find('.xa-destination').data('value');
			var condition = $tr.find('.xa-freeConfigConditionType').val();
			var value = $.trim($tr.find('input[type="text"]').val());
			datas.push({
				id: id,
				destination: destination,
				condition: condition,
				value: value
			})
		});

		return datas;
	},

	onClickAddSpecialConfigButton: function(event) {
		this.specialConfigTable.addRow({
			destination: '<div\
							data-validate="require-custom-function"\
    	                    data-validate-function="checkDestination">\
    	                    <span class="xa-destinationText">未添加地区</span>\
    	                    <a href="javascript:void(0);" class="ml10 xa-editProvince xui-block">编辑</a>\
    	                 </div>\
    	                 <div class="errorHint"></div>',
			firstWeight: '1.0',
			firstWeightPrice: '',
			addedWeight: '1.0',
			addedWeightPrice: '',
			actions: '<a href="javascript:void(0);" class="btn btn-xs xa-deleteSpecialPostageConfig">删除</a>'
		});
	},

	onClickDeleteSpecialConfigButton: function(event) {
		var $tr = $(event.target).parents('tr');
        var tr_count = $tr.parent().children('tr').length;
        if(tr_count > 1){
            this.specialConfigTable.deleteRow($tr);
        }
	},

	onClickAddFreeConfigButton: function(event) {
		var $freeConfigTable = this.$('.xa-freeConfigTable').eq(0);
		var freeConfigId = 0 - $freeConfigTable.find('tr').length;
		var $node = $.tmpl(this.freeConfigRowTemplate, {id: freeConfigId});

		$freeConfigTable.find('tbody').append($node);
        var free_btn_count = $('.xa-deleteFreePostageConfig').length;
        if(free_btn_count === 1){
            $('.xa-deleteFreePostageConfig').hide();
        }else{
            $('.xa-deleteFreePostageConfig').show();
        }


	},

	onClickEnableSpecialConfig: function(event) {
		var $checkbox = $(event.target);
		if ($checkbox.is(':checked')) {
			if (this.specialConfigTable.getRowCount() === 0) {
				this.onClickAddSpecialConfigButton();
			}
		}
	},

	onClickEnableFreeConfig: function(event) {
		var $checkbox = $(event.target);
		if ($checkbox.is(':checked')) {
			if (this.$('.xa-freeConfigTable tbody tr').length === 0) {
				this.onClickAddFreeConfigButton();
			}
		}
        var free_btn_count = $('.xa-deleteFreePostageConfig').length;
        if(free_btn_count === 1){
            $('.xa-deleteFreePostageConfig').hide();
        }else{
            $('.xa-deleteFreePostageConfig').show();
        }

	},

	onClickDeleteFreeConfigButton: function(event) {
		var $tr = $(event.target).parents('tr');
        $tr.remove();
        var free_btn_count = $('.xa-deleteFreePostageConfig').length;
        if(free_btn_count === 1){
            $('.xa-deleteFreePostageConfig').hide();
        }else{
            $('.xa-deleteFreePostageConfig').show();
        }

	},

	onChangeFreeConfigConditionType: function(event) {
		var $select = $(event.target);
		var $tr = $select.parents('tr')
		var type = $select.val();
		$tr.find('.xa-conditionTypeText').hide();
		$tr.find('.xa-'+type+'Text').show();
	},

	onClickSelectProvince: function(event) {
		var $td = $(event.target).parents('td');
		var provinces = $td.data('value');

		//获得已被使用的province
		var $table = $td.parents('table');
		var provinceSet = {};
		if ($table.hasClass('xa-specialConfigTable')) {
			$table.find('.xa-destinationText').each(function() {
				var $tempTd = $(this).parents('td');
				var province_ids = $tempTd.data('value');
				if (province_ids) {
					if (provinces && province_ids[0] === provinces[0]) {
						//do nothing
						xlog('do nothing');
					} else {
						_.each(province_ids, function(province_id) {
							provinceSet[province_id] = 1;
						});
					}
				}
			});
		}
		
		W.dialog.showDialog('W.dialog.mall.SelectProvinceDialog', {
			provinces: provinces,
			disabledProvinceSet: provinceSet,
			success: function(data) {
				$td.data('value', data.ids);
				$td.find('.xa-destinationText').text(data.names);
			}
		})
	},

	getData: function(event) {
		var id = $.trim(this.$('input[name="id"]').val());
		var name = $.trim(this.$('input[name="name"]').val());
		var firstWeight = $.trim(this.$('input[name="firstWeight"]').val());
		var firstWeightPrice = $.trim(this.$('input[name="firstWeightPrice"]').val());
		var addedWeight = $.trim(this.$('input[name="addedWeight"]').val());
		var addedWeightPrice = $.trim(this.$('input[name="addedWeightPrice"]').val());
		var isEnableSpecialConfig = this.$('input[name="enableSpecialCofnig"]').is(':checked');
		var specialConfigs = this.specialConfigTable.getData();
		var isEnableFreeConfig = this.$('input[name="enableFreeCofnig"]').is(':checked');
		var freeConfigs = this.getFreeConfigData();

		var data = {
			id: id,
			name: name,
			firstWeight: firstWeight,
			firstWeightPrice: firstWeightPrice,
			addedWeight: addedWeight,
			addedWeightPrice: addedWeightPrice,
			isEnableSpecialConfig: isEnableSpecialConfig,
			specialConfigs: specialConfigs,
			isEnableFreeConfig: isEnableFreeConfig,
			freeConfigs: freeConfigs
		}
		return data;
	}
});
