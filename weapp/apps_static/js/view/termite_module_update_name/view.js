/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 修改模块名称
 * 
 * author: liupeiyu
 */
ensureNS('W.view.termite');
W.view.termite.TermiteUpdateNameView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#termite-update-name-info-view').template('termite-update-name-info-dialog-tmpl');
        return "termite-update-name-info-dialog-tmpl";
    },
    
    events:{
     	'click .xa-submit': 'submit',
    },

    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    },
    
    submit: function(event) {
    	var $el = $(event.currentTarget);
        args = {};
        args['id'] = this.modelId;
        args['name'] = this.$el.find('input[name="name"]').val();
        this.submitSendApi(args);
    },

    submitSendApi: function(args){
        if (!W.validate()) {
            return false;
        }
        this.trigger('submit-finish', args);
        /*if (!W.validate()) {
            return false;
        }

        W.getApi().call({
            method:'post',
            app: 'termite2',
            resource: 'custom_module_name',
            args: args,
            success: function(data) {
                window.location.reload();
            },
            error: function() {
                
            }
        })*/
    },
    
    validate: function(args) {
    },
    
    getLogisticsInfo: function() {
    },
    
    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},

    onShow: function(options) {
        this.$content.html($.tmpl(this.getTemplate()));
        this.position = options.position;
        
    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0'
    	})
    },
    
    showPrivate: function(options) {
    	this.modelId = options.modelId;
        this.modelName = options.modelName;
        this.$content.html($.tmpl(this.getTemplate(), {id: this.modelId}));
        this.$el.find('input[name="name"]').attr('value', this.modelName);
	}

});


W.getTermiteUpdateNameView = function(options) {
	var dialog = W.registry['W.view.termite.TermiteUpdateNameView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.termite.TermiteUpdateNameView');
		dialog = new W.view.termite.TermiteUpdateNameView(options);
		W.registry['W.view.termite.TermiteUpdateNameView'] = dialog;
	}
	return dialog;
};