/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.UploadImg = W.component.Component.extend({
	type: 'appkit.uploadimg',
	selectable: 'yes',
	propertyViewTitle: '上传图片',

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-UploadImg',
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
		name: '上传图片',
		imgClass: 'componentList_component_uploadimg' // 控件icon
	}
});
