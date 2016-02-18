/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 微信支付JS接口
 * author: chuter
 */
W.WXPayV3 = function(appId,partnerId, parterKey, //商户信息
    productName, orderId, totalFee, //商品名称，订单id和价格（单位为分）
    userIp, //发起支付用户ip
    attach, //附加数据，支付结果通知会原样返回
    notifyUrl, //支付结果通知地址
    secret,
    openid,
    code
    ) {

    this.appId = appId;
    this.partnerId = partnerId;
    this.parterKey = parterKey;
   // this.paySignKey = paySignKey;
    this.productName = productName;
    this.orderId = orderId;
    this.totalFee = totalFee;
    this.userIp = userIp;
    this.attach = attach;
    this.notifyUrl = notifyUrl;

    this.openid = openid;
    this.code = code;
    this.secret = secret;
    this.nonce_str ='';
    this.timestamp = '';
    this.nonce_str_new = ''

    this.pay = function(payCallBack) {
        if (W.isUnderDevelopMode) {
            //开发模式下，直接调用payCallBack
            payCallBack(true, '');
        } else {
            var _this = this;

            W.WeixinJsApi.ready(function(API) {
                WeixinJSBridge.invoke('getBrandWCPayRequest', {
                    "appId" : _this.appId.toString(),
                    "timeStamp" : _this.getTimeStamp(),
                    "nonceStr" : _this.nonce_str_new,
                    "package" : "prepay_id="+_this.prepay_id,
                    "signType" : _this.getSignType(),
                    "paySign" : _this.sign,
                }, function(res) {
        var isPaySucceed = false;
                    var errMsg = res.err_msg;
            alert(errMsg);
                    if (errMsg == "get_brand_wcpay_request:ok") {
                        isPaySucceed = true;
                    } else {
                        try {
                           errMsg += ' -- ' + res.err_code + res.err_desc;
                        } catch (err) {

                            console.log(err);
                         alert("=====aa===:"+err);
            }
                    }

                    payCallBack(isPaySucceed, errMsg);
                });
            });
        }
    };

    //以下是package组包过程：s
    var oldPackageString;//记住package，方便最后进行整体签名时取用
    
    this.getPackageInfo = function() {
        //var attach = this.attach;
        //var banktype = "WX";
        var body = this.productName;
        var fee_type = "1"; //费用类型，这里1为默认的人民币
        var input_charset = "UTF-8"; //字符集，这里将统一使用GBK
        var notify_url = this.notifyUrl; //支付成功后将通知该地址
        var out_trade_no = this.orderId; //订单号，商户需要保证该字段对于本商户的唯一性
        var partner = this.partnerId;//测试商户号
        var spbill_create_ip = this.userIp; //用户浏览器的ip，这个需要在前端获取
        var total_fee = this.totalFee; //总金额
        var partnerKey = this.parterKey; //这个值和以上其他值不一样是：签名需要它，而最后组成的传输字符串不能含有它。这个key是需要商户好好保存的
        var appid = this.appId;
        var openid = this.openid;
        //首先第一步：对原串进行签名，注意这里不要对任何字段进行编码。这里是将参数按照key=value进行字典排序后组成下面的字符串,在这个字符串最后拼接上key=XXXX。由于这里的字段固定，因此只需要按照这个顺序进行排序即可。

        var signString = "appid="+appid+"&body="+body+"&mch_id="+partner+"&notify_url="+notify_url+"&openid="+openid+"&out_trade_no="+out_trade_no+"&spbill_create_ip="+spbill_create_ip+"&trade_type=JSAPI&total_fee="+total_fee+"&key="+partnerKey;
        alert('signString:'+signString);
        //if (attach.length > 0) {
        //   signString = "attach="+attach+"&"+signString;
        //}
        var md5SignValue =  ("" + CryptoJS.MD5(signString)).toUpperCase();
        var data = {
                    woid: this.webappOwnerId, 
                    module:'mall',
                    target_api: 'wixin_pay_package/get',
                    appid : appid,
                    mch_id: partner,
                    nonce_str: this.getNonceStr(),
                    sign:md5SignValue,
                    out_trade_no: out_trade_no,
                    openid: openid,
                    body: body,
                    total_fee: total_fee,
                    notify_url: notify_url,
                    trade_type: 'JSAPI',
                    spbill_create_ip: spbill_create_ip
                };

        $.ajax({ 
            type: "post", 
            url: "/webapp/api/project_api/call/", 
            data: data,
            dataType: "json", 
            success: function (data) { 
                if (data.code == 200){
                    _this.sign = data.data.sign;
                    _this.nonce_str_new = data.data.nonce_str;
                    _this.prepay_id = data.data.prepay_id;
                 } 
            }, 
            error: function (XMLHttpRequest, textStatus, errorThrown) { 
                alert(errorThrown); 
            } 
        });
       
       
        //var nonce_str =this.getNonceStr();

      /*  //然后第二步，对每个参数进行url转码
        //attach = encodeURIComponent(attach);
    appid = encodeURIComponent(appid);
    body = encodeURIComponent(body);
    nonce_str = encodeURIComponent(nonce_str);
        //fee_type = encodeURIComponent(fee_type);
        //input_charset = encodeURIComponent(input_charset);
    notify_url = encodeURIComponent(notify_url);
    out_trade_no = encodeURIComponent(out_trade_no);
    partner = encodeURIComponent(partner);
    spbill_create_ip = encodeURIComponent(spbill_create_ip);
    total_fee = encodeURIComponent(total_fee);
    openid =  encodeURIComponent(openid);

    trade_type = encodeURIComponent('JSAPI');
        
        //然后进行最后一步，这里按照key＝value除了sign外进行字典序排序后组成下列的字符串,最后再串接sign=value
    var completeString = "appid="+appid+"&body="+body+"&mch_id="+partner+"&notify_url="+notify_url+"&openid="+openid+"&out_trade_no="+out_trade_no+"&spbill_create_ip="+spbill_create_ip+"&trade_type=JSAPI&total_fee="+total_fee;
       

    completeString = completeString + "&sign="+md5SignValue;      
    */
 
    };
        
    var oldTimeStamp; //记住timestamp，避免签名时的timestamp与传入的timestamp时不一致
    var oldNonceStr; //记住nonceStr, 避免签名时的nonceStr与传入的nonceStr不一致
        
    this.getTimeStamp = function() {
        if (this.timestamp != ''){
            return this.timestamp;
        }
        var timestamp = new Date().getTime();
        var timestampstring = timestamp.toString(); //一定要转换字符串
        oldTimeStamp = timestampstring;
        return timestampstring;
    };
    
    this.getNonceStr = function() {
        if (this.nonce_str != ''){
            return this.nonce_str;
        }

        var $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var maxPos = $chars.length;
        var noceStr = "";
        for (i = 0; i < 32; i++) {
            noceStr += $chars.charAt(Math.floor(Math.random() * maxPos));
        }
        oldNonceStr = noceStr;
        this.nonce_str = noceStr;
        return noceStr;
    };
    
    this.getSignType = function() {
        return "SHA1";
    };
    
    this.getSign = function() {
        var app_id = this.appId.toString();
        //var app_key = this.paySignKey.toString();
        var timestamp = this.getTimeStamp();
        var nonce_str = oldNonceStr;
        var package_string = oldPackageString;
        var time_stamp = oldTimeStamp;
        alert('oldPackageString::'+oldPackageString)
        //第一步，对所有需要传入的参数加上appkey作一次key＝value字典序的排序
        var keyvaluestring = "appid="+app_id+"&noncestr="+nonce_str+"&package="+package_string+"&signType=SHA1&timestamp="+time_stamp;
        sign = CryptoJS.SHA1(keyvaluestring).toString();
        return sign;
    };

    this.createOauthUrlForCode = function (redirect_uri) {
    var redirect_uri = encodeURIComponent(redirect_uri);
        var queryString = "appid="+this.appId+"&redirect_uri="+redirect_uri+"&response_type=code&scope=snsapi_base&state=123#wechat_redirect";
        return "https://open.weixin.qq.com/connect/oauth2/authorize?"+queryString;
    };

    this.createOauthUrlForOpenid = function(code) {
        var queryString = "appid="+this.appId+"&secret="+this.secret+"&code="+code+"&grant_type=authorization_code";
    return "https://api.weixin.qq.com/sns/oauth2/access_token?"+queryString;
    }

    this.getOpenid = function(code, webappOwnerId) {
        this.code = code;
        var _this = this;
        var data = {woid:webappOwnerId, module:'mall',target_api: 'openid/get',
                appid:_this.appId,
                secret:_this.secret,
                code:code };
 
        $.ajax({ 
            type: "post", 
            url: "/webapp/api/project_api/call/", 
            data: data,
            dataType: "json", 
            success: function (data) { 
                if (data.code == 200){
                    _this.openid = data.data.openid;
                    alert(_this.openid);
                 } 
            }, 
            error: function (XMLHttpRequest, textStatus, errorThrown) { 
                alert(errorThrown); 
            } 
            });
    return _this.openid;
    };
}
