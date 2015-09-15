#coding: utf8
"""
访问WAPI的client

"""

from weapp.settings import WAPI_SECRET_ACCESS_TOKEN, WAPI_HOST
import json
import requests

_api_client = None

def wapi():
	global _api_client
	if _api_client is None:
		_api_client = ApiClient()
	return _api_client


def set_wapi_client(client):
	"""
	用于BDD测试模式
	"""
	global _api_client
	_api_client = TestApiClient(client)
	return


class TestApiClient:
	"""
	用于BDD测试用的ApiClient
	"""

	def __init__(self, client, access_token=WAPI_SECRET_ACCESS_TOKEN):
		self.access_token = access_token
		self.client = client
		return

	def _get(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		url = "/%s" % (addr)
		print("GET: {}".format(url))
		req = self.client.get(url, params)
		return req.content


	def _post(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		url = "/%s" % (addr)
		print("POST: {}".format(url))
		req = self.client.post(url, params)
		return req.content


	def _put(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		params['_method'] = 'put'
		url = "/%s" % (addr)
		print("PUT: {}".format(url))
		req = self.client.post(url, params)
		return req.content


	def _get_json(self, addr, params=None):
		text = self.get(addr, params)
		json_obj = json.loads(text)
		if json_obj is not None:
			if json_obj["code"] == 200:
				return json_obj["data"]
			print("response: {}".format(text))
			raise Exception("Error Message: %s (code: %d)" % (json_obj.get('errMsg'), json_obj.get('code')))
		else:
			print("response: {}".format(text))
			raise Exception("Not valid JSON!")

	def get(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._get_json(url, params)

	def post(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._post(url, params)

	def put(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._put(url, params)


class ApiClient:

	def __init__(self, host=WAPI_HOST, access_token=WAPI_SECRET_ACCESS_TOKEN):
		self.access_token = access_token
		self.hostname = host
		#self.conn = httplib.HTTPConnection(self.hostname)
		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain",
			"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
			#"Cache-Control": "no-cache",
			}
		return


	def _get(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		url = "%s/%s" % (self.hostname, addr)
		print("URL: {}".format(url))
		req = requests.get(url, params=params, headers=self.headers)
		return req.text


	def _post(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		url = "%s/%s" % (self.hostname, addr)
		print("URL: {}".format(url))
		req = requests.post(url, params=params, headers=self.headers)
		return req.text


	def _put(self, addr, params=None):
		if params is None:
			params={'access_token': self.access_token}
		else:
			params['access_token'] = self.access_token
		params['_method'] = 'put'
		url = "%s/%s" % (self.hostname, addr)
		print("PUT: {}".format(url))
		req = requests.post(url, params=params, headers=self.headers)
		return req.text


	def _get_json(self, addr, params=None):
		text = self.get(addr, params)
		json_obj = json.loads(text)
		if json_obj is not None:
			if json_obj["code"] == 200:
				return json_obj["data"]
			print("response: {}".format(text))
			raise Exception("Error Message: %s (code: %d)" % (json_obj.get('errMsg'), json_obj.get('code')))
		else:
			print("response: {}".format(text))
			raise Exception("Not valid JSON!")

	def get(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._get_json(url, params)

	def post(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._post(url, params)

	def put(self, app, resource, params=None):
		url = "%s/api/%s".format(app, resource)
		return self._put(url, params)
