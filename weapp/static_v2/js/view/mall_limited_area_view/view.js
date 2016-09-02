ensureNS('W.view.mall');
W.view.mall.limitedAreaSelectorView = Backbone.View.extend({
	getTemplate: function() {
		$('#selected-limited-area-view-tmpl-src').template('selected-limited-area-view-tmpl');
		return 'selected-limited-area-view-tmpl';
	},

	events: {
		'click .xa-edit': 'onClickEdit',
	},

	initialize: function(options) {
		this.$el = $(options.el);
		// 已经选择的商品id
		this.selectedProductIds = [];
	},

	render: function() {
		var $node = $.tmpl(this.getTemplate(), {provinces:[]});
		this.$('.xa-selectedLimitedArea').empty().append($node);
		// if (this.promotionId !== 0) {
		// 	W.getApi().call({
		// 		app: 'mall2',
		// 		resource: 'promotion',
		// 		args: {type: 'promotion_products', id: this.promotionId},
		// 		scope: this,
		// 		success: function(data) {
  //                   alert(data);
		// 			this.addProducts(data);
		// 		},
		// 		error: function(resp) {
		// 			W.showHint('error', '获取促销的商品信息失败!');
		// 		}
		// 	})
		// }
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
	onClickEdit:function(){
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectLimitedAreaDialog', {
			success: function(data) {
				console.log('---------------',data.provinces)
				var $node = $.tmpl(_this.getTemplate(), {provinces: data.provinces});
				_this.$('.xa-selectedLimitedArea').empty().append($node);
			}
		});
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
		// 按照id去重
		this.products = _.uniq(this.products, false, 'id');

		if (this.filter_type === 'integral_sale') {
			// 积分应用
			var $node = $.tmpl(this.tableTemplate, {products: this.products});

			this.$('.xa-selectedProductList').empty().append($node);
			$node.find('input[type="text"]').eq(0).focus();
		} else {			
			var $node = $.tmpl(this.tableTemplate, {products: products});

			if (this.enableTableItemSelectable) {
				$node.find('thead tr').prepend('<th width="30"><input type="checkbox" class="xa-selectAll" /></th>');
				$node.find('tbody tr').each(function() {
					var $tr = $(this);
					$tr.prepend('<td><input type="checkbox" class="xa-select" /></td>');
				});
			}
			if(this.tableOutAllSelectable){
				$node.find('thead tr').prepend('<th width="30"></th>');
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

		}
		this.selectedProductIds = [];
		for (var i = 0; i < this.products.length; i++) {
			this.selectedProductIds.push(this.products[i].id);
		};

		this.trigger('finish-select-products', this.products);
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
	getAllSelectedItemsIds: function() {
		var ids = [];
		this.$('tbody .xa-select').each(function() {
			var $checkbox = $(this);
			if ($checkbox.is(":checked")) {
				var $tr = $checkbox.parents('tr');
				ids.push($tr.data('id'));
			}
		});

		return ids;
	},

	addProductsHasCategory: function (category_ids) {
		var _this = this;
		W.getApi().call({
			method: 'get',
			app: 'mall2',
			resource: 'category_products',
			args: {
				promotion_type: 'integral_sale',
				category_ids: category_ids.join(','),
			},
			scope: this,
			success: function(successData) { 
				_this.addProducts(successData.products);
			},
			error: function() {
				W.showHint('error','获取分组中的商品失败，请稍后重试！');
			}
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
		this.products = _.filter(this.products, function(product){ return product.id !== productId; });
		
		this.trigger('finish-select-products', this.products);
	},
	onClickBatchDelete:function(event){

		var ids = this.getAllSelectedItemsIds();
		for (var i = 0; i < ids.length; i++) {
			var id = ids[i];
			this.selectedProductIds.pop(id);
			$('[data-id="'+id+'"]').remove();
		};
		
		if (this.$('tbody tr').length === 0) {
			this.$('.xa-selectedProductList').empty().text('请通过查询选择参与活动的商品');
		}
	},
	/**
	 * onClickSelectAll: 点击全选选择框时的响应函数
	 */
	onClickSelectAll: function(event) {
		var $checkbox = $(event.currentTarget);
		var isChecked = $checkbox.is(':checked');
		this.$('tbody .xa-select').prop('checked', isChecked);
	},
	onClickSelect:function(envent){
		var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        var isAllChecked = true;
        this.$('tbody .xa-select').each(function() {
            var isChecked = $(this).is(':checked');
            if (!isChecked) {
                isAllChecked = false;
                $('.xa-selectAll').attr('checked', false);
            }
        });
        if (isAllChecked) {
            $('.xa-selectAll').attr('checked', true);
        }
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
