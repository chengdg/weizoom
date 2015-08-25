/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.QA = W.component.Component.extend({
	type: 'appkit.qa',
	selectable: 'yes',
	propertyViewTitle: '问答',

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-QA',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::问答标题不能为空,,require-word::请输入除\' . \' , \' _ \'和\' $ \'以外的字符"',
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
		name: '问答',
		imgClass: 'componentList_component_qa' // 控件icon
	}
});
