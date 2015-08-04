/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 微信支付V3版JS接口
 * author: slzhu
 */
W.WXPayV3 = function(appId, appSecret, partnerId, partnerKey, //商户信息
    productName, orderId, totalFee, //商品名称，订单id和价格（单位为分）
    userIp, //发起支付用户ip
    notifyUrl, //支付结果通知地址
    code
    ) {

    this.appId = appId;
    this.appSecret = appSecret;
    this.partnerId = partnerId;
    this.partnerKey = partnerKey;
    this.productName = productName;
    this.orderId = orderId;
    this.totalFee = totalFee;
    this.userIp = userIp;
    this.notifyUrl = notifyUrl;
    
    this.code = code;
    
    //记录api返回信息
    this.msg = '';

	this.pay = function(payCallBack){
		if (W.isUnderDevelopMode) {
            //开发模式下，直接调用payCallBack
            payCallBack(true, '');
        } else {
        	var _this = this;
        	
        	_this.productName = W.getWeixinStringApi().cutString(_this.productName, 50);
        	_this.getOpenid();
        	if (_this.openid) {
        		_this.getWeixinPayPackage();
        		if (_this.timeStamp && _this.nonceStr && _this.prepayId && _this.paySign) {
	        		W.WeixinJsApi.ready(function(API) {
		                WeixinJSBridge.invoke('getBrandWCPayRequest', {
		                    "appId": _this.appId.toString(),
		                    "timeStamp": _this.timeStamp,
		                    "nonceStr": _this.nonceStr,
		                    "package": "prepay_id=" + _this.prepayId,
		                    "signType":  "MD5",
		                    "paySign": _this.paySign,
		                }, function(res) {
		        			var isPaySucceed = false;
		                    var errMsg = res.err_msg;
		                    var payErrMsg = '';
		                    if (errMsg == "get_brand_wcpay_request:ok") {
		                        isPaySucceed = true;
		                    } else {
		                        try {
		                           	var payDetailMsg = '{\nappId: ' + _this.appId + ',\nappSecret: ' + _this.appSecret + ',\npartnerId: ' + _this.partnerId + ',\npartnerKey: ' + _this.partnerKey + ',\nproductName: ' + _this.productName + ',\norderId: ' + _this.orderId + '\n}';
                            		payErrMsg = 'weixin pay, stage:[getBrandWCPayRequest], result:' + errMsg + ' -- ' + res.err_code + res.err_desc + '\ndetail:' + payDetailMsg;
		                        } catch (err) {
		                        	console.log(err);
		                    	}
		                    }
		                    payCallBack(isPaySucceed, payErrMsg);
		                });
		            });
	            } else {
	            	var getWeixinPayPackageErrMsg = 'weixin pay, stage:[get unifiedorder], result:\n' + _this.msg;
	            	payCallBack(false, getWeixinPayPackageErrMsg);
	            }
        	} else {
        		var getOpenidErrMsg = 'weixin pay, stage:[get openid], result:\n' + _this.msg;
        		payCallBack(false, getOpenidErrMsg);
        	}
    	}
    };

	// 获取openid
    this.getOpenid = function() {
        var _this = this;
        var data = {
        	appid: _this.appId,
			secret: _this.appSecret,
			code: _this.code
		};
        $.ajax({ 
            url: "/pay/weixin/api/openid/get/", 
            data: data,
            async: false,
            type: "post", 
            dataType: "json",
            success: function (data) {
            	_this.msg = JSON.stringify(data);
                if (data.code == 200){
                    _this.openid = data.data.openid;
                }
            }, 
            error: function (XMLHttpRequest, textStatus, errorThrown) { 
                console.log(errorThrown);
            } 
        });
    };
    
    // 获取预支付订单号
    this.getWeixinPayPackage = function() {	
		var _this = this;
		var data = {
            appid: _this.appId,
            mch_id: _this.partnerId,
            body: _this.productName,
            out_trade_no: _this.orderId,
            total_fee: _this.totalFee,
            spbill_create_ip: _this.userIp,
            notify_url: _this.notifyUrl,
            openid: _this.openid,
    		partner_key: _this.partnerKey
        };
        $.ajax({ 
            url: "/pay/weixin/api/unifiedorder/get/",
            data: data,
            async: false,
            type: "post",
            dataType: "json", 
            success: function (data) {
            	_this.msg = JSON.stringify(data);
                if (data.code == 200){
                    _this.nonceStr = data.data.nonce_str;
                    _this.prepayId = data.data.prepay_id;
			        _this.timeStamp = data.data.time_stamp;
			        _this.paySign = data.data.pay_sign;
                 } 
            }, 
            error: function (XMLHttpRequest, textStatus, errorThrown) { 
                console.log(errorThrown); 
            } 
        });
	};
}