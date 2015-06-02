# -*- coding: utf-8 -*-

__author__ = 'chuter'

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

import sys

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)

def import_module(name, package=None):
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1

        name = _resolve_name(name[level:], package, level)

    __import__(name)
    return sys.modules[name]