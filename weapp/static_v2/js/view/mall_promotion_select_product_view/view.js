ensureNS('W.view.mall');
W.view.mall.PromotionSelectProductView = Backbone.View.extend({
	getTemplate: function() {
		$('#mall-promotion-select-product-view-tmpl-src').template('mall-promotion-select-product-view-tmpl');
		return 'mall-promotion-select-product-view-tmpl';
	},

	getModelInfoTemplate: function() {
		$('#mall-product-list-view-model-info-tmpl-src').template('mall-product-list-view-model-info-tmpl');
		return 'mall-product-list-view-model-info-tmpl';
	},

	events: {
		'click .xa-search': 'onClickSearchButton',
		'click .xa-reset': 'onClickResetButton',
		'click .xa-delete': 'onClickDeleteProduct',
		'click .xa-showAllModels': 'onClickShowAllModelsButton',
		'click .xa-selectAll': 'onClickSelectAll'
	},

	initialize: function(options) {
		this.$el = $(options.el);
		this.products = null;
		this.enableMultiSelection = false;
		if (options.hasOwnProperty('enableMultiSelection')) {
			this.enableMultiSelection = options.enableMultiSelection;
		}

		this.enableTableItemSelectable = false;
		if (options.hasOwnProperty('enableTableItemSelectable')) {
			this.enableTableItemSelectable = options.enableTableItemSelectable;
		}

		this.promotionId = 0;
		if (options.hasOwnProperty('promotionId')) {
			this.promotionId = options.promotionId;
		}

		this.tableTemplate = options.tableTemplate;
		$('#'+this.tableTemplate).template(this.tableTemplate);

		this.modelInfoTemplate = this.getModelInfoTemplate();
		// 已经选择的商品id
		this.selectedProductIds = [];
		this.filter_type = options.filter_type
	},

	render: function() {
		var $node = $.tmpl(this.getTemplate(), {});
		this.$('.xa-productSelectConditionPanel').empty().append($node);
		if (this.promotionId !== 0) {
			W.getApi().call({
				app: 'mall2',
				resource: 'promotion',
				args: {type: 'promotion_products', id: this.promotionId},
				scope: this,
				success: function(data) {
                    alert(data);
					this.addProducts(data);
					this.trigger('finish-select-products', data);
				},
				error: function(resp) {
					W.showHint('error', '获取促销的商品信息失败!');
				}
			})
		}
	},

	getData: function() {
		var products = [];
		this.$('tbody tr').each(function() {
			var $tr = $(this);
			var productId = $tr.data('id');
			var modelId = $tr.data('modelId');
			var data = {
				id: productId,
				model_id: modelId
			}

			var $inputs = $tr.find('input[name]');
			var inputCount = $inputs.length;
			for (var i = 0; i < inputCount; ++i) {
				var $input = $inputs.eq(i);
				data[$input.attr('name')] = $input.val();
			}

			products.push(data);
		});

		return products;
	},

	addProducts: function(products) {
		this.$('.errorHint').hide();

		if (this.enableMultiSelection) {
			if (!this.products) {
				this.products = products;
			} else {
				this.products = this.products.concat(products);
			}
		} else {
			this.products = products;
		}

		var $node = $.tmpl(this.tableTemplate, {products: products});
		if (this.enableTableItemSelectable) {
			$node.find('thead tr').prepend('<th width="30"><input type="checkbox" class="xa-selectAll" /></th>');
			$node.find('tbody tr').each(function() {
				var $tr = $(this);
				$tr.prepend('<td><input type="checkbox" class="xa-select" /></td>');
			});
		}
		if (this.enableMultiSelection) {
			var $tbody = this.$('.xa-selectedProductList tbody');
			if ($tbody.length > 0) {
				$tbody.append($node.find('tbody tr'));
			} else {
				this.$('.xa-selectedProductList').empty().append($node);
			}
		} else {
			this.$('.xa-selectedProductList').empty().append($node);
			$node.find('input[type="text"]').eq(0).focus();
		}

		for (var i = 0; i < products.length; i++) {
			this.selectedProductIds.push(products[i].id);
		};
	},

	getAllSelectedItems: function() {
		var $trs = [];
		this.$('tbody .xa-select').each(function() {
			var $checkbox = $(this);
			if ($checkbox.is(":checked")) {
				var $tr = $checkbox.parents('tr');
				$trs.push($tr.clone());
			}
		});

		return $trs;
	},

	onClickSearchButton: function(){
		var name = $.trim(this.$('[name="name"]').val());
		var barCode  = $.trim(this.$('[name="bar_code"]').val());
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectPromotionProductDialog', {
			enableMultiSelection: this.enableMultiSelection,
			name: name,
			barCode: barCode,
			selectedProductIds: _this.selectedProductIds,
			success: function(data) {
				_this.addProducts(data);
				_this.trigger('finish-select-products', data);
			},
			filter_type: _this.filter_type
		});
	},

	onClickResetButton: function(){
		this.$('[name="bar_code"]').val('');
		this.$('[name="name"]').val('').focus();
	},

	onClickDeleteProduct: function(event) {
		var $tr = $(event.currentTarget).parents('tr').eq(0);
		var productId = parseInt($tr.attr('data-id'));
		$tr.remove();

		if (this.$('tbody tr').length === 0) {
			this.$('.xa-selectedProductList').empty().text('请通过查询选择参与活动的商品');
		}

		for (var i = 0; i < this.selectedProductIds.length; i++) {
			if (this.selectedProductIds[i] === productId) {
				this.selectedProductIds.splice(i, 1);
			}
		};
	},

	/**
	 * onClickSelectAll: 点击全选选择框时的响应函数
	 */
	onClickSelectAll: function(event) {
		var $checkbox = $(event.currentTarget);
		var isChecked = $checkbox.is(':checked');
		this.$('tbody .xa-select').prop('checked', isChecked);
	},

	/**
	 * onClickShowAllModelsButton: 鼠标点击“查看规格”区域的响应函数
	 */
	onClickShowAllModelsButton: function(event) {
		var $target = $(event.currentTarget);
		var $tr = $target.parents('tr');
		var id = parseInt($tr.data('id'));
		var product = _.find(this.products, function(product) { return product.id === id});
		var models = product['models'];
		xlog(models);
		var properties = _.pluck(models[0].property_values, 'propertyName');
		xlog(properties);
		var $node = $.tmpl(this.modelInfoTemplate, {properties: properties, models: models});
		W.popup({
			$el: $target,
			position:'top',
			isTitle: false,
			msg: $node
		});
	},
});
