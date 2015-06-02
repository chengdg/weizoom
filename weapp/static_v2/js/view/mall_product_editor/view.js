/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductEditor = Backbone.View.extend({
	getImageTemplate: function() {
		$('#mall-product-editor-tmpl-image-src').template('mall-product-editor-tmpl-image');
		return 'mall-product-editor-tmpl-image';
	},

	getPropertyTemplate: function() {
		$('#mall-product-editor-tmpl-property-src').template('mall-product-editor-tmpl-property');
		return 'mall-product-editor-tmpl-property';
	},

	getPropertiesTemplate: function() {
		$('#mall-product-editor-tmpl-properties-src').template('mall-product-editor-tmpl-properties');
		return 'mall-product-editor-tmpl-properties';
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.imageTemplate = this.getImageTemplate();
		this.propertyTemplate = this.getPropertyTemplate();
		this.propertiesTemplate = this.getPropertiesTemplate();

		this.customModelEditor = this.$('[data-ui-role="mall-product-custom-model-editor"]').data('view');
	},

	events: {
		'click .xa-selectImage': 'onClickSelectImageButton',
		'mouseenter .xa-image': 'onEnterImage',
		'mouseleave .xa-image': 'onLeaveImage',
		'click .xa-deleteImage': 'onDeleteImage',
		'submit .xa-addProductForm': 'onSubmit',
		'click .xa-unifiedPostageInput': 'onClickUnifiedPostageInput',
		'change .xa-customPostageSelector': 'onSelectCustomPostage',
		'click .xa-customPostageSelectorLabel': 'onClickCustomPostageLabel',
		'change .xa-propertyTemplateSelector': 'onSelectPropertyTemplate',
		'click .xa-deleteProperty': 'onClickDeletePropertyLink',
		'click .xa-addProperty': 'onClickAddPropertyLink',
	},

	render: function() {
		// this.$('input[type="text"]').eq(0).focus();
	},

	onClickSelectImageButton: function(event) {
        var $target = $(event.currentTarget).parents('#imgSelect');    // 图片验证input的父节点
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectMallImagesDialog', {
			success: function(data) {
				var images = data;
				var $imageContainer = _this.$('.xui-i-images');
				var buf = [];
				var $images = _this.$('.xa-image');
				for (var i = 0; i < $images.length; ++i) {
					var $image = $images.eq(i);
					buf.push($image.clone());
				}
				var id = (0-$images.length);
				_.each(images, function(image) {
					id -= 1;
					image['id'] = id
					var $node = $.tmpl(_this.imageTemplate, {image: image});
					buf.push($node);
				});
				buf.push('<li class="xui-i-image  xa-selectImage" ><img src="/static_v2/img/editor/addProduct.png"/></li>');
				$imageContainer.empty().append(buf);

                // 验证是否提供图片
                // $target.children('#swipe_images').val(buf);
                // W.validate();

			}
		});
	},

	onEnterImage: function(event) {
		$(event.currentTarget).find('.xa-deleteImage').show();
	},

	onLeaveImage: function(event) {
		$(event.currentTarget).find('.xa-deleteImage').hide();
	},

	onDeleteImage: function(event) {
		var $li = $(event.currentTarget).parents('li').eq(0);
		var imageId = $li.data('imageId');
		$li.remove();
	},

	onClickUnifiedPostageInput: function(event) {
        var $input = $(event.currentTarget).parent().find(".xa-freight");
		event.stopPropagation();
		event.preventDefault();
		$(event.currentTarget).parents('label').find('input[type="radio"]').prop('checked', true);
        $input.trigger('click');
	},

	onSelectCustomPostage: function(event) {
		event.stopPropagation();
		event.preventDefault();

		$(event.currentTarget).parents('label').find('input[type="radio"]').prop('checked', true);
	},

	onClickCustomPostageLabel: function(event) {
		var $el = $(event.target);
		if ($el.hasClass('xa-customPostageSelector')) {
			event.stopPropagation();
			event.preventDefault();
		}
	},

	onSelectPropertyTemplate: function(event) {
		var $select = $(event.currentTarget);
		var templateId = $select.val();
//		if ("-1" === templateId) {
//            this.$('.xa-customProperties ul').empty();
//		} else {
            this.$('.xa-customProperties ul').empty();
			W.getApi().call({
				app: 'mall',
				api: 'template_properties/get',
				args: {id: templateId},
				scope: this,
				success: function(data) {
					var properties = data;
					for(var i = 0; i < properties.length; ++i) {
						//properties[i].value = '';
						properties[i].id = -1;
					}
					var $node = $.tmpl(this.propertiesTemplate, {properties: properties});
					$node.editable();
					this.$('.xa-customProperties ul').prepend($node);
				},
				error: function(resp) {
					W.showHint('error', '获取属性信息失败!')
				}
			});
//		}
	},

	onClickDeletePropertyLink: function(event) {
		var $link = $(event.currentTarget);
		$link.parents('li').remove();
	},

	onClickAddPropertyLink: function(event) {
		var $node = $.tmpl(this.propertyTemplate, {});
		$node.editable();
		this.$('div.xa-customProperties ul').append($node);
	},

	onSubmit: function(event) {
		//收集custom model信息
		var customModels = this.customModelEditor.getData();
		this.$('[name="customModels"]').val(JSON.stringify(customModels));

		//收集swipe image
		var swipeImages = [];
		this.$('.xa-image').each(function() {
			var $li = $(this);
			var width = $li.data('width');
			var height = $li.data('height');
			var id = $li.data('imageId');
			var url = $li.find('img').eq(0).attr('src');
			swipeImages.push({
				id: id,
				url: url,
				width: width,
				height: height
			})
		});

		//收集category
		var buf = [];
		this.$('.xa-product_category').each(function() {
			var $checkbox = $(this);
			if ($checkbox.is(":checked")) {
				buf.push($checkbox.val());
			}
		})
		this.$('#product_category').val(buf.join(','));

		//搜集swipe image
		this.$('[name="swipe_images"]').val(JSON.stringify(swipeImages));

		//收集property
		buf = [];
		this.$('.xa-property').each(function() {
			var $property = $(this);
			var id = $property.data('propertyId');
			var name = $.trim($property.find('.xa-name').val());
			var value = $.trim($property.find('.xa-value').val());
			buf.push({id:id, name:name, value:value});
		});
		this.$('input[name="properties"]').val(JSON.stringify(buf));

        if(!W.validate()){
            return false;
        }
	}
});
