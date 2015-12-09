# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import wapi as resource


if __name__ == '__main__':

    products = resource.get('open', 'orders', {})
    print "zl--------------",products