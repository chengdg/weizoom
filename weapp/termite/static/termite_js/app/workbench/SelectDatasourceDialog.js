/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * select datasource的对话框
 */
W.workbench.SelectDatasourceDialog = Backbone.View.extend({
    events: {
        'click .selectDatasourceDialog_submitBtn': 'onClickSubmitButton',
        'change select[name="page_id"]': 'onChangePageSelection',
        'click .selectDatasourceDialog_typeSwitcher input': 'onClickTypeSwitcher'
    },

    getTemplate: function() {
        $('#select-datasource-dialog-tmpl-src').template('select-datasource-dialog-tmpl');
        return "select-datasource-dialog-tmpl";
    },

    getOneImageTemplate: function() {
        $('#select-image-dialog-one-image-tmpl-src').template('select-image-dialog-one-image-tmpl');
        return "select-image-dialog-one-image-tmpl";
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.template = this.getTemplate();
        $('body').append($.tmpl(this.template, {
            pages: W.data.datasourceProjectPages,
            component: null,
            page: null,
            existedModelDatasource: {},
            existedFieldMap: null
        }));
        this.el = $('#selectDatasourceDialog')[0];
        this.$el = $(this.el);

        this.successCallback = null;
        this.$dialog = this.$el;
        this.component = null;
    },

    render: function() {
    },

    show: function(options) {
        this.successCallback = options.success;
        this.component = options.component;
        xwarn(this.component);
        var existedModelDatasource = options.component.model.get('datasource') || {};

        //确定已选中的page
        var page = null;
        if (existedModelDatasource && existedModelDatasource.page_id) {
            page = _.findWhere(W.data.datasourceProjectPages, {id: existedModelDatasource.page_id})
        }

        var $node = $.tmpl(this.template, {
            pages: W.data.datasourceProjectPages,
            component: this.component,
            page: page,
            existedModelDatasource: existedModelDatasource,
            existedFieldMap: existedModelDatasource ? existedModelDatasource.component_field2page_field : null
        });
        this.$dialog.empty().append($node.contents());
        this.$dialog.modal('show');
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var datasource = {};
        var pageId = this.$dialog.find('select[name="page_id"]').val();
        var type = this.$dialog.find('input[name="type"]:checked').val();
        var recordSource = this.$dialog.find('select[name="record_source"]').val();
        var filterPageField = this.$dialog.find('select[name="filter_page_field"]').val();
        var filterValue = this.$dialog.find('select[name="filter_value"]').val();
        var apiName = this.$dialog.find('input[name="apiName"]').val();

        var componentField2pageField = {};
        this.$dialog.find('.selectDatasourceDialog_fields select').each(function() {
            var $select = $(this);
            var componentField = $select.attr('name');
            var pageField = $select.val();
            componentField2pageField[componentField] = pageField;
        });

        datasource['type'] = type;
        datasource['api_name'] = apiName;
        datasource['page_id'] = pageId;
        datasource['record_source'] = recordSource;
        datasource['filter'] = {
            page_field: filterPageField,
            value: filterValue
        }
        datasource['component_field2page_field'] = componentField2pageField;

        this.$dialog.modal('hide');
        if (this.successCallback) {
            //调用success callback
            var _this = this;
            var task = new W.DelayedTask(function() {
                _this.successCallback(datasource);
                _this.successCallback = null;
            });
          
            task.delay(300);            
        }
    },

    /**
     * onChangePageSelection: 切换page后的响应函数
     */
    onChangePageSelection: function(event) {
        $select = $(event.currentTarget);
        var page = _.findWhere(W.data.datasourceProjectPages, {id: $select.val()})

        var $node = $.tmpl(this.template, {
            pages: W.data.datasourceProjectPages,
            component: this.component,
            page: page,
            existedModelDatasource: {},
            existedFieldMap: {}
        });


        var selector = '.selectDatasourceDialog_record';
        this.$dialog.find(selector).empty().append($node.find(selector).contents());

        var selector = '.selectDatasourceDialog_fields';
        this.$dialog.find(selector).empty().append($node.find(selector).contents());

        var selector = '.selectDatasourceDialog_filter';
        this.$dialog.find(selector).empty().append($node.find(selector).contents());
    },

    /**
     * onClickTypeSwitcher: 点击type switcher的响应函数
     */
    onClickTypeSwitcher: function(event) {
        var $radio = $(event.currentTarget);
        var type = $radio.val();
        if (type === 'data') {
            this.$('.selectDatasourceDialog_apiZone').hide();
            this.$('.selectDatasourceDialog_dataZone').show();
        } else {
            this.$('.selectDatasourceDialog_dataZone').hide();
            this.$('.selectDatasourceDialog_apiZone').show();
        }
    }
});