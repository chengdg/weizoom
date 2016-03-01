/**
 * @class W.component.appkit.GroupItem
 * 签到动态组件
 */
ensureNS('W.component.appkit');
W.component.appkit.GroupItem = W.component.Component.extend({
	type: 'appkit.groupitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		groupClass: 'xa-serial-points-settings',
		fields: [{
            name: 'group_type',
            className:'xui-app-Group-i-type',
            type: 'selector_v1',
            displayName: '2.',
            isUserProperty: true,
            source:[{
                name:'5人团',
                value:'5'
            },{
                name:'10人团',
                value:'10'
            }],
			//validate: 'data-validate="require-notempty::选项不能为空',
            default: '5'
        },{
            name: 'group_days',
            className:'xui-app-Group-i-days',
            type: 'text_with_annotation',
            displayName: '拼团时间',
            isUserProperty: true,
            maxLength: 5,
            size: '70px',
            annotation: '天',
            //validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
            //validateIgnoreDefaultValue: true,
            default: ''
        },{
            name: 'group_price',
            className:'xui-app-Group-i-price',
            type: 'text_with_annotation',
            displayName: '团购价',
            isUserProperty: true,
            maxLength: 5,
            size: '70px',
            annotation: '元',
            //validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
            //validateIgnoreDefaultValue: true,
            default: ''
        }]
	}],

	propertyChangeHandlers: {
		serial_count_points: function($node, model, value, $propertyViewNode){
			console.log(value);
			if(value == ''){
				model.set('serial_count_points', 0);
				$propertyViewNode.find('input[data-field="serial_count_points"]').val('0');
			}
		}
	}
});
