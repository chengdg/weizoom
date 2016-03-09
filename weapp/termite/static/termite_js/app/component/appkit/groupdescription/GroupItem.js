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
		groupClass: 'xui-propertyView-app-DynamicGroupItems',
		fields: [{
            name: 'group_type',
            type: 'select',
			//validate:'data-validate="require-notempty::选项不能为空',
            displayName: '类型',
			//annotation:'注：1个团购可创建多种拼团人数供顾客选择',
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
			displayName:'团拼时间：',
			annotation:'天',
			size:'35px',
			isUserProperty:true
		},{
			name:'group_price',
			type:'text_with_annotation',
			displayName:'团购价：',
			annotation:'元',
			size:'35px',
			isUserProperty:true
		}]

	}],

	propertyChangeHandlers: {
		group_type:function($node, model, value, $propertyViewNode){
			console.log('DDDDD/////');
			console.log(value);
			// data-dynamic-cid="5"
			var that = this;
			var GroupArray = $propertyViewNode.parent().children('.propertyGroup_property_dynamicControlField_control');
			var cidArray = [];
			for(var i=0;i<GroupArray.length;i++){
				var cid =$(GroupArray[i]).attr('data-dynamic-cid');
				cidArray.push(cid);
			}
			var localCid = that.cid;
			var maxCid = Math.max.apply(this,cidArray);



			if(localCid<maxCid){
				var $cur_target = $node.find('.wui-i-group1');
				$cur_target.find('.group_type').html(''+value+'人团');
			}else{
				var $cur_target = $node.find('.wui-i-group2');
				$cur_target.find('.group_type').html(''+value+'人团');
			}

		}
	}
});
