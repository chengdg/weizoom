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
		groupClass: 'xui-propertyView-app-DynamicGroupItems ',
		fields: [{
            name: 'group_type',
            type: 'select',
            displayName: '类型',
			source:[{
				name:'2人团',
				value:'2'
			},{
				name:'3人团',
				value:'3'
			}],
            default:'2',
			isUserProperty:true

        },{
			name:'group_days',
			type:'text_with_annotation',
			displayName:'团拼时间：',
			annotation:'天',
			size:'35px',
			// validate:'data-validate="require-notempty::选项不能为空',
			isUserProperty:true
		},{
			name:'group_price',
			type:'text_with_annotation',
			displayName:'团购价：',
			annotation:'元',
			size:'35px',
			// validate:'data-validate="require-notempty::选项不能为空',
			isUserProperty:true
		}]

	}],

	propertyChangeHandlers: {
		group_type:function($node, model, value, $propertyViewNode){
			var that = this;
			var GroupArray = $propertyViewNode.parent().children('.propertyGroup_property_dynamicControlField_control');
			var cidArray = [];
			for(var i=0;i<GroupArray.length;i++){
				var cid =$(GroupArray[i]).attr('data-dynamic-cid');
				cidArray.push(cid);
			}
			var localCid = that.cid;
			var maxCid = Math.max.apply(this,cidArray);

			console.log('localCid:'+localCid);
			console.log('cidArray:'+cidArray);
			console.log('maxCid:'+maxCid);
			if(cidArray.length==1){
				var $cur_target = $node.find('.wui-i-group1');
				$cur_target.find('.group_type').html(''+value+'人团');
			}else{
				if(localCid<maxCid){
					var $cur_target = $node.find('.wui-i-group1');
					$cur_target.find('.group_type').html(''+value+'人团');
				}else{
					var $cur_target = $node.find('.wui-i-group2');
					$cur_target.find('.group_type').html(''+value+'人团');
				}
			}

			validate_group($node, model, value, $propertyViewNode);
		},
		group_days:function($node, model, value, $propertyViewNode){
			var that = this;
			var GroupArray = $propertyViewNode.parent().children('.propertyGroup_property_dynamicControlField_control');
			var cidArray = [];
			for(var i=0;i<GroupArray.length;i++){
				var cid =$(GroupArray[i]).attr('data-dynamic-cid');
				cidArray.push(cid);
			}
			var localCid = that.cid;
			var maxCid = Math.max.apply(this,cidArray);

			console.log('localCid:'+localCid);
			console.log('cidArray:'+cidArray);
			console.log('maxCid:'+maxCid);
			if(cidArray.length==1){
				var $cur_target = $node.find('.wui-i-group1');
				$cur_target.find('.group_days').html('拼团时间'+value+'天');
			}else{
				if(localCid<maxCid){
					var $cur_target = $node.find('.wui-i-group1');
					$cur_target.find('.group_days').html('拼团时间'+value+'天');
				}else{
					var $cur_target = $node.find('.wui-i-group2');
					$cur_target.find('.group_days').html('拼团时间'+value+'天');
				}
			}
			validate_group($node, model, value, $propertyViewNode);
		},
		group_price:function($node, model, value, $propertyViewNode){
			var that = this;
			var GroupArray = $propertyViewNode.parent().children('.propertyGroup_property_dynamicControlField_control');
			var cidArray = [];
			for(var i=0;i<GroupArray.length;i++){
				var cid =$(GroupArray[i]).attr('data-dynamic-cid');
				cidArray.push(cid);
			}
			var localCid = that.cid;
			var maxCid = Math.max.apply(this,cidArray);

			console.log('localCid:'+localCid);
			console.log('cidArray:'+cidArray);
			console.log('maxCid:'+maxCid);
			if(cidArray.length==1){
				var $cur_target = $node.find('.wui-i-group1');
				$cur_target.find('.group_price').html('团购价：'+value+'元');
			}else{
				if(localCid<maxCid){
					var $cur_target = $node.find('.wui-i-group1');
					$cur_target.find('.group_price').html('团购价：'+value+'元');
				}else{
					var $cur_target = $node.find('.wui-i-group2');
					$cur_target.find('.group_price').html('团购价：'+value+'元');
				}
			}

			validate_group($node, model, value, $propertyViewNode);
		}


	}
});
