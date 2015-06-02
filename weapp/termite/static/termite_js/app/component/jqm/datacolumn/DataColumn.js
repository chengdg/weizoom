/**
 * @class W.component.jqm.DataColumn
 * 
 */
W.component.jqm.DataColumn = W.component.Component.extend({
	type: 'jqm.datacolumn',
    propertyViewTitle: '数据列',
    forceDisplayInPropertyView: 'yes',

    dynamicComponentTypes: [
        {type: 'jqm.datacolumn_data', model: {index: 1, text: '数据1', price: '1.0', original_price: '2.0'}},
        {type: 'jqm.datacolumn_data', model: {index: 2, text: '数据2', price: '1.0', original_price: '2.0'}},
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '标题',
                default: ''
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
