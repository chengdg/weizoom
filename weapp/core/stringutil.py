# -*- coding: utf-8 -*-

"""
 * 处理过长的字符串，截取并添加省略号
 * 注：半角长度为1，全角长度为2
 *
 * pStr:字符串
 * pLen:截取长度
 *
 * return: 截取后的字符串
"""
def cut_string(pstr, plen):
	_ret = __cut_string(pstr, plen)
	_cut_flag = _ret['cutflag']
	_cut_stringn = _ret['cutstring']
	  
	if "1" == _cut_flag:
		return _cut_stringn + "..."
	else:
		return _cut_stringn
      
"""
 * 取得指定长度的字符串
 * 注：半角长度为1，全角长度为2
 * 
 * pStr:字符串
 * pLen:截取长度
 * 
 * return: 截取后的字符串
"""
def __cut_string(pstr, plen):
	# 原字符串长度
	_str_len = len(pstr)
	_cut_string = ''
	# 默认情况下，返回的字符串是原字符串的一部分
	_cut_flag = "1"
	_len_count = 0
	_ret = False
	
	if _str_len <= plen/2:
		_cut_string = pstr
		_ret = True
	
	if not _ret:
		for i in range(_str_len):
			if __is_full(pstr[i]):
				_len_count += 2
			else:
				_len_count += 1
			
			if _len_count > plen:
				_cut_string = pstr[0:i]
				_ret = True
				break
			elif _len_count == plen:
				_cut_string = pstr[0:i + 1]
				_ret = True
				break
	
	if not _ret:
		_cut_string = pstr
		_ret = True
	
	if len(_cut_string) == _str_len:
		_cut_flag = "0"
		
	return {"cutstring":_cut_string, "cutflag":_cut_flag}
      
""" 
 * 判断是否为全角
 * 
 * pChar:长度为1的字符串
 * return: true:全角
 *         false:半角
"""
def __is_full(pchar):
	if ord(pchar[0]) > 128:
		return True
	else:
		return False