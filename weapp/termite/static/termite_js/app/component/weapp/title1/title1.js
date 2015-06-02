/**
 * @class W.component.weapp.Title
 *
 */
ensureNS('W.component.weapp');
W.component.weapp.title1 = W.component.Component.extend({
	type: 'weapp.title1',
	propertyViewtitle1: '标题',

	properties: [{
		group: '属性1',
		fields: [{
			name: 'title1',
			type: 'text',
			displayName: '标题名',
			isUserProperty: true,
			default: '请输入标题名'
		}, {
			name: 'subtitle1',
			type: 'text',
			displayName: '副标题',
			isUserProperty: true;,
			default: ''
		}, {
			name: 'align',
			type: 'radio',
			displayName: '显示',
			isUserProperty: true,
			source: [{
				name: '居左',
				value: 'left'
			}, {
				name: '居中',
				value: 'center'
			}, {
				name: '居右',
				value: 'right'
			}],
			default: 'left'
		}, {
			name: 'background_color',
			type: 'dialog_select',
			displayName: '背景色',
			isUserProperty: true,
			triggerButton: '选择颜色...',
			dialog: 'W.dialog.workbench.SelectColorDialog',
			isUserProperty: true,
			default: 'F46B41'
		}]
	}],

	propertyChangeHandlers: {
		title1: function($node, model, value) {
			$node.find('h2').text(value);
			W.Broadcaster.trigger('component:resize', this);
		},
		subtitle1: function($node, model, value) {
			$node.find('span').text(value);
			W.Broadcaster.trigger('component:resize', this);
		},
		align: function($node, model, value) {
			$node.css('text-align', value);
		},
		background_color: function($node, model, value) {
			$node.css('background-color', value);
		}
	}
}, {
	indicator: {
		name: '标题',
		imgClass: 'componentList_component_heading'
	}
});