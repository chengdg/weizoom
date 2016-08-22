/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ScanlotteryDescription = W.component.Component.extend({
	type: 'appkit.scanlotterydescription',
	selectable: 'yes',
	propertyViewTitle: '扫码抽奖',

	dynamicComponentTypes: [{
        type: 'appkit.scanlotteryitem',
        model: 3
    }],

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-Selection',
		fields: [
		{
			name: 'title',
			type: 'text',
			displayName: '活动标题',
			isUserProperty: true,
			maxLength: 10,
			validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '活动标题'
		}, {
			name: 'chance',
			type: 'text_with_annotation',
			displayName: '中奖率',
			isUserProperty: true,
			maxLength: 3,
			size: '70px',
			annotation: "%  <b style='color:#1262b7' id='lottery_chance_dialog_trigger'>中奖率详细规则</b>",
			validate: 'data-validate="require-notempty::中奖率不能为空,,require-percent::请输入1-100之间的数字"',
			validateIgnoreDefaultValue: true
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
			name: 'description',
			type: 'textarea',
			displayName: '活动规则',
			maxLength: 200,
			validate: 'data-validate="require-notempty::活动规则不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			isUserProperty: true,
			default: ''
		}, {
            name: 'items',
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: false,
            minItemLength: 3,
			maxItemLength: 3,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			$node.find('.xa-title').text(value);
		},
		start_time: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-start_time').text(value);
		},
		end_time: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-end_time').text(value);
		},
		description: function($node, model, value, $propertyViewNode) {
			model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-description .wui-i-description-content').html(value.replace(/\n/g,'<br>'));
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
