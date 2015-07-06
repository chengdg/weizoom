/**
 * @class W.component.wepage.Block
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.Block = W.component.Component.extend({
    type: 'wepage.block',
    propertyViewTitle: '辅助空白',
    properties: [{
        group: '属性1',
        fields: [{
            name: 'height',
            type: 'slider',
            displayName: '空白高度',
            isUserProperty: true,
            default: '20'
        }]
    }],
    propertyChangeHandlers: {
        height: function($node, model, value) {
            //xlog('123213')
            if (!isNaN(value)) {
                $node.find('.wa-inner-block').height(value);
                W.Broadcaster.trigger('component:resize', this)
            }
        }
    }
}, {
    indicator: {
        name: '辅助空白',
        imgClass: 'componentList_component_black'
    }
});
