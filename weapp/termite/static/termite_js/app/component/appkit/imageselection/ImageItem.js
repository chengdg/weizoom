/**
 * @class W.component.appkit.ImageItem
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ImageItem = W.component.Component.extend({
	type: 'appkit.imageitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		gropuClass: 'xui-propertyView-app-dynamicItem',
		fields: [{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '选项',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'更换'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示：建议图片长宽100px*100px，正方形图片',
			validate: 'data-validate="require-notempty::请添加一张图片"',
			default: ""
		},{
			name: 'title',
			type: 'text',
			displayName: '   ',
			isUserProperty: true,
			maxLength: 20,
			validate: 'data-validate="require-notempty::选项不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '20字以内的图片描述'
		}
		//	,{
		//	name: 'mt',
		//	type: 'hidden',
		//	displayName: '',
		//	isUserProperty: false,
		//	default: '0'
		//}
		]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-text').text(value);
			//var parentComponent = W.component.getComponent(this.pid);
			//if('table' === parentComponent.model.get('disp_type')){
			//	var $target = $node.find('.wui-i-text');
			//	var h = parseInt($target.height()) || 0;
			//	var mt = (-h)+'px';
			//	$target.css('margin-top', mt);
			//	model.set({
			//		mt: mt
			//	}, {silent: true});
			//}
		},
		image: function($node, model, value, $propertyViewNode) {
			var image = {url:''};
			var data = {type:null};
			if (value !== '') {
				data = $.parseJSON(value);
				image = data.images[0];
			}
			model.set({
				image: image.url
			}, {silent: true});

			if (data.type === 'newImage') {
				W.resource.termite2.Image.put({
					data: image,
					success: function(data) {
					},
					error: function(resp) {
					}
				})
			}
			var cid = $propertyViewNode.attr('data-dynamic-cid');
			var $target = $('#phoneIFrame').contents().find('li[data-component-cid='+cid+']');//找到子frame中的相应元素
			$target.find('img').attr('src', image.url);
			this.refresh(null, {resize:true, refreshPropertyView: true, dynamicComponentId: $propertyViewNode.attr('data-parent-cid')});
		}
	}
});
