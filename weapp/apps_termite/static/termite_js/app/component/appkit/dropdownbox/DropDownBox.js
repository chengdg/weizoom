/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.DropDownBox = W.component.Component.extend({
	type: 'appkit.dropdownbox',
	selectable: 'yes',
	propertyViewTitle: '下拉选项',

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-DropDownBox',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 10,
			validate: 'data-validate="require-notempty::下拉选项标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '标题名称',
			placeholder: '标题名称'
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
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		is_mandatory: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		}
	}
}, {
	indicator: {
		name: '下拉选项',
		imgClass: 'componentList_component_dropdownbox' // 控件icon
	}
});
