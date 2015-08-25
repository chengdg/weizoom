/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个微信会话的view
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductCustomModelEditor = Backbone.View.extend({
	getTemplate: function() {
		$('#mall-product-custom-model-property-editor-tmpl-src').template('mall-product-custom-model-property-editor-tmpl');
		return 'mall-product-custom-model-property-editor-tmpl';
	},

	getModelTableTemplate: function() {
		$('#mall-product-custom-model-property-editor-custom-model-table-tmpl-src').template('mall-product-custom-model-property-editor-custom-model-table-tmpl');
		return 'mall-product-custom-model-property-editor-custom-model-table-tmpl';
	},
	
	getIntegralTemplate: function() {
		$('#mall-integral-product-custom-model-property-editor-tmpl-src').template('mall-integral-product-custom-model-property-editor-tmpl');
		return 'mall-integral-product-custom-model-property-editor-tmpl';
	},

	getIntegralModelTableTemplate: function() {
		$('#mall-integral-product-custom-model-property-editor-custom-model-table-tmpl-src').template('mall-integral-product-custom-model-property-editor-custom-model-table-tmpl');
		return 'mall-integral-product-custom-model-property-editor-custom-model-table-tmpl';
	},

	events: {
		'click .xa-useCustomModel': 'onClickCustomModelCheckbox',
		'click .xa-selectProductModelProperty': 'onClickSelectProductModelButton',
		'click .xa-removeOneModel': 'onClickRemoveModelButton',
		'click .xa-stockTypeRadio': 'onClickStockTypeRadio',
		'click .xa-stock input[type="text"]': 'onClickInputInStockZone'
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		this.modelTableTemplate = this.getModelTableTemplate();
		this.isUseCustomModel = options.isUseCustomModel;
		this.customProperties = options.customProperties;
		this.productType = options.productType || "object";
		console.log(this.productType)
		if (this.productType === "integral") {
			this.template = this.getIntegralTemplate();
			this.modelTableTemplate = this.getIntegralModelTableTemplate();
		}

		this.name2model = {};
		this.models = options.models;
		this.standardModel = {};
		this.customModels = [];
		for (var i = 0; i < this.models.length; ++i) {
			var model = this.models[i];
			if (model.name === 'standard') {
				this.standardModel = model;
			} else {
				model['modelId'] = model['name'];
				model['propertyValues'] = model['property_values'];
				this.customModels.push(model);
			}
		}
		this.cacheModel(this.customModels);
	},

	render: function() {
		this.$el.html($.tmpl(this.template, {
			isUseCustomModel: this.isUseCustomModel,
			standardModel: this.standardModel
		}));

		if (this.isUseCustomModel && this.customModels.length > 0) {
			this.$('.xa-customModelTable').empty().append($.tmpl(this.modelTableTemplate, {
				headers: this.customProperties,
				models: this.customModels
			}))
		}
	},

	onClickCustomModelCheckbox: function(event) {
		var $checkbox = $(event.currentTarget);
		var isUseCustomModel = $checkbox.is(':checked');
		if (isUseCustomModel) {
			this.$('.xa-standardModel').hide();
			this.$('.xa-standardModel').find('[data-validate]').attr('data-ignore-validate', 'true');
			this.$('.xa-customModel').show();
			this.$('.xa-customModel').find('[data-validate]').removeAttr('data-ignore-validate');
		} else {
			this.$('.xa-customModel').hide();
			this.$('.xa-customModel').find('[data-validate]').attr('data-ignore-validate', 'true');
			this.$('.xa-standardModel').show();
			this.$('.xa-standardModel').find('[data-validate]').removeAttr('data-ignore-validate');
		}
	},

	cacheModel: function(customModels) {
		var _this = this;
		this.name2model = {};
		_.each(customModels, function(customModel) {
			_this.name2model[customModel['name']] = customModel
		});
	},

	/**
	 * convertFromSelectModelPropertyData: 将select model property对话框数据格式转换为view需要的格式
	 */
	convertFromSelectModelPropertyData: function(data) {
		/*
		 * 将数据结构：
		 * [
		 *		{propertyId:1, propertyName:'颜色', values:[{id:1, name:'黑色'}, {id:2, name:'白色'}]},
		 *		{propertyId:2, propertyName:'尺寸', values:[{id:3, name:'S'}, {id:4, name:'M'}]},
		 *	]
		 * 转换为:
		 * headers: [{id:1, name:'颜色'}, {id:2, name:'尺寸'}]
		 * values: [
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}],
		 ]
		 */
		var source = [];
		var target = [];
		var headers = [];
		var _this = this;
		_.each(data, function(property) {
			headers.push({
				id: property.propertyId, 
				name: property.propertyName
			});

			_.each(property.values, function(propertyValue) {
				var valueName = propertyValue.name;
				var valueId = propertyValue.id;
				if (source.length === 0) {
					target.push([{name:valueName, id:valueId, propertyId:property.propertyId}]);
				} else {
					_.each(source, function(sourceItem) {
						sourceItem = _.clone(sourceItem);
						sourceItem.push({
							name: valueName, 
							id: valueId,
							propertyId: property.propertyId
						})
						target.push(sourceItem);
					});
				}
			});

			source = target;
			target = [];
		});

		/*
		 * 将数据结构：
		 values: [
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}],
		 	[{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}],
		 ]
		 转换为:
		 models: [{
		 	modelId: '1:1_2:3',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:1_2:4',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}]
		 }, {
		 	modelId: '1:2_2:3',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:2_2:4',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}]
		 }]
		 */
		var models = [];
		_.each(source, function(values) {
			var ids = [];
			for (var i = 0; i < values.length; ++i) {
				var value = values[i];
				ids.push(value['propertyId']+':'+value['id']);
			}
			ids = _.sortBy(ids, function(id) { return id; });
			var modelId = ids.join('_');
			if (_this.name2model.hasOwnProperty(modelId)) {
				models.push(_this.name2model[modelId]);				
			} else {
				models.push({
					modelId: modelId,
					propertyValues: values
				})
			}
		});

		this.customProperties = headers;
		this.customModels = models;

		this.cacheModel(this.customModels);
	},

	/**
	 * convertToSelectModelPropertyData: 将view需要的格式转换为select model property对话框数据格式
	 */
	convertToSelectModelPropertyData: function(data) {
		/*
		 * 将数据结构：
		 headers: [{id:1, name:'颜色'}, {id:2, name:'尺寸'}]
		 models: [{
		 	modelId: '1:1_2:3',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:1_2:4',
		 	propertyValues: [{propertyId:1, id:1, name:'黑色'}, {propertyId:2, id:4, name:'M'}]
		 }, {
		 	modelId: '1:2_2:3',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:3, name:'S'}]
		 }, {
		 	modelId: '1:2_2:4',
		 	propertyValues: [{propertyId:1, id:2, name:'白色'}, {propertyId:2, id:4, name:'M'}]
		 }]
		 转换为：
		 [
		 	{propertyId:1, propertyName:'颜色', values:[{id:1, name:'黑色'}, {id:2, name:'白色'}]},
		 	{propertyId:2, propertyName:'尺寸', values:[{id:3, name:'S'}, {id:4, name:'M'}]},
		 ]
		*/
		property2values = {};
		selectedValues = {};
		_.each(this.customProperties, function(customProperty) {
			property2values[customProperty['id']] = {
				propertyId: customProperty['id'],
				propertyName: customProperty['name'],
				values: []
			}
		});

		_.each(this.customModels, function(customModel) {
			var propertyValues = customModel.propertyValues;
			for (var i = 0; i < propertyValues.length; ++i) {
				var propertyValue = propertyValues[i];
				var selectedValueId = propertyValue['propertyId'] + ':' + propertyValue['id'];
				selectedValues[selectedValueId] = 1
				var propertyId = propertyValue['propertyId'];
				property2values[propertyId].values.push(propertyValue);
			}
		});

		return selectedValues;
	},

	onClickSelectProductModelButton: function(event) {
		var selectedValues = this.convertToSelectModelPropertyData();
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectProductModelPropertyDialog', {
			selectedValues: selectedValues,
			success: function(data) {
				_this.convertFromSelectModelPropertyData(data);
				_this.$('.xa-customModelTable').empty().append($.tmpl(_this.modelTableTemplate, {
					headers: _this.customProperties,
					models: _this.customModels
				}))
			}				
		})
	},

	onClickRemoveModelButton: function(event) {
		var $button = $(event.currentTarget);
		var $tr = $button.parents('tr');
		$tr.remove();
	},

	onClickStockTypeRadio: function(event) {
		var $el = $(event.currentTarget);
    	var value = $el.attr('value');
    	var $stocksInput = $el.parents('td').find('.xa-stockCount');
    	if ($stocksInput.length === 0) {
    		var $stocksInput = $el.parents('div.controls').find('.xa-stockCount');
    	}
		if (value === '1') {
			$stocksInput.val('0').show();
			_.delay(function() {
				$stocksInput.val('0').focus();
			}, 100);
		} else {
			$stocksInput.val('-1').hide();
		}
	},

	onClickInputInStockZone: function(event) {
		event.stopPropagation();
		event.preventDefault();
	}
});

W.registerUIRole('[data-ui-role="mall-product-custom-model-editor"]', function() {
    var $container = $(this);
    var models = $container.data('models');
    var customProperties = $container.data('custom-properties');
    var isUseCustomModel = $container.data('use-custom-model');
    var productType = $container.data('product-type');
    var view = new W.view.mall.ProductCustomModelEditor({
        el: this,
        models: models,
        customProperties: customProperties,
        isUseCustomModel: isUseCustomModel,
        productType: productType
    });
    view.render();

    $container.data('view', view);
});