/**
 * @class W.component.weapp.Line
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.Line = W.component.Component.extend({
	type: 'weapp.line',
	propertyViewTitle: '辅助线'
}, {
    indicator: {
        name: '辅助线',
        imgClass: 'componentList_component_subline'
    }
});
