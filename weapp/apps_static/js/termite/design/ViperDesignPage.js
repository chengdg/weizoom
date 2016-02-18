/**
 * @class W.design.ViperDesignPage
 * viper的设计页面
 */
W.design.ViperDesignPage = W.design.DesignPage.extend({
    refreshPage: function(onPageFinished) {
        this.coverManager.hide();

        this.$el.empty();

        var _this = this;
        W.getApi().call({
            app: 'workbench',
            api: 'viper_design_page/create',
            method: 'post',
            args: {
                page: JSON.stringify(this.page.toJSON()),
                project_id: parent.W.projectId,
                design_mode: 1
            },
            success: function(data) {
                _this.$el.append(data);

                _this.coverManager.refresh();
                _this.enableSortComponent();
                W.initUIRole();

                if (onPageFinished) {
                    onPageFinished();
                }
            },
            error: function(resp) {
                //console.error("Error: in ViperDesignPage. Msg: " + resp);
                alert('渲染页面失败');
            }
        });
    }
});
