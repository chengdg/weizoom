/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.common.MessagesLocalStorage = Backbone.Collection.extend({
    initData: [],
    
    initializeEvent: function() {
        this.isCanAlert = null;
        this.href = window.location.href;
        
        this.bind('add', function(model) {
            this.initData.push(model.toJSON());
            this.pushCacheData(model);
        }, this);
        
        var _this = this;
        window.onbeforeunload = function(beforeunload) {
            if(_this.timeoutValue) {
                clearTimeout(_this.timeoutValue);
                _this.timeoutValue = null;
            }
            var initDataString = JSON.stringify(_this.initData);
            var dataString = JSON.stringify(_this.toJSON());
            var isCanAlert = _this.isCanAlert;
            
            if(null === _this.isCanAlert) {
                _this.setLocalStorage();
            }else{
                _this.clearLocalStorage();
            }
            if(initDataString !== dataString && false !== _this.isCanAlert) {
                return true;
            }
        };
        
        window.onload = function() {
            _this.parseData();
        };
        
        $(document).bind('click', function(event) {
            if(_this.timeoutValue) {
                clearTimeout(_this.timeoutValue);
                _this.timeoutValue = null;
            }
            
            _this.isCanAlert = true;
            if(event.target.id === 'submit-btn') {
                _this.isCanAlert = false;
            }
            
            _this.timeoutValue = setTimeout(function() {
                clearTimeout(_this.timeoutValue);
                _this.timeoutValue = null;
                _this.isCanAlert = _this.isCanAlert === true ? null : _this.isCanAlert;
            }, 10);
        });
    },
    
    parseData: function() {
        var cacheData = this.getLocalStorage();
        if(!cacheData) {
            return;
        }
        var cacheDataList = {};
        var i, k;
        for(i = 0, k = cacheData.length; i < k; i++) {
            cacheDataList[cacheData[i].id] = cacheData[i];
            this.addModel(cacheData[i]);
        }
        this.deleteModel(cacheDataList);
    },
    
    addModel: function(modelJson) {
        if(!this.get(modelJson.id)) {
            this.add([modelJson]);
            this.trigger('creat-model-from-cache', this.models[this.length-1]);
        }
        //console.log('addModel===', this.toJSON())
    },
    
    deleteModel: function(cacheDataList) {
        for(i = 0, k = this.length; i < k; i++) {
            if(this.models[i] && !cacheDataList[this.models[i].id]) {
                this.trigger('delete-model-from-cache', this.models[i]);
                this.deleteModel(cacheDataList);
                return;
            }
        }
        //console.log('deleteModel===', this.toJSON())
    },
    
    pushCacheData: function(model) {
        var cacheData = this.getLocalStorage();
        if(!cacheData) {
            return;
        }
        
        var i, k;
        for(i = 0, k = cacheData.length; i < k; i++) {
            if(model.id === cacheData[i].id) {
                model.attributes = cacheData[i];
            }
        }
        //console.log('pushCacheData===', this.toJSON())
    },
    
    clearLocalStorage: function() {
        //console.log('clear===')
        window.localStorage.clear();
    },
    
    setLocalStorage: function() {
        var data = this.toJSON();
        //console.log('set ====',data)
        window.localStorage.setItem('cacheFormValue_' + this.href, JSON.stringify(data));
    },
    
    getLocalStorage: function() {
        var data = window.localStorage.getItem('cacheFormValue_' + this.href);
        this.localStorageData = this.localStorageData || $.evalJson(data);
        //console.log('get ====',this.localStorageData)
        return this.localStorageData;
    },
    
    getInitData: function() {
        return this.initData;
    }
});