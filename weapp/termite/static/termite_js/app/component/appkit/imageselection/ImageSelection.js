/**
 * @class W.component.appkit.ImageSelection
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ImageSelection = W.component.Component.extend({
	type: 'appkit.imageselection',
	selectable: 'yes',
	propertyViewTitle: '',

	dynamicComponentTypes: [{
        type: 'appkit.imageitem',
        model: 3
    }],

	properties: [{
		group: '投票项',
		groupClass: '',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '标题名称',
			placeholder: '标题名称'
		}, {
			name: 'type',
			type: 'radio',
			displayName: '单选/多选',
			isUserProperty: true,
			source: [{
				name: '单选',
				value: 'single'
			}, {
				name: '多选',
				value: 'multi'
			}],
			default: 'single'
		}, {
			name: 'disp_type',
			type: 'radio',
			displayName: '图片展示',
			isUserProperty: true,
			source: [{
				name: '列表',
				value: 'list'
			}, {
				name: '表格',
				value: 'table'
			}],
			default: 'list'
		}, {
			name: 'is_mandatory',
			type: 'radio',
			displayName: '是否必填',
			isUserProperty: true,
			source: [{
				name: '是',
				value: 'true'
			}, {
				name: '否',
				value: 'false'
			}],
			default: 'true'
		}, {
            name: 'items',
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 2,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		type: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		disp_type: function($node, model, value, $propertyViewNode) {
			$node = this.refresh($node, {resize:true});
			//if('table' === value){
			//	var $target = $node.find('.wui-i-text');
			//	$target.each(function(){
			//		var $this = $(this);
			//		var cid = $this.parents('li').eq(0).attr('data-component-cid');
			//		var childComponent = W.component.getComponent(cid);
			//		var h = parseInt($this.height()) || 0;
			//		var mt = (-h)+'px';
			//		$this.css('margin-top', mt);
			//		childComponent.model.set({
			//			mt: mt
			//		}, {silent: true});
			//	});
			//}
		},
		is_mandatory: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		items: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true, refreshPropertyView: true});
		}
	}
}, {
	indicator: {
		name: '图片项',
		imgClass: 'componentList_component_imageselection' // 控件icon
	}
});
