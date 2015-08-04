/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个微信会话的view
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductModelPropertyEditor = Backbone.View.extend({
	getTemplate: function() {
		$('#mall-product-model-property-editor-tmpl-src').template('mall-product-model-property-editor-tmpl');
		return 'mall-product-model-property-editor-tmpl';
	},

	getValueTemplate: function() {
		$('#mall-product-model-property-editor-single-value-tmpl-src').template('mall-product-model-property-editor-single-value-tmpl');
		return 'mall-product-model-property-editor-single-value-tmpl';
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		this.valueTemplate = this.getValueTemplate();
		this.cid = -1;
		this.values = options.values;
		this.isImageMode = options.initImageMode;
	},
	
	events: {
		'click .xa-addValueBtn': 'onClickAddValueButton',
		'click .xa-removeValueBtn': 'onClickRemoveValueButton',
		'click .xa-selectIcon': 'onClickSelectIconLink',
		'click .xa-changeIcon': 'onClickChangeIconLink',
		'keypress input[type="text"]': 'onPressKeyInInput'
	},

	render: function() {
		this.$el.html($.tmpl(this.template, {values: this.values, isImageMode: this.isImageMode}));
	},

	onClickAddValueButton: function(event) {
		var $node = $.tmpl(this.valueTemplate, {cid: this.cid, isImageMode: this.isImageMode});
		this.$('tbody').append($node);
		$node.find('input[type="text"]').focus();
		this.cid -= 1;
		event.stopPropagation();
	},

	onClickRemoveValueButton: function(event) {
		var $btn = $(event.currentTarget);
		$btn.parents('tr').eq(0).remove();
		event.stopPropagation();
	},

	onClickSelectIconLink: function(event) {
		var $link = $(event.currentTarget);
		W.dialog.showDialog('W.dialog.common.SelectUserIconDialog', {
			success: function(data) {
				var $td = $link.parents('td');
				$td.find('input[type="hidden"]').val(data);
				$td.find('img').attr('src', data);
				$td.find('.xa-selectZone').hide();
				$td.find('.xa-imageZone').show();
			}
		});
	},

	onClickChangeIconLink: function(event) {
		var $link = $(event.currentTarget);
		var $td = $link.parents('td');
		$td.find('input[type="hidden"]').val('');
		$td.find('.xa-imageZone').hide();
		$td.find('.xa-selectZone').show();
		
		W.dialog.showDialog('W.dialog.common.SelectUserIconDialog', {
			success: function(data) {
				$td.find('input[type="hidden"]').val(data);
				$td.find('img').attr('src', data);
				$td.find('.xa-selectZone').hide();
				$td.find('.xa-imageZone').show();
			}
		});
	},

	onPressKeyInInput: function(event) {
		var keyCode = event.keyCode;
        if(keyCode === 13) {
            event.stopPropagation();
            event.preventDefault();
        }
	},

	enterImageValueMode: function(event) {
		this.$('.xa-imageColumn').show();
		this.isImageMode = true;
	},

	enterTextValueMode: function(event) {
		this.$('.xa-imageColumn').hide();
		this.isImageMode = false;
	}
});

W.registerUIRole('[data-ui-role="product-model-property-value-editor"]', function() {
    var $container = $(this);
    var values = $.parseJSON($container.attr('data-values'));
    var initImageMode = ($.trim($container.attr('data-init-image-mode')) === 'true');
    var view = new W.view.mall.ProductModelPropertyEditor({
        el: this,
        values: values,
        initImageMode: initImageMode
    });
    view.render();

    $container.data('view', view);
});