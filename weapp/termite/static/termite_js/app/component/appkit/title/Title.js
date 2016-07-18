/**
 * @class W.component.appkit.Title
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.Title = W.component.Component.extend({
	type: 'appkit.title',
	propertyViewTitle: '标题',

	properties: [
        {
            group: '属性1',
            groupClass:'xui-propertyView-title',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: '标题名',
                maxLength: 30,
                validate: 'data-validate="require-notempty::标题名不能为空"',
                validateIgnoreDefaultValue: true,
                isUserProperty: true,
                placeholder:'编辑[标题]',
                default: '编辑[标题]'
            },{
                name: 'subtitle',
                type: 'text',
                displayName: '副标题',
                maxLength: 30,
                isUserProperty: true,
                default: ''
            },{
                name: 'time',
                type: 'time',
                isUserProperty: true,
                default: ''
            },{
                name: 'align',
                type: 'radio',
                displayName: '显示',
                isUserProperty: true,
                source: [{name:'居左', value:'left'},{name:'居中', value:'center'},{name:'居右', value:'right'}],
                default: 'left'
            },{
                name: 'background_color',
                type: 'color_picker',
                displayName: '背景颜色',
                isUserProperty: true,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
    	title: function($node, model, value) {
            value = this.getDisplayValue(value, 'title');
            //$node.find('.wa-inner-title').text(value);
            this.refresh($node, {resize:true});
        },
        subtitle: function($node, model, value){
            this.refresh($node, {resize: true});
        },
        align: function($node, model, value){
            //$node.css('text-align',value);
            this.refresh($node);
        },
        background_color: function($node, model, value, $propertyViewNode){
        	$node.css('background-color', value);
        },
        time:function($node, model, value){
            this.refresh($node, {resize: true});
        }
    }
}, {
    indicator: {
        name: '标题',
        imgClass: 'componentList_component_title'
    }
});
