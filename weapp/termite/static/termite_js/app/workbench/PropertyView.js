/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 右侧的property视图
 * @class
 */
W.workbench.PropertyView = Backbone.View.extend({
	el: '',

	events: {
        'input .propertyGroup_property_input > input': 'onChangeInputContent',
        'input .propertyGroup_property_input > textarea': 'onChangeInputContent',
        'change .propertyGroup_property_input > select': 'onChangeSelection',
        'change .propertyGroup_property_input > input[type="radio"]': 'onChangeSelection',
        'change .propertyGroup_property_input > label > input[type="radio"]': 'onChangeSelection',
        'change .propertyGroup_property_textCheckboxField input[type="checkbox"]': 'onChangeTextCheckboxSelection',
        'click .btn-group > .btn': 'onClickRadioGroupButton',
        'click .propertyGroup_property_dynamicControlField_buttons > .btn': 'onClickAddDynamicComponentButton',
        'click .propertyGroup_property_dynamicControlField_title': 'onClickDynamicComponentTitle',
        'click .propertyGroup_property_dynamicControlField_title .icon-remove': 'onClickRemoveDynamicComponentButton',
        'click .propertyGroup_property_dialogSelectField .btn': 'onClickOpenDialogButton',
        'click .propertyGroup_property_htmlEditorField .btn': 'onClickSaveHtmlEditorContentButton',
        'keypress .propertyGroup_property_htmlEditorField pre': 'onHtmlEditorKeypress',

        'click [data-action="editProperty"]': 'onClickEditPropertyButton',
        'click [data-action="editDatasource"]': 'onClickEditDatasourceButton',
        'click select.datasourceEditor_pageSelector': 'onChangeDatasourcePageSelection',
        'click #datasourceEditor_submitBtn': 'onClickSubmitDatasourceEditorButton',
	},

    getTemplate: function() {
        $('#property-view-tmpl-src').template('property-view-tmpl');
        return "property-view-tmpl";
    },

    getDatasourceFieldsTemplate: function() {
        $('#datasource-editor-fields-selector-tmpl-src').template('datasource-editor-fields-selector-tmpl');
        return "datasource-editor-fields-selector-tmpl";
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.template = this.getTemplate();
        this.component = null;
        this.onlyShowUserProperty = options.onlyShowUserProperty || false;

        //design page中切换component的响应函数
        W.util.changeComponentInDesignPageHandlers.push(function() {
            if (!W.validate(this.$el)) {
                W.getErrorHintView().show('请完成必填的property信息!');
                return false;
            }
            return true;
        });

        W.Broadcaster.on('component:select', _.bind(this.onUpdatePropertyEditor, this));
        W.Broadcaster.on('mobilepage:delete-widget', _.bind(this.onDeleteMobilePageWidget, this));
	},

    render: function() {
        /*
        this.$el.append($.tmpl(this.template, {}));
        */
    },

    /**
     * getTargetComponent: 获得要发送event的component
     */
    getTargetComponent: function($node) {
        var $parents = $node.parents('.propertyGroup_property_dynamicControlField_control');
        if ($parents.length > 0) {
            var cid = $parents.eq(0).attr('data-dynamic-cid');
            return W.component.CID2COMPONENT[cid];
        } else {
            return this.component;
        }
    },

    /**
     * updateDynamicComponents: 更新dynamic component信息
     */
    updateDynamicComponents: function($item) {
        var orderedCids = [];
        this.$(".propertyGroup_property_dynamicControlField_control").each(function() {
            orderedCids.push(parseInt($(this).attr('data-dynamic-cid')));
        });
        xlog('[property view]: update ' + this.component.cid + "'s dynamic components to [" + orderedCids + "]");

        var $dynamicControl = null;
        if ($item) {
            $dynamicControl = $item.parents(".propertyGroup_property_dynamicControlField");
        } else {
            $dynamicControl = this.$(".propertyGroup_property_dynamicControlField");
        }
        
        var attr = $dynamicControl.attr('data-field');
        this.component.model.set(attr, orderedCids);
    },

    /**
     * enableSortDynamicComponent: 开启dynamic component的拖动排序功能
     */
    enableSortDynamicComponent: function() {
        var _this = this;
        this.$(".propertyGroup_property_dynamicControlField").sortable({
            axis: 'y',
            opacity: '0.4',
            cursor: 'move',
            handle: '.propertyGroup_property_dynamicControlField_title',
            start: function() {
                xlog('[property view]: start sort...');
            },
            stop: function(event, ui) {
                _this.updateDynamicComponents(ui.item);
            }
        });
    },

    /*********************************************************
     * onSwitchPage: 切换页面时，清空属性编辑器
     *********************************************************/    
    onSwitchPage: function(component) {
        this.$el.empty();
    },    

    /**
     * onDeleteMobilePageWidget: mobilepage:delete_widget事件的响应函数
     */
    onDeleteMobilePageWidget: function() {
        this.$el.empty();
    },

    /*********************************************************
     * onUpdatePropertyEditor: 更新属性编辑器
     *********************************************************/    
    onUpdatePropertyEditor: function(component) {
        xlog("[property view]: update property editor");
        this.component = component;
        var dynamicComponents = _.sortBy(_.filter(component.components, function(component) {
            xlog(component);
            if (component.selectable === 'no') {
                return true;
            }

            if (component.forceDisplayInPropertyView == 'yes') {
                return true;
            }

            return false;
        }), function(component) {
            return component.model.get('index');
        });
        _.each(component.dynamicComponentTypes, function(componentType) {
            xlog(W.component.getPropertyViewTitleByType(componentType.type));
        });

        //确定group的isUserProperty
        _.each(component.properties, function(property_group) {
            property_group.isUserProperty = false;
            var fieldCount = property_group.fields.length;
            for (var i = 0; i < fieldCount; ++i) {
                var field = property_group.fields[i];
                if (field.isUserProperty) {
                    property_group.isUserProperty = true;
                    break;
                }
            }
        });

        //合并component.dynamicComponentTypes中相同类型的sub component，支持添加按钮的显示
        var unifiedDynamicComponentTypes = {};
        _.each(component.dynamicComponentTypes, function(dynamicComponentType) {
            var type = dynamicComponentType['type'];
            if (!unifiedDynamicComponentTypes[type]) {
                unifiedDynamicComponentTypes[type] = dynamicComponentType;
            }
        });
        component.unifiedDynamicComponentTypes = _.values(unifiedDynamicComponentTypes);

        var title = component.propertyViewTitle;
        if (!this.onlyShowUserProperty) {
            title += ('(' + component.cid + ')');
        }
        xlog('[property view]: ' + component.type);
        xlog({
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            dynamicComponents: dynamicComponents, 
            title: title, 
            property_groups: component.properties, 
            model: component.model,
            datasourceProject: W.data.datasourceProject
        });
        var node = $.tmpl(this.template, {
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            dynamicComponents: dynamicComponents, 
            title: title, 
            property_groups: component.properties, 
            model: component.model,
            datasourceProject: []
        });

        this.$(".propertyGroup_property_dynamicControlField").sortable('destroy');
        this.$el.empty().append(node);
        if (component.canEditHtml()) {
            W.data.htmlEditor = ace.edit("htmlEditor"+component.cid);
            W.data.htmlEditor.setTheme("ace/theme/monokai");
            W.data.htmlEditor.getSession().setMode("ace/mode/html");
            this.$('.propertyGroup_property_htmlEditorField').show();
        }

        this.enableSortDynamicComponent();

        this.$('input').eq(0).focus();        
    },

    /*********************************************************
     * onChangeInputContent: 改变输入框中的内容
     *********************************************************/
    onChangeInputContent: function(event) {
        var $input = $(event.target); 
        var value = $input.val();
        var attr = $input.attr('data-field');
        this.getTargetComponent($input).model.set(attr, value);
    },

    /*********************************************************
     * onChangeSelection: 改变select的选项
     *********************************************************/
    onChangeSelection: function(event) {
        var $select = $(event.target);
        var value = $select.val();
        var attr = $select.attr('data-field');
        this.getTargetComponent($select).model.set(attr, value);
    },

    /*********************************************************
     * onChangeTextCheckboxSelection: 改变text-checkbox下checkbox的select的选项
     *********************************************************/
    onChangeTextCheckboxSelection: function(event) {
        var $checkboxGroups = $(event.currentTarget).parents('div.propertyGroup_property_textCheckboxField');
        var results = {};
        $checkboxGroups.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            results[$checkbox.attr('data-column-name')] = {select: $checkbox.is(':checked')};
        });

        var attr = $(event.currentTarget).attr('data-field');
        //this.component.model.set(attr, results);
        this.getTargetComponent($checkboxGroups).model.set(attr, results);
    },

    /**
     * onClickRadioGroupButton: 点击radio group中的button后的响应函数
     */
    onClickRadioGroupButton: function(event) {
        var $node = $(event.currentTarget);
        var $groupNode = $node.parent();
        $groupNode.find('.btn-primary').removeClass('btn-primary');
        $groupNode.find('.icon-white').removeClass('icon-white');
        $node.addClass('btn-primary').find('i').addClass('icon-white');

        var attr = $groupNode.attr('data-field');
        var value = $node.attr('data-value');
        this.component.model.set(attr, value);
    }, 


    /**
     * onClickAddDynamicComponentButton: 点击dynamic component区域中的添加button后的响应函数
     */
    onClickAddDynamicComponentButton: function(event) {
        var $node = $(event.currentTarget);
        var componentType = $node.attr('data-component');
        var component = W.component.Component.create(componentType);
        this.component.addComponent(component, {isAddDynamicComponent: true});

        xlog('[property view]: click add dynamic component button, and crete component' + component.type);
    },

    /**
     * onClickRemoveDynamicComponentButton: 点击dynamic component区域中的remove button后的响应函数
     */
    onClickRemoveDynamicComponentButton: function(event) {
        var $node = $(event.currentTarget);
        var $control = $node.parents('.propertyGroup_property_dynamicControlField_control').eq(0);
        var parentComponentCid = parseInt($control.attr('data-parent-cid'));
        var cid = parseInt($control.attr('data-dynamic-cid'));
        xlog('[property view]: remove ' + cid + ' from ' + parentComponentCid);
        $control.remove();
        W.component.getComponent(parentComponentCid).removeComponent(cid);

        this.updateDynamicComponents();
    },

    /**
     * onClickDynamicComponentTitle: 点击dynamic component区域的title bar后的响应函数
     */
    onClickDynamicComponentTitle: function(event) {
        var $titleBar = $(event.currentTarget);
        if ($titleBar.find('.icon-chevron-down').length > 0) {
            //收缩title
            var $propertyGroup = $titleBar.parents('.propertyGroup');
            $propertyGroup.find('.icon-chevron-down').removeClass('icon-chevron-down');
            $propertyGroup.find('.propertyGroup_property_dynamicControlField_activeContent').hide().removeClass('propertyGroup_property_dynamicControlField_activeContent');
        } else {
            //切换title
            var $propertyGroup = $titleBar.parents('.propertyGroup');
            $propertyGroup.find('.icon-chevron-down').removeClass('icon-chevron-down');
            $propertyGroup.find('.propertyGroup_property_dynamicControlField_activeContent').hide().removeClass('propertyGroup_property_dynamicControlField_activeContent');
            $titleBar.find('.icon-chevron-right').addClass('icon-chevron-down');
            $titleBar.next().addClass('propertyGroup_property_dynamicControlField_activeContent').show();
        }

        this.$el.scrollTop(10000); //确保dynamic component展开后，其编辑区域位于屏幕中
    },

    /**
     * onClickOpenDialogButton: 点击打开select dialog的按钮后的响应函数
     */
    onClickOpenDialogButton: function(event) {
        var $button = $(event.currentTarget);
        var dialog = $button.attr('data-target-dialog');

        var parameter = null;
        var parameterStr = $button.attr('data-dialog-parameter');
        if (parameterStr) {
            parameter = W.data.getData(parameterStr, this.component, $button);
        }

        var options = {
            success: _.bind(function(data) {
                        var $input = $button.parent().find('input[type="hidden"]');
                        console.warn($input);
                        $input.val(data).trigger('input');
                    }, this),
            component: this.component,
            $button: $button
        }

        if (parameter) {
            _.extend(options, parameter);
        }
        
        W.dialog.showDialog(dialog, options);
    },

    /**
     * onClickSaveHtmlEditorContentButton: 点击保存html editor按钮后的响应函数
     */
    onClickSaveHtmlEditorContentButton: function(event) {
        var $button = $(event.currentTarget);
        var attr = $button.parents('.propertyGroup_property_htmlEditorField').find('pre').eq(0).attr('data-field');
        var value = W.data.htmlEditor.getValue();
        this.component.model.set(attr, value);
    },

    /**
     * onHtmlEditorKeypress: 在html editor中按下键盘的响应函数
     */
    onHtmlEditorKeypress: function(event) {
        if (event.ctrlKey && event.which === 115) {
            event.preventDefault();
            event.stopPropagation();

            var clickEvent = {};
            xlog($(event.currentTarget).parents('.propertyGroup_property_htmlEditorField').find('.btn'));
            clickEvent.currentTarget = $(event.currentTarget).parents('.propertyGroup_property_htmlEditorField').find('.btn').get(0);
            this.onClickSaveHtmlEditorContentButton(clickEvent);
        }    
    },

    /**
     * toggleEditor: 切换action button的active状态，切换editor
     */
    toggleEditor: function(event) {
        var $button = $(event.currentTarget);
        if ($button.hasClass('active')) {

        } else {
            this.$('.sectionActionBar a').removeClass('active');
            $button.addClass('active');
        }

        var $target = this.$($button.attr('data-target'));
        if ($target.length > 0) {
            this.$('.propertyView_actionTarget').hide();
            $target.show();
        }
    },

    /**
     * onClickEditPropertyButton: 点击header中“编辑属性”按钮的响应函数
     */
    onClickEditPropertyButton: function(event) {
        this.toggleEditor(event);

        this.$('input').eq(0).focus();
    },

    /**
     * onClickEditDatasourceButton: 点击header中“编辑数据源”按钮的响应函数
     */
    onClickEditDatasourceButton: function(event) {
        /*
        this.toggleEditor(event);

        var existedDatasource = this.component.model.get('datasource');
        var datasource_page_id = existedDatasource.__datasource_page_id;
        if (datasource_page_id && datasource_page_id !== 'null') {
            var $pageSelector = this.$('select[name="__datasource_page_id"]').eq(0);
            $pageSelector.val(__datasource_page_id);

            var event = {
                currentTarget: $pageSelector[0]
            }
            this.onChangeDatasourcePageSelection(event);
        }
        */
        var dialog = 'W.workbench.SelectDatasourceDialog';
        var options = {
            success: _.bind(function(datasource) {
                this.component.model.set('datasource', datasource);
            }, this),
            component: this.component
        }
        W.dialog.showDialog(dialog, options);
    },

    /**
     * onChangeDatasourcePageSelection: 点击header中“编辑数据源”按钮的响应函数
     */
    onChangeDatasourcePageSelection: function(event) {
        var datasource_page_id = $(event.currentTarget).val();
        if (datasource_page_id === 'null') {
            return;
        }
        
        var datasourcePage = _.findWhere(parent.W.data.datasourceProject, {id: datasource_page_id});        
        var $node = $.tmpl(this.getDatasourceFieldsTemplate(), {
            dataItems: this.component.datasource,
            fields: datasourcePage.fields,
            existedDatasource: this.component.model.get('datasource')
        });

        this.$('#datasrouceEditor_dateItems').empty().append($node);
    },

    /**
     * onClickSubmitDatasourceEditorButton: 点击header中“编辑数据源”按钮的响应函数
     */
    onClickSubmitDatasourceEditorButton: function(event) {
        var $datasourceEditor = this.$('#datasourceEditor');
        var datasource = {};
        $datasourceEditor.find('select').each(function() {
            $select = $(this);
            datasource[$select.attr('name')] = $select.val();
        });

        this.component.model.set('datasource', datasource);
    },
});