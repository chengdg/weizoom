/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.SurveyDescription = W.component.Component.extend({
	type: 'appkit.surveydescription',
	selectable: 'yes',
	propertyViewTitle: '调研简介',

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-TextSurvey',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '活动标题'
		}, {
			name: 'subtitle',
			type: 'text',
			displayName: '副标题',
			maxLength: 30,
			isUserProperty: true,
			default: ''
		}, {
			name: 'description',
			type: 'rich_text',
			displayName: '内容',
			isUserProperty: true,
			default: ''
		}, {
			name: 'start_time',
			type: 'hidden',
			displayName: '开始时间',
			isUserProperty: false,
			default: ''
		}, {
			name: 'end_time',
			type: 'hidden',
			displayName: '结束时间',
			isUserProperty: false,
			default: ''
		}, {
			name: 'valid_time',
			type: 'date_range_selector',
			displayName: '有效时间',
			isUserProperty: true,
			validate: 'data-validate="require-notempty::有效时间不能为空"',
			validateIgnoreDefaultValue: true,
			default: ''
		}, {
			name: 'permission',
			type: 'radio',
			displayName: '活动权限',
			isUserProperty: true,
			source: [{
				name: '无需关注即可参与',
				value: 'no_member'
			}, {
				name: '必须关注才可参与',
				value: 'member'
			}],
			default: 'member'
		}, {
			name: 'prize',
			type: 'prize_selector',
			displayName: '活动奖励',
			isUserProperty: true,
			default: {type:"no_prize", data:null}
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		subtitle: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		description: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		start_time: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		end_time: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		prize: function($node, model, value) {
			this.refresh($node, {resize:true});
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
