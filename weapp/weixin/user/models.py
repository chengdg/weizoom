# -*- coding: utf-8 -*-

__author__ = 'chuter'

from datetime import datetime
from hashlib import md5

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN

from core.emojicons_util import encode_emojicons_for_html

#########################################################################
# WeixinUser：微信用户
#########################################################################
class WeixinUser(models.Model):
	username = models.CharField(max_length=100, unique=True)
	webapp_id = models.CharField(max_length=16, verbose_name='对应的webapp id')
	fake_id = models.CharField(max_length=50, default="") #微信公众平台字段fakeId
	nick_name = models.CharField(max_length=256) #微信公众平台字段nickName
	weixin_user_remark_name = models.CharField(max_length=64) #微信公众平台字段remarkName,暂未使用
	weixin_user_icon = models.CharField(max_length=1024) #微信公众平台字段icon
	created_at = models.DateTimeField(auto_now_add=True)
	is_head_image_received = models.BooleanField(default=False) #是否接收到头像
	head_image_retry_count = models.IntegerField(default=0) #接收头像的重试次数
	is_subscribed = models.BooleanField(default=True) #是否关注  0 ：取消关注 ，1 ：关注

	class Meta(object):
		managed = False
		ordering = ['-id']
		db_table = 'app_weixin_user'
		verbose_name = '微信用户'
		verbose_name_plural = '微信用户'

	@property
	def weixin_user_nick_name(self):
		if hasattr(self, '_nick_name'):
			return self._nick_name
		from utils.string_util import hex_to_byte
		self._nick_name = hex_to_byte(self.nick_name)
		return self._nick_name

	@weixin_user_nick_name.setter
	def weixin_user_nick_name(self, nick_name):
		from utils.string_util import byte_to_hex
		self.nick_name = byte_to_hex(nick_name)

	@property
	def nickname_for_html(self):
		if hasattr(self, '_nickname_for_html'):
			return self._nickname_for_html

		if (self.nick_name is not None) and (len(self.nick_name) > 0):
			self._nickname_for_html = encode_emojicons_for_html(self.nick_name, is_hex_str=True)
		else:
			self._nickname_for_html = ''

		try:
			#解决用户名本身就是字节码串导致不能正常转换得问题，例如ae
			self._nickname_for_html.decode('utf-8')
		except:
			self._nickname_for_html = self.nick_name

		return self._nickname_for_html

#===============================================================================
# WeixinMpUser : 微信公众号
#===============================================================================
#TODO 删除无用字段
AESKEY_NORMAL = 0
AESKEY_BOTH = 1
AESKEY_ENCODE = 2
class WeixinMpUser(models.Model):
	owner = models.ForeignKey(User, unique=True)
	username = models.CharField(default='', max_length=50) #用户名
	password = models.CharField(default='', max_length=50) #密码
	is_certified = models.BooleanField(default=False, verbose_name='是否进行过微信认证')
	is_service = models.BooleanField(default=False, verbose_name='是否为服务号')
	is_active = models.BooleanField(default=True) #公众号是否有效
	aeskey = models.IntegerField(default=AESKEY_NORMAL)
	encode_aeskey = models.TextField(default='') 
	created_at = models.DateTimeField(auto_now=True) #公众号添加的时间

	def __unicode__(self):
		return self.username

	class Meta(object):
		db_table = 'account_weixin_mp_user'
		verbose_name = '微信公众账号'
		verbose_name_plural = '微信公众账号'


	@staticmethod
	def get_weixin_mp_user(user_id):
		if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
			return WeixinMpUser.objects.filter(owner_id=user_id)[0]
		else:
			return None


	@staticmethod
	def get_weixin_mp_user_access_token_by_mp_user(mpuser):
		if WeixinMpUserAccessToken.objects.filter(mpuser=mpuser).count() > 0:
			return WeixinMpUserAccessToken.objects.filter(mpuser=mpuser)[0]
		else:
			return None


#===============================================================================
# PreviewUser : 预览显示的用户信息
#===============================================================================
DEFAULT_ICON = '/static/img/user-1.jpg'
class MpuserPreviewInfo(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser)
	name = models.CharField(max_length=100)#预览显示的名字
	image_path = models.CharField(max_length=500, default=DEFAULT_ICON)#预览显示的图片

	class Meta(object):
		db_table='account_mpuser_preview_info'
		verbose_name = '微信公众账号预览信息'
		verbose_name_plural = '微信公众账号预览信息'

def update_mpuser_preview_info(instance, created, **kwargs):
	if created:
		return
	from weixin import cache_util
	cache_util.get_mpuser_preview_info_by_mpuser_id(instance.mpuser_id)
signals.post_save.connect(update_mpuser_preview_info, sender=MpuserPreviewInfo, dispatch_uid = "account.mpuser_preview_info")


#===============================================================================
# WeixinMpUserAccessToken : 微信公众号的AccessToken信息
# access_token对应于公众号是全局唯一的票据，重复获取将导致上次获取的access_token
# 失效
#===============================================================================
class WeixinMpUserAccessToken(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser)
	app_id = models.CharField(max_length=64)
	app_secret = models.CharField(max_length=64)
	access_token = models.CharField(max_length=1024, null=True, blank=True) #mp平台返回的access_token
	update_time = models.DateTimeField(auto_now=True)
	expire_time = models.DateTimeField(blank=True, default=datetime.now())
	created_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.mpuser.username

	class Meta(object):
		#managed = False
		db_table = 'weixin_mp_user_access_token'
		verbose_name = '微信公众账号AccessToken'
		verbose_name_plural = '微信公众账号AccessToken'

def set_share_img(request):
	if hasattr(request, 'webapp_owner_info') and request.webapp_owner_info and request.webapp_owner_info.mpuser_preview_info.image_path:
		request.share_img_url = request.webapp_owner_info.mpuser_preview_info.image_path

def get_mpuser_access_token_for(mpuser):
	if mpuser is None:
		return None

	mpuser_access_tokens = WeixinMpUserAccessToken.objects.filter(mpuser=mpuser)
	if mpuser_access_tokens.count() > 0:
		return mpuser_access_tokens[0]
	else:
		return None

def get_mpuser_access_token_by_appid(appid):
	if appid is None:
		return None

	mpuser_access_tokens = WeixinMpUserAccessToken.objects.filter(app_id=appid)
	if mpuser_access_tokens.count() > 0:
		return mpuser_access_tokens[0]
	else:
		return None

#===============================================================================
# get_token_for : 获得(webapp_id, weixin_user_name)对应的weizoom token
#===============================================================================
def get_token_for(webapp_id, weixin_user_name, for_user_from_simulator=False):
	if type(weixin_user_name) == WeixinUser:
		weixin_user_name = weixin_user_name.username

	# try:
	# 	weixin_account = SocialAccount.objects.get(openid=weixin_user_name, webapp_id=webapp_id)
	# 	return weixin_account.token
	# except:
	#	token = md5('%s_%s' % (webapp_id, weixin_user_name)).hexdigest()
	return md5('%s_%s' % (webapp_id, weixin_user_name)).hexdigest()
		# create_social_account(webapp_id, weixin_user_name, token, SOCIAL_PLATFORM_WEIXIN, for_user_from_simulator)
		#return token

def inactive_mpuser_access_token(access_token):
	if access_token is None:
		return

	try:
		latest_access_token = WeixinMpUserAccessToken.objects.get(id=access_token.id)

		if latest_access_token.access_token == access_token.access_token:
			access_token.is_active = False
			access_token.expire_time = datetime.now()
			access_token.save()
	except:
		pass

def get_system_user_binded_mpuser(user):
	if user is None:
		return None
	
	binded_mpusers = WeixinMpUser.objects.filter(owner=user)
	if binded_mpusers.count() > 0:
		return binded_mpusers[0]
	else:
		return None

def is_subscribed(weixin_user):
	return weixin_user.is_subscribed


"""
	<xml><AppId><![CDATA[wx984abb2d00cc47b8]]></AppId>
	<CreateTime>1427710810</CreateTime>
	<InfoType><![CDATA[component_verify_ticket]]></InfoType>
	<ComponentVerifyTicket><![CDATA[Z8RBNjttRu3P5eM8rPe9TW3dA09yuAequP1BmbHhITxs8lZ-
	X-Gxwaegr5lcPkfJ4VAiRLiuLlCrhKmIz-oSpw]]></ComponentVerifyTicket>
	</xml>

	<xml><AppId><![CDATA[wx984abb2d00cc47b8]]></AppId>
	<CreateTime>1427710810</CreateTime>
	<InfoType><![CDATA[component_verify_ticket]]></InfoType>
	<ComponentVerifyTicket><![CDATA[Z8RBNjttRu3P5eM8rPe9TW3dA09yuAequP1BmbHhITxs8lZ-
	X-Gxwaegr5lcPkfJ4VAiRLiuLlCrhKmIz-oSpw]]></ComponentVerifyTicket>
	</xml>
"""

class ComponentInfo(models.Model):
	app_id = models.CharField(max_length=64)
	app_secret = models.CharField(max_length=64)
	component_verify_ticket = models.TextField() 
	token = models.TextField()
	ase_key = models.TextField()
	last_update_time = models.DateTimeField(default=datetime.now())
	component_access_token = models.TextField()
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.app_id

	class Meta(object):
		db_table = 'component_info'
		verbose_name = '第三方帐号信息'
		verbose_name_plural = '第三方帐号信息'

"""
	参数	说明
	authorization_info	授权信息
	authorizer_appid	授权方appid
	authorizer_access_token	授权方令牌（在授权的公众号具备API权限时，才有此返回值）
	expires_in	有效期（在授权的公众号具备API权限时，才有此返回值）
	authorizer_refresh_token	刷新令牌（在授权的公众号具备API权限时，才有此返回值），刷新令牌主要用于公众号第三方平台获取和刷新已授权用户的access_token，只会在授权时刻提供，请妥善保存。 一旦丢失，只能让用户重新授权，才能再次拿到新的刷新令牌
	func_info	公众号授权给开发者的权限集列表（请注意，当出现用户已经将消息与菜单权限集授权给了某个第三方，再授权给另一个第三方时，由于该权限集是互斥的，后一个第三方的授权将去除此权限集，开发者可以在返回的func_info信息中验证这一点，避免信息遗漏），
	1到8分别代表：
	1消息与菜单权限集
	2用户管理权限集
	3帐号管理权限集
	4网页授权权限集
	5微信小店权限集
	6多客服权限集
	7业务通知权限集
	8微信卡券权限集

"""
class ComponentAuthedAppid(models.Model):
	component_info = models.ForeignKey(ComponentInfo)
	auth_code = models.TextField(default='')
	user_id = models.IntegerField(default=0) #对应帐号user id
	last_update_time = models.DateTimeField(default=datetime.now())
	authorizer_appid = models.CharField(max_length=255, default='')
	authorizer_access_token = models.TextField()
	authorizer_refresh_token = models.TextField()
	func_info = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'component_authed_appid'
		verbose_name = '委托授权帐号基本信息'
		verbose_name_plural = '委托授权帐号基本信息'

"""
	参数	说明
	authorizer_info	授权方昵称
	head_img	授权方头像
	service_type_info	授权方公众号类型，0代表订阅号，1代表由历史老帐号升级后的订阅号，2代表服务号
	verify_type_info	授权方认证类型，-1代表未认证，0代表微信认证，1代表新浪微博认证，2代表腾讯微博认证，3代表已资质认证通过但还未通过名称认证，4代表已资质认证通过、还未通过名称认证，但通过了新浪微博认证，5代表已资质认证通过、还未通过名称认证，但通过了腾讯微博认证
	user_name	授权方公众号的原始ID
	alias	授权方公众号所设置的微信号，可能为空
	qrcode_url	二维码图片的URL，开发者最好自行也进行保存
	authorization_info	授权信息
	appid	授权方appid
	func_info	公众号授权给开发者的权限集列表（请注意，当出现用户已经将消息与菜单权限集授权给了某个第三方，再授权给另一个第三方时，由于该权限集是互斥的，后一个第三方的授权将去除此权限集，开发者可以在返回的func_info信息中验证这一点，避免信息遗漏），1到9分别代表：
	消息与菜单权限集
	用户管理权限集
	帐号管理权限集
	网页授权权限集
	微信小店权限集
	多客服权限集
	业务通知权限集
	微信卡券权限集
	微信扫一扫权限集

"""
class ComponentAuthedAppidInfo(models.Model):
	auth_appid = models.ForeignKey(ComponentAuthedAppid)
	nick_name = models.CharField(max_length=255)
	head_img = models.CharField(max_length=255)
	service_type_info = models.CharField(max_length=255)
	verify_type_info = models.CharField(max_length=255)
	user_name = models.CharField(max_length=255) #授权方公众号的原始ID
	alias = models.TextField()
	qrcode_url = models.CharField(max_length=255)
	appid = models.CharField(max_length=255)
	func_info = models.TextField()
	created_at = models.DateTimeField(auto_now=True)

	class Meta(object):
		db_table = 'component_authed_appid_info'
		verbose_name = '委托授权帐号详细信息'
		verbose_name_plural = '委托授权帐号详细信息'


class WoFu(models.Model):
	phone_number =  models.CharField(max_length=25, db_index=True)
	coupon_rule_id = models.IntegerField(db_index=True)
	level = models.IntegerField(db_index=True) # 1234
	is_send = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now=True)

	class Meta(object):
		db_table = 'wofu'
		verbose_name = 'WoFu'
		verbose_name_plural = 'WoFu'

class WoFuLog(models.Model):
	wofu = models.ForeignKey(WoFu)
	member_id = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now=True)

	class Meta(object):
		db_table = 'wofu_log'
		verbose_name = 'wofu_log'
		verbose_name_plural = 'WoFu_log'	