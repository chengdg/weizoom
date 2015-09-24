/**
 * @class W.component.appkit.SignDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.SignDescription = W.component.Component.extend({
	type: 'appkit.signdescription',
	selectable: 'yes',
	propertyViewTitle: '签到',

    dynamicComponentTypes: [{
        type: 'appkit.signitem',
        model: 366
    }],

	properties: [{
		group: '签到设置',
		groupClass: 'xui-propertyView-app-Selection',
		fields: [{
			name: 'title_group',
			type: 'title_with_annotation',
			displayName: '活动名称',
			isUserProperty: true
		},{
			name: 'title',
			type: 'text',
			displayName: '活动名称',
			isUserProperty: true,
			maxLength: 10,
			validate: 'data-validate="require-notempty::活动不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'description',
			type: 'textarea',
			displayName: '签到说明',
			maxLength: 200,
			isUserProperty: true,
			default: ''
		},{
			name: 'share_group',
			type: 'title_with_annotation',
			displayName: '分享设置',
			isUserProperty: true
		},{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '上传图片',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '格式：建议jpg.png 尺寸：50*50 不超过1M',
			default: ''
		},{
			name: 'share_description',
			type: 'textarea',
			displayName: '分享描述',
			maxLength: 200,
			isUserProperty: true,
			default: '签到赚积分啦！'
		},{
			name: 'reply_group',
			type: 'title_with_annotation',
			displayName: '自动回复',
			isUserProperty: true
		},{
			name: 'reply_keyword',
			type: 'text',
			displayName: '关键字',
			isUserProperty: true,
			maxLength: 10,
			//validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'reply_content',
			type: 'textarea',
			displayName: '回复内容',
			maxLength: 200,
			isUserProperty: true,
			default: '建议填写垫付近期活动通知，签到奖励等内容……'
		},{
			name: 'signsetting_group',
			type: 'title_with_annotation',
			displayName: '签到设置',
			isUserProperty: true
		},{
			name:'sign0_group',
			displayName:'每日签到',
			type:'title_with_annotation',
			isUserProperty:true

		},{
			name: 'sign0_points',
			type: 'text_with_annotation_v2',
			displayName: '送积分',
			isUserProperty: true,
			maxLength: 5,
			size: '70px',
			annotation: '积分',
			validate: 'data-validate="require-notempty::选项不能为空,,require-nonnegative::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'sign0_prizes',
			type: 'prize_selector_v4',
			displayName: '送优惠券',
			isUserProperty: true,
			help:"仅能选择限领为“不限”的优惠券",
			default:""
		},{
			name: 'items',//动态组件,那个加好
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: false,
            minItemLength: 2,
			maxItemLength: 4,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		image: function($node, model, value, $propertyViewNode) {
			var image = {url:''};
			var data = {type:null};
			if (value !== '') {
				data = $.parseJSON(value);
				image = data.images[0];
			}
			model.set({
				image: image.url
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

			if (value) {
				//更新propertyView中的图片
				$propertyViewNode.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
				$propertyViewNode.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
			}
		},
		items: function($node, model, value) {
			/*
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {
                    silent: true
                });
            });

            _.delay(_.bind(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this), 100);
			*/
            this.refresh($node, {resize:true, refreshPropertyView:true});
        }
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
