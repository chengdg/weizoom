/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.Shortcuts = W.component.Component.extend({
	type: 'appkit.shortcuts',
	selectable: 'yes',
	propertyViewTitle: '',

	properties: [{
		group: '快捷模块',
		groupClass: 'xui-propertyView-app-Shortcuts',
		fields: [{
			name: 'modules',
			type: 'checkbox',
			displayName: '填写项',
			isUserProperty: true,
			source: [{
				name: '姓名',
				value: 'name',
				columnName: 'name',
			}, {
				name: '手机号',
				value: 'phone',
				columnName: 'phone',
			}, {
				name: '邮箱',
				value: 'email',
				columnName: 'email',
			}],
			default: {name:{select:true}, phone:{select:true}, email:{select:true}}
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
		modules: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		is_mandatory: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		}
	}
}, {
	indicator: {
		name: '快捷模块',
		imgClass: 'componentList_component_shortcuts' // 控件icon
	}
});
