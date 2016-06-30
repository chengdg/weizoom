/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ExlotteryDescription = W.component.Component.extend({
	type: 'appkit.exlotterydescription',
	selectable: 'yes',
	propertyViewTitle: '专项抽奖',

	dynamicComponentTypes: [{
        type: 'appkit.exlotteryitem',
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
			name: 'share_description',
			type: 'textarea',
			displayName: '分享简介',
			maxLength: 30,
			isUserProperty: true,
			validate: 'data-validate="require-notempty::分享简介不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '用于分享活动时的简略描述，不超过30字'
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
			name: 'homepage_image',
			type: 'image_dialog_select_v2',
			displayName: '首页背景图',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示:建议图片长款640px*500px',
			validate: 'data-validate="require-notempty::请添加一张图片"',
			default: ""
		}, {
			name: 'exlottery_bg_image',
			type: 'image_dialog_select_v2',
			displayName: '抽奖背景图',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示:建议图片长款640px*500px',
			default: ""
		}, {
            name: 'background_color',
            type: 'color_picker',
            displayName: '抽奖背景颜色',
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
			validate: 'data-validate="require-notempty::生成抽奖码不能为空,,require-nonnegative::只能输入0和正整数"',
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
		homepage_image: function($node, model, value, $propertyViewNode){
			var image = {url:''};
            var data = {type:null};
            if (value !== '') {
                data = $.parseJSON(value);
                image = data.images[0];
            }
            model.set({
                homepage_image: image.url
            }, {silent: true});

            // if (data.type === 'newImage') {
            //     W.resource.termite2.Image.put({
            //         data: image,
            //         success: function(data) {
            //         },
            //         error: function(resp) {
            //         }
            //     })
            // }
            this.refresh($node, {refreshPropertyView: true});
		},
		exlottery_bg_image: function($node, model, value, $propertyViewNode){
			var image = {url:''};
            var data = {type:null};
            if (value !== '') {
                data = $.parseJSON(value);
                image = data.images[0];
            }
            model.set({
                exlottery_bg_image: image.url
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
			var $target = $('#phoneIFrame').contents().find('.xa-exlotterydescription');//找到子frame中的相应元素
			if (value) {
				//更新propertyView中的图片
				$target.css("background-image","url("+image.url+")");
			}
            this.refresh($node, {refreshPropertyView: true});
		},
		background_color: function($node, model, value, $propertyViewNode){
			if (value) {
				var $target = $('#phoneIFrame').contents().find('.xa-prizeContainer');//找到子frame中的相应元素
				$target.css("background-color", value);
			}
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
