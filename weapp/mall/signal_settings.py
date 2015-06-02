# -*- coding: utf-8 -*-
import signals
from core import common_util

signal_handlers = {
	signals.check_order_related_resource: [
		'webapp.modules.mall'
	]
}

common_util.register_signal_handlers(signals, signal_handlers)