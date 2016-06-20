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
			name: 'share_description',
			type: 'textarea',
			displayName: '分享说明',
			maxLength: 30,
			isUserProperty: true,
			default: '',
			placeholder: '用于分享活动时的简略描述，不超过30字'
		}, {
			name: 'expend',
			type: 'text_with_annotation',
			displayName: '消耗积分',
			maxLength: 4,
			annotation: '积分数为0时，则为不消耗',
			validate: 'data-validate="require-notempty::消耗积分不能为空,,require-nonnegative::只能输入0和正整数"',
			size: '70px',
			isUserProperty: true,
			default: 0
		}, {
			name: 'delivery',
			type: 'text_with_annotation',
			displayName: '参与送积分',
			maxLength: 4,
			annotation: '积分数为0时，则为不送',
			validate: 'data-validate="require-notempty::参与送积分不能为空,,require-nonnegative::只能输入0和正整数"',
			size: '70px',
			isUserProperty: true,
			default: 0
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
			name: 'lottery_code_count',
			type: 'text_with_annotation',
			displayName: '生成抽奖码',
			isUserProperty: true,
			maxLength: 10,
			size: '70px',
			annotation: "张",
			validate: 'data-validate="require-notempty::生成抽奖码不能为空,,require-percent::请输入纯数字"',
			validateIgnoreDefaultValue: true
		}, {
			name: 'reply',
			type: 'text',
			displayName: '自动回复语设置',
			isUserProperty: true,
			maxLength: 30,
			validate: 'data-validate="require-notempty::自动回复语不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
		}, {
			name: 'reply_link',
			type: 'text',
			displayName: '自动回复超链接',
			isUserProperty: true,
			maxLength: 30,
			validate: 'data-validate="require-notempty::自动回复超链接不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
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
			$node.find('.wui-i-start_time').text(value);
		},
		end_time: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-end_time').text(value);
		},
		description: function($node, model, value, $propertyViewNode) {
			model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-description .wui-i-description-content').html(value.replace(/\n/g,'<br>'));
		},
		expend: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-lotterydescription .xa-remainedIntegral strong').text(value);
		},
		delivery: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-prize>.xa-delivery').html(value);
		},
		// limitation: function($node, model, value, $propertyViewNode) {
		// 	switch (value){
		// 		case 'once_per_user':
		// 			value = '1';
		// 			break;
		// 		case 'once_per_day':
		// 			value = '1';
		// 			break;
		// 		case 'twice_per_day':
		// 			value = '2';
		// 			break;
		// 		case 'no_limit':
		// 			value = '-1';
		// 			break;
		// 		default :
		// 			value = '0';
		// 			break;
		// 	}
		// 	var $header = $node.find('.wui-lotterydescription').find('.xa-header');
		// 	if(value == '-1'){
		// 		$header.addClass('wui-lotterydescription-hide');
		// 	}else{
		// 		$header.removeClass('wui-lotterydescription-hide').find('p b').html(value);
		// 	}
        //
		// }
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
