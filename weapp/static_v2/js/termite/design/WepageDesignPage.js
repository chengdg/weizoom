/**
 * @class WepageDesignPage
 * wepage设计页面
 */
W.design.WepageDesignPage = W.design.DesignPage.extend({
    refreshPage: function(onPageFinished) {
        alert('没有实现');
    },

    renderComponentFromServer: function(component, onRenderFinished) {
        var _this = this;
        var componentData = component.toJSON();
        var componentContainer = {
            type: 'wepage.runtime_component_container',
            components: [componentData]
        }
        W.getApi().call({
            app: 'termite2',
            api: 'component_render_result',
            method: 'post',
            args: {
                _method: 'put',
                component: JSON.stringify(componentContainer),
                project_id: W.projectId,
                design_mode: 1
            },
            success: function(data) {
                if (onRenderFinished) {
                    onRenderFinished(data);
                }
            },
            error: function(resp) {
                W.showHint('error', '渲染组件失败');
            }
        });
    },
});
