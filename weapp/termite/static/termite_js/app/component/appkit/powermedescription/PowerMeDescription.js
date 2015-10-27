/**
 * @class W.component.appkit.PowerMeDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.PowerMeDescription = W.component.Component.extend({
	type: 'appkit.powermedescription',
	selectable: 'yes',
	propertyViewTitle: '微助力',

    dynamicComponentTypes: [],

	properties: [{
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
			displayName: '活动时间',
			isUserProperty: true,
			validate: 'data-validate="require-notempty::有效时间不能为空"',
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
			name: 'image',
			type: 'image_dialog_select',
			displayName: '链接图文',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示：建议图片长宽20px*20px，正方形图片',
			default: ""
		},{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '顶部图片',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示:图片格式jpg/png, 图片宽度640px, 高度自定义, 请上传风格与背景配色协调的图片',
			default: ""
		},{
			name: 'share_description',
			type: 'textarea',
			displayName: '分享描述',
			maxLength: 200,
			isUserProperty: true,
			default: '签到赚积分啦！'
		}]}],
	propertyChangeHandlers: {

	},

	initialize: function(obj) {
		this.super('initialize', obj);

	}
});