/**
 * @class W.component.jqm.RadioButtonGroup
 * 
 */
W.component.viper.RadioButtonGroup = W.component.Component.extend({
	type: 'viper.radio_button_group',
	propertyViewTitle: 'Radio Button Group',

    dynamicComponentTypes: [
        {type: 'viper.radio_button', model: {text: '选项', value: 'radio'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: '单选框'
            }, {
                name: 'orientation',
                type: 'select',
                displayName: '排列',
                source: W.data.RadioButtonOrientations,
                default: 'vertical'
            }, {
                name: 'datasource_page',
                type: 'select',
                displayName: '数据Page',
                source: W.data.getWorkbenchPages,
                default: '#'
            }, {
                name: 'datasource_field',
                type: 'select',
                displayName: '数据Field',
                source: function(component) {
                    var pageCid = component.model.get('datasource_page').split('-')[1];
                    if (pageCid) {
                        var fields = W.data.getWorkbenchPageFields(pageCid);
                        return fields;
                    } else {
                        return []
                    }
                },
                default: '#'
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                default: []
            }]
        }, {
            group: '事件',
            fields: [{
                name: 'event:onclick',
                type: 'dialog_select',
                displayName: 'Click',
                triggerButton: '编辑代码...',
                dialog: 'W.workbench.EditCodeDialog',
                default: ''
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
        },
        label: function($node, model, value) {
            $node.find('label.control-label').text(value+':');
        },
        orientation: function($node, model, value) {
            if (value === 'vertical') {
                $node.find('label.radio').removeClass('inline');
            } else {
                $node.find('label.radio').addClass('inline');
            }
            
            W.Broadcaster.trigger('component:resize', this);
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Radio Buttons',
        imgClass: 'componentList_component_radio'
    }
});