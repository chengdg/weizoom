/**
 * @class W.component.Page
 * 页面
 */
W.data.getPageFields = function() {
    return [
        {name: '选择字段...', value: ''}
    ];
}

W.data.getPageType = function() {
    return [
        {name: '顶级页面', value: 'top_level_page'},
        {name: '编辑页面', value: 'edit_page'},
        {name: '对话框页面', value: 'dialog_page'},
        {name: '自由页面', value: 'free_page'}
    ];
}

/**
 * W.data.getPageFieldsForOrder: 获得page中用于进行拖动排序的field集合
 */
W.data.getPageFieldsForOrder = function(page) {
    var id2columnInfo = {}
    _.each(page.components, function(subComponent) {
        id2columnInfo[subComponent.cid] = {
            type: subComponent.type,
            id: subComponent.cid, 
            name: subComponent.model.get('name'),
            label: subComponent.model.get('label'), 
            index: 999,
            is_checked: false
        };
    });

    //构建已排序的元素
    var existedColumnInfos = $.parseJSON(page.model.get('columns'));
    _.each(existedColumnInfos, function(existedColumnInfo) {
        var id = existedColumnInfo.id;
        columnInfo = id2columnInfo[id];
        if (columnInfo) {
            columnInfo.index = existedColumnInfo.index;
            columnInfo.is_checked = existedColumnInfo.is_checked;
            columnInfo.width = existedColumnInfo.width;
        } else if (id < 0) {
            //id<0, 意味着是系统级的column
            id2columnInfo[id] = existedColumnInfo;
        }
    });

    var orderedColumnInfos = _.sortBy(_.values(id2columnInfo), function(columnInfo) {
        return columnInfo.index;
    });

    return {
        page: page,
        orderedColumnInfos: orderedColumnInfos
    };
}

W.component.viper.Page = W.component.Component.extend({
	type: 'viper.page',
	propertyViewTitle: 'Page',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: '页面名',
                validate: 'required-none',
                default: '页面'
            }, {
                name: 'storeEngine',
                type: 'radio',
                displayName: '存储引擎',
                source: [{name:'MongoDB', value:'mongo'}, {name:'MySQL', value:'mysql'}],
                default: 'mongo'
            }, {
                name: 'className',
                type: 'text',
                displayName: 'Model类',
                placeholder: 'Django Model的类名',
                default: '',
            }/*, {
                name: 'tableName',
                type: 'text',
                displayName: '表名',
                placeholder: 'Django Model的表名',
                default: ''
            }*/, {
                name: 'module',
                type: 'text',
                displayName: 'Module',
                validate: 'required-none',
                placeholder: '所属App Module',
                default: ''
            }, {
                name: 'navName',
                type: 'text',
                displayName: '导航名',
                validate: 'required-none',
                placeholder: '显示名',
                default: ''
            }, {
                name: 'type',
                type: 'select',
                displayName: '类型',
                source: W.data.getPageType,
                default: 'top_level_page'
            }, {
                name: 'entityName',
                type: 'text',
                displayName: '实体名',
                default: ''
            }, {
                name: 'is_horizontal',
                type: 'boolean',
                displayName: '水平控件?',
                default: 'yes'
            }]
        }, {
            group: '事件',
            fields: [{
                name: 'event:onload',
                type: 'dialog_select',
                displayName: 'Click',
                triggerButton: '编辑代码...',
                dialog: 'W.workbench.EditCodeDialog',
                default: ''
            }]
        }/*, {
            group: 'WebApp属性',
            groupName: 'list_page_property',
            fields: [{
                name: 'isEnableSearch',
                type: 'boolean',
                displayName: '可搜索?',
                default: "yes"
            }, {
                name: 'searchField',
                type: 'select',
                displayName: '搜索字段',
                source: W.data.getPageFields,
                default: ''
            }]
        }*/
    ],

    propertyChangeHandlers: {
        is_horizontal: function($node, model, value) {
            if ('yes' === value) {
                $node.find('form').addClass('form-horizontal');
            } else {
                $node.find('form.form-horizontal').removeClass('form-horizontal');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        type: function($node, model, value, $propertyViewNode) {
            W.Broadcaster.trigger('designpage:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});