/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/*
*册除下拉框
*/
W.LoginView = W.DropBox.extend({
	SUBMIT_EVENT: 'submit',
	
	CLOSE_EVENT: 'close',
	
	isArrow: true,
	
	isTitle: false,
	
	events:{
		'keyup #loginView': 'enterFunction',
		'click .tx_submit': 'login',
        'focus [name=username]': 'removeErrorInfo',
        'focus [name=password]': 'removeErrorInfo'
	},
	
	getTemplate: function() {
        $('#login-info-show-view').template('login-view-tmpl');
        return "login-view-tmpl";
    },

	initializePrivate: function(options) {
		this.$el = $(this.el);
		this.render();
	},
	
	enterFunction: function(event) {
		var keyCode = event.keyCode;
		if (keyCode == 13) {
			this.login();
		}
	},
	
	setPosition: function() {
		this.$el.css({
			right:'50px',
			top:'114px',
			width: '300px',
			left: 'auto',
			postion: 'relative',
			'border-radius':'0px',
			'-wibkit-border-radius':'0px',
			'-moz-border-radius':'0px'
		});
	},
	
	render: function() {
		var html = $.tmpl(this.getTemplate());
		this.$content.html(html)
		$('.loginViewBox').append(this.$el);
	},
	
	showPrivate: function(options) {
		this.$el.find('.drop-box-arrow-down-right').remove();
		this.$el.find('[name=username]').focus();
	},
	
	submit: function() {
		// this.$('.tx_submit').bottonLoading({status:'show'});
		this.trigger(this.SUBMIT_EVENT);
	},
	
	closePrivate: function() {
		// this.$('.tx_submit').bottonLoading({status:'hide'});
		this.trigger(this.CLOSE_EVENT);
	},
	
	login: function() {
    	var username = $('[name=username]').val();
    	var password = $('[name=password]').val();
    	W.getApi().call({
    		method: 'post',
            app: 'account',
            api: 'authorized_user/create',
            args: {'username': username, 'password': password},
            scope: this,
            success: function(data) {
              window.location.href = '/';
            },
            error: function(resp) {
				$('.login-error').find('div').text(resp.errMsg);           	
              	$('.login-error').removeClass('hidden');
            }
        });  
  },
  
  removeErrorInfo: function(options) {
	  $('.login-error').addClass('hidden');
  },
    
});

/**
 * 获得ItemDeleteView的单例实例
 */
W.getLoginView = function(options) {
	var dialog = W.registry['LoginView'];
	if (!dialog) {
		//创建dialog
		xlog('create LoginView');
		dialog = new W.LoginView(options);
		W.registry['LoginView'] = dialog;
	}
	return dialog;
};