# -*- coding: utf-8 -*-

__author__ = 'chuter'


import hashlib

#===================================================
# md5_sign : 使用MD5的签名字符串
#===================================================
def md5_sign(text, key):
	sign_source = "{}&key={}".format(text, key)
	return hashlib.md5(sign_source).hexdigest().upper()

#===================================================
# md5_sign : 使用MD5的签名字符串
#===================================================
def sha1_sign(appid, appkey, openid, transid, out_trade_no, deliver_timestamp, deliver_status, deliver_msg):
	sign_str = "appid={}&appkey={}&deliver_msg={}&deliver_status={}&deliver_timestamp={}&openid={}&out_trade_no={}&transid={}".format(
				appid,appkey,deliver_msg,deliver_status,deliver_timestamp,openid,out_trade_no,transid)
	return hashlib.sha1(sign_str).hexdigest()#.upper()