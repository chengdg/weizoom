/**
 * @class W.component.appkit.ComponentAdder
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ComponentAdder = W.component.Component.extend({
	type: 'appkit.componentadder',
	propertyViewTitle: '添加模块',
    shouldShowPropertyViewTitle: true,

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'components',
                type: 'component_list',
                displayName: '组件列表',
                components: W.component.COMPONENTS,
                isUserProperty: true,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {

    }
});
