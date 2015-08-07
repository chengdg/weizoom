/**
 * @class W.component.wepage.Image
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.TextSurvey = W.component.Component.extend({
	type: 'appkit.textsurvey',
	selectable: 'yes',
	propertyViewTitle: '文字调研',

	properties: [{
		group: '文本调研项',
		gropuClass: 'xui-propertyView-app-TextSurvey',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::标题名称不能为空"',
			validateIgnoreDefaultValue: true,
			default: '标题名称',
			placeholder: '标题名称'
		}, {
			name: 'optionType',
			type: 'radio',
			displayName: '单选/多选',
			isUserProperty: true,
			source: [{
				name: '单选',
				value: 'single'
			}, {
				name: '多选',
				value: 'multiple'
			}],
			default: 'single'
		}, {
			name: 'isMandatory',
			type: 'radio',
			displayName: '是否必填',
			isUserProperty: true,
			source: [{
				name: '是',
				value: 'yes'
			}, {
				name: '否',
				value: 'no'
			}],
			default: 'yes'
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			$node.find('.wa-inner-title').html(value);
		},

		optionType: function($node, model, value, $propertyViewNode) {
			xlog("in optionType(), value: " + value);
			// 改选显示方式
			W.Broadcaster.trigger('designpage:refresh'); // 刷新页面
			/*if (value == 'single') {
				$('[name="displaySize"]:first').click();
				$('[name="displaySize"]:last').parent().hide();
			} else {
				$('[name="displaySize"]:last').parent().show();
			}*/
			//W.Broadcaster.trigger('component:resize', this);
		},

		isStrict: function($node, model, value, $propertyViewNode) {
			xlog("in isStrict()");
		},

		option1: function($node, model, value, $propertyViewNode) {
			//W.Broadcaster.trigger('designpage:refresh'); // 刷新页面
			// TODO: 触发更新design page
		},

		option2: function($node, model, value, $propertyViewNode) {
			//W.Broadcaster.trigger('designpage:refresh'); // 刷新页面
		},

		option3: function($node, model, value, $propertyViewNode) {
			//W.Broadcaster.trigger('designpage:refresh'); // 刷新页面
		},

	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
}, {
	indicator: {
		name: '文字选项',
		imgClass: 'componentList_component_text_nav' // 控件icon
	}
});
