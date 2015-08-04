/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/*
 * W.MassMessages: 群发消息组
 */
W.MassMessages = W.ApiCollection.extend({
    model:W.MassMessage,
    app: 'masssend',

    initialize: function(models, options) {
        this.page = '1';
    },

    url: function(){
        return this.getApiUrl('messages/get',{
            page: this.page
        });
    },

    /**
     * 获得分页信息
     */
    getPageData: function() {
        return this.pageInfo;
    },

    setPage: function(page){
          this.page = page;
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        this.pageInfo = data.page_info;
        return data.items;
    }
})