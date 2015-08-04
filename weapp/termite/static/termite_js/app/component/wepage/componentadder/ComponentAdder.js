/**
 * @class W.component.wepage.ComponentAdder
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ComponentAdder = W.component.Component.extend({
    type: 'wepage.componentadder',
    propertyViewTitle: '添加模块',
    shouldShowPropertyViewTitle: true,

    properties: [{
        group: 'Model属性',
        fields: [{
            name: 'components',
            type: 'component_list',
            displayName: '组件列表',
            components: W.component.COMPONENTS,
            isUserProperty: true,
            default: ''
        }]
    }],

    propertyChangeHandlers: {

    }
});
