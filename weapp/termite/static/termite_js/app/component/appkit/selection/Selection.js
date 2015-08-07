/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.Selection = W.component.Component.extend({
	type: 'appkit.selection',
	selectable: 'yes',
	propertyViewTitle: '',

	dynamicComponentTypes: [{
        type: 'appkit.selectitem',
        model: 3
    }],

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-Selection',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::标题不能为空"',
			validateIgnoreDefaultValue: true,
			default: '标题名称',
			placeholder: '标题名称'
		}, {
			name: 'type',
			type: 'radio',
			displayName: '单选/多选',
			isUserProperty: true,
			source: [{
				name: '单选',
				value: 'single'
			}, {
				name: '多选',
				value: 'multi'
			}],
			default: 'single'
		}, {
			name: 'is_mandatory',
			type: 'radio',
			displayName: '是否必填',
			isUserProperty: true,
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
            isShowCloseButton: true,
            minItemLength: 0,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		type: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		is_mandatory: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
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
	}
}, {
	indicator: {
		name: '文本调研',
		imgClass: 'componentList_component_product_list' // 控件icon
	}
});
