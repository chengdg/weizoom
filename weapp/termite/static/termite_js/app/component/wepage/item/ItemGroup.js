/**
 * @class W.component.wepage.ItemGroup
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ItemGroup = W.component.Component.extend({
    type: 'wepage.item_group',
    propertyViewTitle: '商品',
    shouldIgnoreSubComponent: true,
    needServerRender: true,
    needServerProcessComponentData: true,

    dynamicComponentTypes: [{
        type: 'wepage.item',
        model: 3,
        createStrategy: {
            type: 'dialog',
            dialog: 'W.dialog.termite.SelectWebSiteDataDialog',
            dialogParameter: '{"title":[{"name":"已上架商品", "type":"product"}], "navData":{"product":{"dataName":"商品", "dataLink": "/mall2/product/"}}}'
        },
    }],

    properties: [{
        group: '',
        groupClass: 'xui-propertyView-productGroup',
        fields: [{
            name: 'items',
            displayName: '选择商品',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 0,
            isUserProperty: true,
            default: []
        }, {
            name: 'type',
            type: 'radio',
            isUserProperty: false,
            source: [{
                name: '大图',
                value: '0'
            }, {
                name: '小图',
                value: '1'
            }, {
                name: '一大两小',
                value: '2'
            }, {
                name: '列表',
                value: '3'
            }],
            default: '0'
        }, {
            name: 'card_type',
            type: 'radio',
            isUserProperty: false,
            source: [{
                name: '默认样式',
                value: '0'
            }, {
                name: '简洁样式',
                value: '1'
            }],
            default: '0'
        }, {
            name: 'itemname',
            type: 'checkbox',
            displayName: '显示商品名',
            isUserProperty: false,
            default: true
        }, {
            name: 'price',
            type: 'hidden',
            displayName: '显示价格',
            isUserProperty: false,
            default: true
        }, {
            name: 'container',
            type: 'product_style_container',
            isUserProperty: true
        }]
    }],

    propertyChangeHandlers: {
        itemname: function($node, model, value) {
            if (value || model.get('type') == 3) {
                $node.find('.wa-inner-title').show();
                $node.addClass('wui-productTitle');
            } else {
                $node.find('.wa-inner-title').hide();
                $node.removeClass('wui-productTitle');
            }
            
            if (model.get('price') && model.get('card_type') != '1') {
                $node.find('.wa-inner-price').addClass('xui-border');
            }else{
                $node.find('.wa-inner-price').removeClass('xui-border');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        price: function($node, model, value) {
            xlog("in price()");
            if (value || model.get('type') == 3) {
                $node.find('.wa-inner-price').show();
            } else {
                $node.find('.wa-inner-price').hide();
            }

            if (model.get('price') && model.get('card_type') != '1') {
                $node.find('.wa-inner-price').addClass('xui-border');
            }else{
                $node.find('.wa-inner-price').removeClass('xui-border');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        type: function($node, model, value, $propertyViewNode) {
            this.handleTypeChange($node, model);
            
            for (var i = 0; i < 4; i++)
                $node.find('>ul').removeClass('wui-block-type' + i);
            $node.find('>ul').addClass('wui-block-type' + value);

            W.Broadcaster.trigger('component:resize', this);
        },

        card_type: function($node, model, value, $propertyViewNode) {
            this.handleTypeChange($node, model);

            for (var i = 0; i < 2; i++)
                $node.find('>ul').removeClass('wui-card-type-' + i);
            $node.find('>ul').addClass('wui-card-type-' + value);


            W.Broadcaster.trigger('component:resize', this);
        },
        style: function($node, model, value) {
            for (var i = 0; i < 4; i++)
                $node.find('.wa-inner-shopCar').removeClass('wui-shopCar-style' + i);
            $node.find('.wa-inner-shopCar').addClass('wui-shopCar-style' + value);
        },
        items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {
                    silent: true
                });
            });

            _.delay(_.bind(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this), 100);
            //this.refresh($node, {resize:true, refreshPropertyView:true});
        }
    },

    onBeforeTriggerSelectComponent: function($node) {
        for (var i = 0; i < this.components.length; ++i) {
            var component = this.components[i];
            var $component = $node.find('[data-component-cid="' + component.cid + '"]');
            var img = $component.find('img').attr('src');
            component.runtimeData = {
                img: img,
                isInvalid: $component.length === 0
            }
        }
    },

    handleTypeChange: function($node, model){
        var type = model.get('type');
        var card_type = model.get('card_type');
        if( type == 1 && card_type == 1 ){
            $propertyViewNode.find('.xa-nameBlock').show();
            $propertyViewNode.find('.xa-styleType').css('padding-bottom','16px');
            $propertyViewNode.find('.xa-itemname').hide();
            $propertyViewNode.find('.xa-price').show();
        }else if( type == 2 && card_type == 1 ){
            $propertyViewNode.find('.xa-nameBlock').show();
            $propertyViewNode.find('.xa-styleType').css('padding-bottom','16px');
            $propertyViewNode.find('.xa-itemname').hide();
            $propertyViewNode.find('.xa-price').show();
        }else if(type == 3){
            $propertyViewNode.find('.xa-nameBlock').hide();
        }else{
            $propertyViewNode.find('.xa-nameBlock').show();
            $propertyViewNode.find('.xa-styleType').css('padding-bottom','16px');
            $propertyViewNode.find('.xa-itemname').show();
            $propertyViewNode.find('.xa-price').show();
        }

        this.propertyChangeHandlers['itemname']($node, model, model.get('itemname'));
        this.propertyChangeHandlers['price']($node, model, model.get('price'));

    }

}, {
    indicator: {
        name: '商品',
        imgClass: 'componentList_component_product'
    }
});
