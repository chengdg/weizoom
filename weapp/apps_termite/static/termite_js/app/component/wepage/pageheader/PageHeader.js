/**
 * @class W.component.wepage.PageHeader
 * 
 */
W.component.wepage.PageHeader = W.component.Component.extend({
	type: 'wepage.pageheader',
	propertyViewTitle: '',

	properties: [
		{
			group: '属性1',
			groupClass:'xui-propertyView-pageHeader',
			fields: [{
				name: 'backgroud',
				type: 'dialog_select',
				displayName: '背景图片',
				isUserProperty: true,
				triggerButton: {nodata:'选择图片', hasdata:'修改'},
				dialog: 'W.dialog.termite.SelectImagesDialog',
				help: '建议尺寸：640*200像素\n尺寸不匹配，图片将会被拉伸或压缩',
				isShowCloseButton: true,
				default: ''
			}, {
				name: 'logo',
				type: 'image_uploader',
				displayName: '店铺logo',
				isUserProperty: true,
				triggerButton: '+',
				help: '建议尺寸：640*200像素\n尺寸不匹配，图片将会被拉伸或压缩',
				dialog: 'W.dialog.termite.SelectImagesDialog',
				default: ''
			},{
				name: 'background_color',
				type: 'color_picker',
				displayName: '背景颜色',
				isUserProperty: true,
				default: '#256FB5'
			},{
				name: 'title',
				type: 'text',
				displayName: '店铺名称',
				maxLength: 15,
				// validate:true,js报错
				isUserProperty: true,
				placeholder:'店铺名称',
				default: '店铺名称'
			}]
		}
	],

	propertyChangeHandlers: {
		backgroud: function($node, model, value, $propertyViewNode) {
			var image = {url:''};
			var data = {type:null};
			if (value !== '') {
				data = $.parseJSON(value);
				image = data.images[0];
			}
			model.set({
				backgroud: image.url
			}, {silent: true});

			this.refresh($node, {refreshPropertyViewForField:'backgroud'});

			if (data.type === 'newImage') {
				W.resource.termite2.Image.put({
					data: image,
					success: function(data) {

					},
					error: function(resp) {

					}
				})
			}
		},
		logo: function($node, model, value, $propertyViewNode) {
			var $img = $node.find('img');
			if ($img.attr('src') == '' && value) {
				//从无图片到有图片
				$propertyViewNode.find('.xa-imageUploader').removeClass('xui-imageUploader-nodata').addClass('xui-imageUploader-hasdata');
				$propertyViewNode.find('.uploadify-button').text('修改');
			}

			$img.attr('src', value);
			$propertyViewNode.find('.xa-imageUploader-img').attr('src', value);
			$propertyViewNode.find('.xa-imageUploader-imgContainer').show();

			$node.find('img').attr('src', value);
			$propertyViewNode.find('.xa-imageUploader-img').show().attr('src', value);
			$propertyViewNode.find('.xa-imageUploader-imgContainer').show();
			/*
			console.log($propertyViewNode.find('.uploadify-button'),"3333333333333")
			
			$propertyViewNode.find('.xa-imageUploader-imgContainer').css('float','left');
			$propertyViewNode.find('.xa-imageUploader-uploader').css('float','left');
			$propertyViewNode.find('.help-block').css('display','none');
			$propertyViewNode.find('.uploadify-button').css({
				background: 'url()',
				color: '#1183C9',
				'float':'left',
				'line-height':'140px'
			}).text('修改店铺logo');
			*/
		},
		background_color: function($node, model, value, $propertyViewNode){
			$node.find('.wa-shop-backgroud').css('background-color', value);
		},
		title: function($node, model, value) {
			this.refresh($node, {resize: true});
		},
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
}, {
	indicator: {
		name: 'PageHeader',
		imgClass: 'componentList_component_page_header'
	},
	isManagerComponent: true
 });