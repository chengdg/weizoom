/**
 * @class W.component.jqm.Divider
 * 
 */
W.component.jqm.Divider = W.component.Component.extend({
	type: 'jqm.divider',
	propertyViewTitle: 'Divider',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'size',
                type: 'select',
                displayName: 'Size',
                source: [{name:'1', value:'1'}, {name:'2', value:'2'}, {name:'3', value:'3'}, {name:'4', value:'4'}, {name:'5', value:'5'}],
                default: '3'
            }, {
                name: 'color',
                type: 'select',
                displayName: '颜色',
                source: [{name:'Black', value:'#000'}, {name:'Gray', value:'#ccc'}, {name:'White', value:'#fff'}],
                default: 'gray'
            }]
        }
    ],

    propertyChangeHandlers: {
        size: function($node, model, value) {
            $node.find('hr').css('height', value+'px');

            W.Broadcaster.trigger('component:resize', this);
        },
        color: function($node, model, value) {
            $node.find('hr').css('background-color', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Divider',
        imgClass: 'componentList_component_hr'
    }
});
