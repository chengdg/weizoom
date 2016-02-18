/**
 * @class W.component.appkit.TextList
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.TextList = W.component.Component.extend({
	type: 'appkit.textlist',
	selectable: 'yes',
	propertyViewTitle: '',

	dynamicComponentTypes: [{
        type: 'appkit.textitem',
        model: 0
    }],

	properties: [{
		group: '快捷模块',
		groupClass: 'xui-propertyView-app-TextList',
		fields: [{
			name: 'title',
			type: 'title_with_annotation',
			displayName: '报名填写项',
			isUserProperty: true,
			annotation: "(此处勾选默认显示为必填,如需显示为不必填请手动添加)"
		}, {
			name: 'modules',
			type: 'checkbox-group',
			displayName: '默认',
			isUserProperty: true,
			source: [{
				name: '姓名',
				value: 'name',
				columnName: 'name'
			}, {
				name: '手机',
				value: 'phone',
				columnName: 'phone'
			}, {
				name: '邮箱',
				value: 'email',
				columnName: 'email'
			}, {
				name: 'QQ',
				value: 'qq',
				columnName: 'qq'
			}, {
				name: '职位',
				value: 'job',
				columnName: 'job'
			}, {
				name: '住址',
				value: 'addr',
				columnName: 'addr'
			}],
			default: {name:{select:true}, phone:{select:true}, email:{select:true}, qq:{select:false}, job:{select:false}, addr:{select:false}}
		}, {
            name: 'items',
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 0,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		items: function($node, model, value) {
			console.log('======================');
			console.log($node);
			console.log(model);
			console.log(value);
			console.log('======================');
            this.refresh($node, {resize:true, refreshPropertyView:true});
        },
		modules: function($node, model, value){
			this.refresh($node, {resize:true});
		}
	}
}, {
	indicator: {
		name: '快捷模块',
		imgClass: 'componentList_component_memberinfo' // 控件icon
	}
});
