/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 首页菜单
 */

W.ProblemList = Backbone.Model.extend({

})


/**
 * 首页菜单
 */

W.ProblemLists = W.ApiCollection.extend({
    model: W.ProblemList,
    app: 'operation',

    initialize: function(models, options) {
        this.items = null;
    },

    url: function() {
        var _this = this;
        return this.getApiUrl('problems/get/'+_this.titleId);
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        this.items = data.items;
        return data.items;
    },

    getItems: function(){
        return this.items;
    }
});
