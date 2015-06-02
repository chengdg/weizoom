# -*- coding: utf-8 -*-
import random
from datetime import timedelta, datetime, date
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.db.models import F

from core import dateutil


