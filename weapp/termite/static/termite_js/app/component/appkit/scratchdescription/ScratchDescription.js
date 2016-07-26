/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ScratchDescription = W.component.Component.extend({
	type: 'appkit.scratchdescription',
	selectable: 'yes',
	propertyViewTitle: '刮刮卡',

	dynamicComponentTypes: [{
        type: 'appkit.scratchitem',
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
			name: 'scratch_bg_image',
			type: 'image_dialog_select_v2',
			displayName: '刮奖背景图',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示:建议图片长宽640px*500px',
			default: ""
		}, {
            name: 'background_color',
            type: 'color_picker',
            displayName: '刮奖背景颜色',
            isUserProperty: true,
            default: ''
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
			},
			{
				name: '不限',
				value: 'no_limit'
			}
			],
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
				case 'no_limit':
					value = '-1';
					break;
				default :
					value = '0';
					break;
			}
			var $header = $node.find('.wui-lotterydescription').find('.xa-header');
			if(value == '-1'){
				$header.addClass('wui-lotterydescription-hide');
			}else{
				$header.removeClass('wui-lotterydescription-hide').find('p b').html(value);
			}

		},
		scratch_bg_image: function($node, model, value, $propertyViewNode){
			var image = {url:''};
            var data = {type:null};
            if (value !== '') {
                data = $.parseJSON(value);
                image = data.images[0];
            }
            model.set({
                scratch_bg_image: image.url
            }, {silent: true});

            if (data.type === 'newImage') {
                W.resource.termite2.Image.put({
                    data: image,
                    success: function(data) {
                    },
                    error: function(resp) {
                    }
                })
            }
			var $target = $('#phoneIFrame').contents().find('.xa-scratchdescription');//找到子frame中的相应元素
			if (value) {
				//更新propertyView中的图片
				$target.css("background-image","url("+image.url+")");
			}
            this.refresh($node, {refreshPropertyView: true});
		},
		background_color: function($node, model, value, $propertyViewNode){
			if (value) {
				var $target = $('#phoneIFrame').contents().find('.xa-prizeContainer');//找到子frame中的相应元素
				var $target_2 = $('#phoneIFrame').contents().find('.xa-prizeContainer .xa-subtitle');
				var $target_3 = $('#phoneIFrame').contents().find('.xa-prizeContainer .xa-time');
				var $target_4 = $('#phoneIFrame').contents().find('.xa-prizeContainer .xa-description');
				$target.css("background-color", value);
				$target_2.css("background-color", value);
				$target_3.css("border-top", "1px solid #e5e5e5");
				$target_4.css("border-top", "1px solid #e5e5e5");
			}
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
