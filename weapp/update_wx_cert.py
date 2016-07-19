# -*- coding: utf-8 -*-

import os
import sys
import requests
from Crypto.Cipher import AES
from Crypto import Random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from mall.models import WxCertSettings
from core.upyun_util import upload_static_file


SECRET_KEY = b'akoANSpqVzuNBAeVscHB1lQnjNosByMc'


def encrypt(content):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(SECRET_KEY, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(content)
    return msg


def update():
    lines = WxCertSettings.objects.all()
    file_path = '/tmp/wx.pem'
    for l in lines:
        owner_id = l.owner_id
        file_name = l.cert_path.split('/')[-1]
        cert = requests.get(l.up_cert_path).content
        with open(file_path, 'wb') as f:
            f.write(encrypt(cert))
        upload_static_file(file_path, "/cert_files/owner_id" + str(owner_id) + "/" + file_name, False)

        file_name = l.key_path.split('/')[-1]
        key = requests.get(l.up_key_path).content
        with open(file_path, 'wb') as f:
            f.write(encrypt(key))
        upload_static_file(file_path, "/cert_files/owner_id" + str(owner_id) + "/" + file_name, False)

update()
