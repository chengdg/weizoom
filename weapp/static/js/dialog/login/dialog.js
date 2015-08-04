/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 登录的对话框
 * 
 * author: robert
 */
ensureNS('W.weapp.dialog');
W.weapp.dialog.LoginDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#login-info-view').template('login-info-view-dialog-tmpl');
        return "login-info-view-dialog-tmpl";
    },
    
     events: _.extend({
        'click .tx_submit': 'login',
        'focus [name=username]': 'removeErrorInfo',
        'focus [name=password]': 'removeErrorInfo',
        'keyup #loginView': 'enterFunction',
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
    },

    onShow: function(options) {
    },

	enterFunction: function(event) {
		var keyCode = event.keyCode;
		if (keyCode == 13) {
			this.login();
		}
	},
	
    afterShow: function(options) {
    	$('.loginViewBox').append($(this));
    	$(this).find('[name=username]').focus();
    },
    
    removeErrorInfo: function(options) {
    	$('.login-error').addClass('hidden');
    },
    
    login: function(event) {
    	var username = $('[name=username]').val();
    	var password = $('[name=password]').val();
    	if (!(username && password)) {
    		$('.login-error').find('div').text('用户名或密码不能为空！');           	
            $('.login-error').removeClass('hidden');
            return false;
    	}
    	var $checkbox = $('[name=remember_password]');
    	var remember_password = $checkbox[0].checked;
    	W.getApi().call({
    		method: 'post',
            app: 'account',
            api: 'authorized_user/create',
            args: {'username': username, 'password': password, 'remember_password': remember_password},
            scope: this,
            success: function(data) {
              window.location.href = '/';
            },
            error: function(resp) {
				$('.login-error').find('div').text(resp.errMsg);           	
              	$('.login-error').removeClass('hidden');
            }
        });  
    }

});