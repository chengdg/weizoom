/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 首页菜单
 */

W.ProblemTitle = Backbone.Model.extend({

})


/**
 * 首页菜单
 */

W.ProblemTitles = W.ApiCollection.extend({
    model: W.ProblemTitle,
    app: 'operation',

    initialize: function(models, options) {
        this.items = null;
    },

    url: function() {
        return this.getApiUrl('problem_titles/get');
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
