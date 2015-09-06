/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.LotteryDescription = W.component.Component.extend({
	type: 'appkit.lotterydescription',
	selectable: 'yes',
	propertyViewTitle: '微信抽奖',

	dynamicComponentTypes: [{
        type: 'appkit.lotteryitem',
        model: 3
    }],

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-Selection',
		fields: [
		//	{
		//	name: 'lottery_type',
		//	type: 'radio',
		//	displayName: '微信抽奖',
		//	isUserProperty: true,
		//	validateIgnoreDefaultValue: true,
		//	source: [{
		//		name: '刮刮乐',
		//		value: 'scratch',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-scratch'
		//	}, {
		//		name: '大转盘',
		//		value: 'roulette',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-roulette'
		//	}, {
		//		name: '微信红包',
		//		value: 'red',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-red'
		//	}],
		//	default: {roulette:{select:true}}
		//},
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
			displayName: '活动说明',
			maxLength: 200,
			isUserProperty: true,
			default: ''
		}, {
			name: 'expend',
			type: 'text_with_annotation',
			displayName: '消耗积分',
			maxLength: 4,
			annotation: '积分数为0时，则为不消耗',
			validate: 'data-validate="require-notempty::消耗积分不能为空,,require-nonnegative::只能输入0和正整数"',
			validateIgnoreDefaultValue: true,
			size: '70px',
			isUserProperty: true,
			default: ''
		}, {
			name: 'delivery',
			type: 'text_with_annotation',
			displayName: '参与送积分',
			maxLength: 4,
			annotation: '积分数为0时，则为不送',
			validate: 'data-validate="require-notempty::参与送积分不能为空,,require-nonnegative::只能输入0和正整数"',
			validateIgnoreDefaultValue: true,
			size: '70px',
			isUserProperty: true,
			default: '0'
		}, {
			name: 'delivery_setting',
			type: 'radio',
			displayName: '送积分规则',
			isUserProperty: true,
			source: [{
				name: '仅限未中奖用户',
				value: 'true'
			}, {
				name: '所有用户',
				value: 'false'
			}],
			default: 'true'
		},{
			name: 'limitation',
			type: 'radio',
			displayName: '抽奖限制',
			isUserProperty: true,
			source: [{
				name: '一人一次',
				value: 'once_per_user'
			}, {
				name: '一天一次',
				value: 'once_per_day'
			}, {
				name: '一天两次',
				value: 'twice_per_day'
			}],
			default: 'once_per_user'
		},{
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
			name: 'allow_repeat',
			type: 'radio_with_annotation',
			displayName: '重复中奖',
			isUserProperty: true,
			annotation: '是否允许用户多次中奖',
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
			value = value.split(' ')[0].replace( /-/g,'.');
			$node.find('.wui-i-start_time').text(value);
			model.set({
				start_time: value
			}, {silent: true})
		},
		end_time: function($node, model, value, $propertyViewNode) {
			value = value.split(' ')[0].replace( /-/g,'.');
			$node.find('.wui-i-end_time').text(value);
			model.set({
				end_time: value
			}, {silent: true})
		},
		description: function($node, model, value, $propertyViewNode) {
			model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-description').html(value.replace(/\n/g,'<br>'));
		},
		expend: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-lotterydescription .xa-remainedIntegral strong').text(value);
		},
		delivery: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-prize>.xa-delivery').html(value);
		},
		limitation: function($node, model, value, $propertyViewNode) {
			switch (value){
				case 'once_per_user':
					value = '1';
					break;
				case 'once_per_day':
					value = '1';
					break;
				case 'twice_per_day':
					value = '2';
					break;
				default :
					value = '0';
					break;
			}
			$node.find('.wui-lotterydescription').find('.xa-header p b').html(value);
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
