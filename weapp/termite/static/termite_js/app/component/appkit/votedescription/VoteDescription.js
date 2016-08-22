/**
 * @class W.component.appkit.CommonDescription
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.VoteDescription = W.component.Component.extend({
	type: 'appkit.votedescription',
	selectable: 'yes',
	propertyViewTitle: '投票简介',

	properties: [{
		group: '文本项',
		groupClass: 'xui-propertyView-app-TextSurvey',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '活动名称',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::活动名称不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '活动名称'
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
			name: 'image',
			type: 'image_dialog_select',
			displayName: '分享图片',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '注:不上传则使用默认图片,建议尺寸90*90，仅支持jpg/png',
			default: "/static_v2/img/thumbnails_vote.png"
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
		image: function($node, model, value, $propertyViewNode) {
			console.log(value);
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
