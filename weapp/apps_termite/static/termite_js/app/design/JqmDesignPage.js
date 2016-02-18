/**
 * @class JqmDesignPage
 * jquery mobile的设计页面
 */
W.design.JqmDesignPage = W.design.DesignPage.extend({
    refreshPage: function(onPageFinished) {
        //console.log("in JqmDesignPage.refreshPage()");
        
        this.coverManager.hide();

        this.$el.detach();
        xlog('[jqm design page]: destroy page');
        $('div.ui-content').sortable('destroy');
        this.$el.page('destroy');
        this.$el.find('*').remove();

        var _this = this;
        W.getApi().call({
            app: 'workbench',
            api: 'jqm_design_page/create',
            method: 'post',
            args: {
                page: JSON.stringify(this.page.toJSON()),
                project_id: parent.W.projectId,
                design_mode: 1
            },
            success: function(data) {
                _this.$el.append(data);
                _this.$el.prependTo($('body'));
                _this.$el.page();

                //_this.coverManager.updateWidgetPosition();
                _this.coverManager.refresh();
                _this.enableSortComponent();

                if (onPageFinished) {
                    onPageFinished();
                }
            },
            error: function(resp) {
                //console.error("Error: in JqmDesignPage. Msg: "+resp);
                alert('渲染页面失败');
            }
        });
    }
});
