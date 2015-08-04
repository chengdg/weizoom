/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 跑马灯
 */

W.mall.SwipePhoto = Backbone.Model.extend({

})


/**
 * 跑马灯
 */

W.mall.SwipePhotos = W.ApiCollection.extend({
    model: W.SwipePhoto,
    app: 'mall',

    initialize: function(models, options) {
    },

    url: function() {
        return this.getApiUrl('swipe_images/get');
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        return data.items;
    }
});
