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
        model: 2
    }],

	properties: [
		{
		group: '占空位',
		groupClass: '',
		fields: [{
		}]},{
		group: '活动名称',
		groupClass: 'xui-propertyView-app-SignNameGroup',
		fields: [{
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
		}]},{
		group:'分享设置',
		groupClass:'xui-propertyView-app-ShareGroup',
		fields:[{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '上传图片',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '注:不上传则使用默认图片,建议尺寸90*90，仅支持jpg/png',
			default: ''
		},{
			name: 'share_description',
			type: 'textarea',
			displayName: '分享描述',
			maxLength: 200,
			isUserProperty: true,
			default: '签到赚积分啦！'
		}]},{
		group:"自动回复",
		groupClass:'xui-propertyView-app-ReplyGroup',
		fields:[{
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
		}]},{
			group:"签到设置",
			groupClass:"xui-propertyView-app-SignSettingGroupName",
			groupHelp:{
				text:'奖励说明',
				handler: 'W.component.appkit.SignDescription.handleHelp',
				id:'outerFunctionTrigger'
			},
			fields:[{
				name:'SignSettingGroupName',
				isUserProperty: true,
				type:'title'
			}]
		},{
		group:"",
		groupClass:'xui-propertyView-app-SignSettingGroup',
		fields:[{
			name:'daily_group',
			displayName:'每日签到',
			type:'title_with_annotation',
			isUserProperty:true

		},{
			name: 'daily_points',
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
			name: 'daily_prizes',
			type: 'prize_selector_v4',
			displayName: '送优惠券',
			isUserProperty: true,
			help:"仅能选择限领为“不限”的优惠券",
			default:""
		}]},{
		group:"",
		groupClass:"xui-propertyView-app-SignynamicGroup",
		fields:[{
			name: 'items',//动态组件,那个加好
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: false,
            minItemLength: 2,
			maxItemLength: 10,
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
            this.refresh($node, {resize:true, refreshPropertyView:true});
        },
		daily_points:function($node, model, value){
			$node.find('.daily_points').text(value);

		},
		daily_prizes:function($node, model, value){
			$node.find('.daily_prizes').text(value);
		}

	},

	initialize: function(obj) {
		this.super('initialize', obj);

	}
});

W.component.appkit.SignDescription.handleHelp = function(){

	//初始化签到奖励说明
	ensureNS('W.dialog.sign');
	W.dialog.sign.InstructionDialog = W.dialog.Dialog.extend({
		getTemplate: function() {
			$('#sign-chance-dialog-tmpl-src').template('sign-chance-dialog-tmpl');
			return "sign-chance-dialog-tmpl";
		}
	});

};