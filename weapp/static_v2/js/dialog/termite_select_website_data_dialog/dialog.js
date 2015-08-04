/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择链接dialog
 */
ensureNS('W.dialog.termite');
W.dialog.termite.SelectWebSiteDataDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-checkbox': 'onSelectData',
        'click .xa-search': 'onSearch',
        'keypress .xa-query': 'onPressKey',
        'click .xa-titleNav': 'onClickTitle'
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#termite-select-website-data-dialog-tmpl-src'
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.enableMultiSelection = options.enableMultiSelection || true;
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        this.navData = options.navData;
        this.selectedId = options.selectedId || 0;
        if (options.enableMultiSelection == false) {
            this.enableMultiSelection = false;
        }else{
            this.enableMultiSelection = true;
        }
        
        this.$dialog.find('.xa-query').val('');
    },

    afterShow: function(options) {
        var $activeNav = this.$dialog.find('.xui-dialog-activeTitleNav');
        this.type = $activeNav.data('nav');
        this.setAddBtuHtml();
        this.onSearch();
    },

    onPressKey: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            this.onSearch(event);
        }
    },

    onSearch: function(event) {
        var query = $.trim($('.xa-query').val());
        if (!this.enableMultiSelection) {
            var param = {
                type: this.type,
                query: query,
                selected_id: this.selectedId
            }
        }else{
            var param = {
                type: this.type,
                query: query
            }
        }
        this.table.reload(param)
    },

    onClickTitle: function(event){
        var $el = $(event.currentTarget);
        this.itemType = $el.attr('data-nav');
        this.titleName = $el.text();
        this.$dialog.find('.xa-query').val('');

        var $activeNav = this.$dialog.find('.xui-dialog-activeTitleNav');
        this.type = $activeNav.data('nav');
        this.setAddBtuHtml();

        this.onSearch();
    },

    setAddBtuHtml: function(){
        this.$dialog.find('.xa-itemName').text(this.navData[this.type].dataName);
        this.$dialog.find('.xa-addItem').attr('href', this.navData[this.type].dataLink);
    },

    getItemByType: function(type){
        return _.filter(this.titles, function(item) {
            return item.type == type;
        }, this)[0];
    },

    onSelectData: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var dataId = null;
        var _this = this;
        var id2extraData = this.table.getRawData().data;

        var datas = []
        this.$('tbody tr').each(function() {
            var $tr = $(this);
            var data = null;
            if ($tr.find('.xa-checkbox').is(':checked')) {
                var id = parseInt($tr.data('id'));
                var link = $tr.data('link');
                var title = $tr.data('title');
                data = id2extraData[id];
                if (data) {
                    data['id'] = id;
                    data['link'] = link;
                    data['title'] = title;
                } else {
                    data = {id: id, link: link, title: title};
                }
                data['timestamp'] = new Date().getTime();
            }

            if (data) {
                datas.push(data);
            }
        });

        return datas;
    }
});

W.dialog.termite.SelectCategoriesDialog = W.dialog.termite.SelectWebSiteDataDialog;