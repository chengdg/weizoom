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
		groupClass: 'xui-propertyView-app-GroupList',
		fields: [{
            name: 'group_type',
            type: 'select',
			//validate:'data-validate="require-notempty::选项不能为空',
            displayName: '类型',
			//annotation:'1个团购可创建多种拼团人数供顾客选择',
			source:[{
				name:'5人团',
				value:'5'
			},{
				name:'10人团',
				value:'10'
			}],
            default:'5',
			isUserProperty:true

        },{
			name:'group_days',
			type:'text_with_annotation',
			displayName:'团拼时间',
			annotation:'天',
			size:'70px',
			isUserProperty:true
		},{
			name:'group_price',
			type:'text_with_annotation',
			displayName:'团购价',
			annotation:'元',
			size:'70px',
			isUserProperty:true
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
