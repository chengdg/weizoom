/**
 * @class W.component.jqm.Heading
 * 
 */
W.component.jqm.Heading = W.component.Component.extend({
	type: 'jqm.heading',
	propertyViewTitle: 'Heading',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文字',
                default: 'Heading'
            }, {
                name: 'size',
                type: 'select',
                displayName: '尺寸',
                source: [{name:'1', value:'1'}, {name:'2', value:'2'}, {name:'3', value:'3'}, {name:'4', value:'4'}, {name:'5', value:'5'}],
                default: '2'
            }]
        }
    ],

    /* propertyChangeHandlers中的函数将在iframe中被调用 */
    propertyChangeHandlers: {
        text: function($node, model, value) {
            xlog('[heading]: change text property to :' + value);
            $node.text(value);
        },
        size: function($node, model, value) {
            xlog('[heading]: change size property to :' + value);
            var cid = $node.attr('data-cid');
            var $newNode = $(W.render('<h${size} data-cid="${cid}" data-ui-behavior="xub-selectable">${text}</h${size}>', {
                size: value,
                cid: cid,
                text: $node.text()
            }));
            $node.hide();
            $newNode.insertAfter($node);
            $node.remove();
            W.Broadcaster.trigger('mobilewidget:select', cid);
        }
    },

    datasource: [
        {name: 'text'}
    ],

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Heading',
        imgClass: 'componentList_component_heading'
    }
});
