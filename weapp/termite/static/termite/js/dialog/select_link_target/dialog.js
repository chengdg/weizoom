/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择链接目标对话框
 */
ensureNS('W.dialog.workbench');
W.dialog.workbench.SelectLinkTargetDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select[name="workspace"]': 'onChangeWorkspace',
        'change select[name="data_category"]': 'onChangeDataCategory'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#select-link-target-dialog-tmpl-src').template('select-link-target-dialog-tmpl');
        return "select-link-target-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.dataCategory2data = {};
        this.currentValue = null;
        this.frozen = options.frozen || null;
        this.name2meta = {}; //记录<dateCategoryNmae-dataValue, dataMeta>映射
    },

    makeOptions: function(options, targetValue) {
        var buf = [];
        var length = options.length;

        //确定是检查inner_name还是检查value，以确定一个option是否被选中
        var isCheckInnerName = false;
        if (targetValue && targetValue.indexOf('innerName:') !== -1) {
            isCheckInnerName = true;
            targetValue = targetValue.substring(10);
        }

        for (var i = 0; i < length; ++i) {
            var option = options[i];
            if (targetValue && isCheckInnerName && option.innerName && (option.innerName === targetValue)) {
                buf.push('<option selected="selected" value="' + option.value + '">' + option.text + '</option>');
            } else if (targetValue && !isCheckInnerName && (targetValue === option.value)) {
                buf.push('<option selected="selected" value="' + option.value + '">' + option.text + '</option>');
            } else {
                buf.push('<option value="' + option.value + '">' + option.text + '</option>');
            }
        }

        return $(buf.join(''));
    },

    makeRadios: function(options, targetValue) {
        var buf = [];
        var length = options.length;

        for (var i = 0; i < length; ++i) {
            var option = options[i];
            
            if (targetValue && (targetValue.indexOf(option.value) !== -1)) {
                buf.push('<label class="radio"><input name="category" type="radio" checked="checked" value="' + option.value + '"/>' + option.text + "</label>");
            } else {
                buf.push('<label class="radio"><input name="category" type="radio" value="' + option.value + '"/>' + option.text + "</label>");
            }
        }

        return $(buf.join(''));
    },

    /**
     * clear: 清空对话框内容
     */
    clear: function() {
        this.$dialog.find('select[name="data_category"]').empty();
        this.$dialog.find('.x-dataContent').empty();
    },

    onShow: function(options) {
        this.clear();
        
        /*
         * 解决运管BUG http://weappop.weizoom.com/watchdog/show/1156883/
         * 解决项目管理BUG http://project.wintim.com:8088/bug/2871/
         * 当获取cid为空时，跳过从W.component里取组件信息，添加使用options.component组件信息
         */
        this.showOptions = options;
        var targetValue = null;
        if (options.hasOwnProperty('currentLinkTarget')) {
            this.currentValue = options.currentLinkTarget;
            targetValue = this.currentValue['workspace'];
        } else {
            var $triggerButton = options.$button;
            var cid = $triggerButton.parents('div[data-dynamic-cid]').attr('data-dynamic-cid');
            var component = W.component.getComponent(parseInt(cid));
            var modelField = $triggerButton.parents('div.propertyGroup_property_input').eq(0).find('input[type="hidden"]').attr('data-field');
            var value = null;
            if (modelField){
                var cid = $triggerButton.parents('div[data-dynamic-cid]').attr('data-dynamic-cid');
                if (cid) {
                    var component = W.component.getComponent(parseInt(cid));
                    value = component.model.get(modelField);
                } else if(options.component && options.component.model && typeof options.component.model.get == 'function')
                    value = options.component.model.get(modelField);
            }
            var targetValue = null;
            if (value) {
                this.currentValue = $.parseJSON(value);
                targetValue = this.currentValue['workspace'];
            }
        }

        var args = {};
        if (this.showOptions.workspace_filter) {
            args['workspace_filter'] = this.showOptions.workspace_filter
        }
        W.getApi().call({
            app: 'webapp',
            api: 'workspaces/get',
            args: args,
            scope: this,
            success: function(data) {
                var $node = this.makeOptions(data, targetValue);
                var $workspaceSelect = this.$dialog.find('select[name="workspace"]');
                $workspaceSelect.empty().append($node);

                if (this.options.frozen) {
                    this.$dialog.find('select[name="workspace"]').attr('disabled', 'disabled');
                }

                if (targetValue) {
                    var event = {};
                    event.currentTarget = $workspaceSelect[0];
                    this.onChangeWorkspace(event);
                }
            },
            error: function() {

            }
        });
    },

    /**
     * onChangeWorkspace: 切换workspace option之后的响应函数
     */
    onChangeWorkspace: function(event) {
        var $select = $(event.currentTarget);
        var workspaceId = $select.val();
        var $dataContent = this.$dialog.find('.x-dataContent');
        $dataContent.empty();
        if (workspaceId === '0') {
            this.$dialog.find('select[name="data_category"]').empty();
            return;
        }
        if (workspaceId === 'custom') {
            //外部链接
            try {
                this.$dialog.find('select[name="data_category"]').empty().html('<option value="外部链接">外部链接</option>');
                $dataContent.html('<label class="input">输入外部链接：<input style="width: 70%;" type="text"/></label>');
                if (this.currentValue && this.currentValue['data'].indexOf('http://') !== -1) {
                    $dataContent.find('input').focus().val(this.currentValue['data']);
                } else {
                    $dataContent.find('input').focus().val('http://');
                }
            } catch(e) {
                
            }
            return;
        }

        //清空data category select
        var $dataCategorySelect = this.$dialog.find('select[name="data_category"]');
        $dataCategorySelect.empty().html('<option value="0">加载筛选项...</option>');

        var args = {
            workspace_id: workspaceId,
            target_api: 'link_targets/get'
        }
        if (this.showOptions.data_category_filter) {
            args['data_category_filter'] = this.showOptions.data_category_filter;
        }

        W.getApi().call({
            app: 'webapp',
            api: 'data_backend_project_api/call',
            args: args,
            scope: this,
            success: function(data) {
                var dataCategories = data;
                var options =[/*{text: '选择筛选项...', value: 0}*/];
                for (var i = 0; i < dataCategories.length; ++i) {
                    var dataCategory = dataCategories[i];
                    this.dataCategory2data[dataCategory['name']] = dataCategory['data'];
                    var datas = dataCategory['data'];
                    for (var j = 0; j < datas.length; ++j) {
                        var data = datas[j];
                        if (data.meta) {
                            this.name2meta[dataCategory['name']+'-'+data.value] = data.meta
                        }
                    }
                    options.push({
                        text: dataCategory['name'],
                        value: dataCategory['name']
                    });
                }

                var targetValue = null;
                if (this.currentValue) {
                    targetValue = this.currentValue['data_category'];
                }
                var $node = this.makeOptions(options, targetValue);
                $dataCategorySelect.empty().append($node);

                if (targetValue) {
                    var event = {}
                    event.currentTarget = $dataCategorySelect[0];
                    this.onChangeDataCategory(event);
                } else {
                    if ($dataCategorySelect.val()) {
                        var event = {}
                        event.currentTarget = $dataCategorySelect[0];
                        this.onChangeDataCategory(event);
                    }
                }

                if (this.options.frozen) {
                    $dataCategorySelect.attr('disabled', 'disabled');
                }
            },
            error: function(resp) {
                alert('加载数据失败!');
            }
        })
    },

    /**
     * onChangeDataCategory: 切换data category option之后的响应函数
     */
    onChangeDataCategory: function(event) {
        var $select = $(event.currentTarget);
        var $dataContent = this.$dialog.find('.x-dataContent')

        var dataCategory = $select.val();
        if (dataCategory === '0') {
            //do nothing
        } else if (dataCategory === 'custom') {
            $dataContent.empty().append($('<label>输入数据：<input type="text" style="width: 80%"/></label>'));
            $dataContent.find('input').val(this.currentValue.data).focus();
        } else {
            var data = this.dataCategory2data[dataCategory];

            var targetValue = null;
            if (this.currentValue) {
                targetValue = this.currentValue['data'];
            }
            var $node = this.makeRadios(data, targetValue);
            $dataContent.empty().append($node);    
        }
    },

    onGetData: function() {
        var workspaceId = this.$dialog.find('select[name="workspace"]').val();
        if (workspaceId === '0') {
            alert('请选择数据!');
            return false;
        }
        var workspaceName = $.trim(this.$dialog.find('option[value="'+workspaceId+'"]').text());

        var dataCategory = this.$dialog.find('select[name="data_category"]').val();
        if (!dataCategory || dataCategory === '0') {
            alert('请选择数据!');
            return false;
        }

        if (dataCategory === '外部链接') {
            var dataContent = $.trim(this.$dialog.find('.x-dataContent input').val());
            if (dataContent.indexOf(W.host) !== -1) {
                alert('链接地址不能是本站地址，请重新输入');
                return false;
            }

            if (dataContent.indexOf('http://') === -1) {
                alert('链接地址需要以http://开头，请重新输入');
                return false;
            }

            var dataContentName = '外部链接';
        } else {
            var $radio = this.$dialog.find('.x-dataContent input[type="radio"]:checked');
            var dataContent = $radio.val();
            var dataContentName = $radio.parent().text();
        }
        if (!dataContent) {
            alert('请选择数据!');
            return false;
        }

        var data = {
            'workspace': workspaceId,
            'workspace_name': workspaceName,
            'data_category': dataCategory,
            'data_item_name': dataContentName,
            'data_path': workspaceName+'-'+dataCategory+'-'+dataContentName
            //'data': (dataContent + '&workspace_id=' + workspaceId + '&project_id=0')
        }

        if (dataContent.indexOf('project_id') != -1) {
            data['data'] = dataContent;
        } else if (dataContent.indexOf('javascript:') != -1) {
            data['data'] = dataContent;
        } else if (dataContent.indexOf('static_nav:') != -1) {
            data['data'] = dataContent;
        } else if (dataContent.indexOf('http://') != -1) {
            data['data'] = dataContent;
        } else {
            data['data'] = (dataContent + '&workspace_id=' + workspaceId);
        }
        if (workspaceId === 'custom') {
            data['data_path'] = data['data'];
        }

        //获取data的meta信息
        var metaKey = data['data_category']+'-'+dataContent;
        var meta = this.name2meta[metaKey];
        if (meta) {
            data['meta'] = meta;
        }

        this.$dialog.find('.x-dataContent').empty();
        this.$dialog.find('select[name="data_category"]').empty();
        this.$dialog.find('select[name="workspace"]').empty().html('<option value="0">加载项目...</option>');
        this.currentValue = null;

        return JSON.stringify(data);
    },
});