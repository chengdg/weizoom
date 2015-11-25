/**
 * @class W.component.wepage.ItemList
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ItemList = W.component.Component.extend({
	type: 'wepage.item_list',
	propertyViewTitle: '商品列表',
    needServerRender: true,
    needServerProcessComponentData: true,

	properties: [
       {
            group: '关联链接',
            groupClass: 'xui-propertyView-productList',
            fields: [{
                name: 'category',
                type: 'dialog_select',
                displayName: '商品来源',
                isUserProperty: true,
                triggerButton: '从商品分类中选择',
                selectedButton: '修改',
                dialog: 'W.dialog.termite.SelectCategoriesDialog',
                dialogParameter: '{"enableMultiSelection":false, "title":[{"name":"商品分组", "type":"category"}], "navData":{"category":{"dataName":"商品分组", "dataLink": "/mall2/category_list/"}}}'
            },{
                name: 'type',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: false,
                source: [{name:'大图', value:'0'},{name:'小图', value:'1'},{name:'一大两小', value:'2'},{name:'列表', value:'3'}],
                default: '2'
            },{
                name: 'itemname',
                type: 'checkbox',
                displayName: '显示商品名',
                isUserProperty: false,
                source: [{name:'显示商品名', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'}}
            },{
                name: 'price',
                type: 'checkbox',
                displayName: '显示价格',
                isUserProperty: false,
                source: [{name:'显示价格', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'},c1:{select:'True'}}
            },{
                name: 'count',
                type: 'radio',
                displayName: '显示个数',
                isUserProperty: true,
                source: [{name:'6', value:'6'},{name:'9', value:'9'},{name:'12', value:'12'},{name:'全部', value:'-1'}],
                default: '6'
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
                name: 'container',
                type: 'product_style_container',
                isUserProperty: true
            }]
        }
    ],

    propertyChangeHandlers: {
        itemname: function($node, model, value){
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
        count:function($node, model, value, $propertyViewNode){
            this.handleTypeChange($node, model);

            _.delay(_.bind(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this), 100);

        },
        price: function($node, model, value){
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
        type: function($node, model, value){
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
        style: function($node, model, value){
            for(var i=0; i<4; i++)
                $node.find('.wa-inner-shopCar').removeClass('wui-shopCar-style'+i);
            $node.find('.wa-inner-shopCar').addClass('wui-shopCar-style'+value);
        },
        category: function($node, module, value, $propertyViewNode) {
            var data = $.parseJSON(value)[0];
            var categoryId = data['id'];
            var _this = this;

            W.getLoadingView().show();
            api = 'products_by_category_id/get';
            W.getApi().call({
                app: 'webapp',
                api: api,
                args: {
                    id: categoryId,
                    count: module.get('count')
                },
                success: function(apidata) {                    
                    _.delay(_.bind(function() {
                        W.Broadcaster.trigger('component:finish_create', null, _this);
                    }, this), 100);

                    $propertyViewNode.find('.xa-categoryName').text(data['title']).css('display','inline-block');
                    $propertyViewNode.find('button').text('修改');
                    W.getLoadingView().hide();   

                    // 加入 dailog默认选中 某一条数据
                    var dialogParameter = '{"selectedId": '+categoryId+', "enableMultiSelection":false, "title":[{"name":"商品分组", "type":"category"}], "navData":{"category":{"dataName":"商品分组", "dataLink": "/mall2/category_list/"}}}';
                    $propertyViewNode.find('button').attr('data-dialog-parameter', dialogParameter);
                },
                error: function(resp) {
                    W.getLoadingView().hide();
                    W.getErrorHintView().show('加载分类数据失败!');
                }
            })
        }
    },

    updateModel: function(modelData) {
        var targetData = {
            meta: {
                id: modelData.id
            },
            data: modelData.link
        }
        this.model.set('category', JSON.stringify(targetData));
    },

    onBeforeTriggerSelectComponent: function($node) {
        for (var i = 0; i < this.components.length; ++i) {
            var component = this.components[i];
            var $component = $node.find('[data-cid="' + component.cid + '"]');
            var img = $component.find('img').attr('src');
            component.runtimeData = {
                img: img
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
    },

}, {
    indicator: {
        name: '商品列表',
        imgClass: 'componentList_component_product_list'
    }
});