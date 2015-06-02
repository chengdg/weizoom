/**
 * @class W.component.weapp.Search
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.Search = W.component.Component.extend({
	type: 'weapp.search',
	propertyViewTitle: '商品搜索'
}, {
    indicator: {
        name: '商品搜索',
        imgClass: 'componentList_component_heading'
    }
});
