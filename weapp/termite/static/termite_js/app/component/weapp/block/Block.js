/**
 * @class W.component.weapp.Block
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.Block = W.component.Component.extend({
	type: 'weapp.block',
	propertyViewTitle: '辅助空白',
	properties: [{
            group: '属性1',
            fields: [{
                name: 'height',
                type: 'text',
                displayName: '空白高度',
                isUserProperty: true,
                default: '20'
            }]
        }],
     propertyChangeHandlers: {
    	height: function($node,model,value){
    		if(!isNaN(value)){
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
