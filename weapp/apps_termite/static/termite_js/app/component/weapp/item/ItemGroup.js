/**
 * @class W.component.weapp.ItemGroup
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.ItemGroup = W.component.Component.extend({
	type: 'weapp.item_group',
	propertyViewTitle: '商品',

    dynamicComponentTypes: [
        {type: 'weapp.item', model: 3}
    ],

	properties: [
       {
            group: '关联链接',
            fields: [{
                name: 'type',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [{name:'大图', value:'0'},{name:'小图', value:'1'},{name:'一大两小', value:'2'},{name:'列表', value:'3'}],
                default: '2'
            },{
                name: 'itemname',
                type: 'checkbox',
                displayName: '商品名称',
                isUserProperty: true,
                source: [{name:'显示商品名', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'}}
            },{
                name: 'price',
                type: 'checkbox',
                displayName: '价格',
                isUserProperty: true,
                source: [{name:'显示价格', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'},c1:{select:'True'}}
            },{
                name: 'style',
                type: 'radio',
                displayName: '购物车图标',
                isUserProperty: true,
                source: [{name:'无', value:''},{name:'样式一', value:'0'},{name:'样式二', value:'1'},{name:'样式三', value:'2'},{name:'样式四', value:'3'}],
                default:'2'
            },{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        itemname: function($node, model, value){
            if(value.c0.select)
                $node.find('.wa-inner-title').show();
            else
                $node.find('.wa-inner-title').hide();
        },
        price: function($node, model, value){
            if(value.c0)
                if(value.c0.select)
                    $node.find('.wa-inner-price').show();
                else
                    $node.find('.wa-inner-price').hide();

        },
        type: function($node, model, value){
            for(var i=0; i<4; i++)
                $node.find('>ul').removeClass('wui-block-type'+i);
            $node.find('>ul').addClass('wui-block-type'+value);
            W.Broadcaster.trigger('component:resize', this);
        },
        style: function($node, model, value){
            for(var i=0; i<4; i++)
                $node.find('.wa-inner-shopCar').removeClass('wui-shopCar-style'+i);
            $node.find('.wa-inner-shopCar').addClass('wui-shopCar-style'+value);
        },
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
    }
}, {
    indicator: {
        name: '商品',
        imgClass: 'componentList_component_product'
    }
});